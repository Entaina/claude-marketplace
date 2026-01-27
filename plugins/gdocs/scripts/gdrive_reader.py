#!/usr/bin/env python3
"""
Google Drive Reader CLI Tool

Reads content from Google Drive files (Docs, Sheets, Slides) and exports to text.
Usage:
    python gdrive_reader.py read <file_path_or_id>
    python gdrive_reader.py list <folder_path>
    python gdrive_reader.py auth  # First-time authentication
"""

import os
import sys
import json
import argparse
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes for read-only access
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/documents.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/presentations.readonly',
]

# Paths - credentials lookup order:
# 1. Project level: ./.gdocs/ (current working directory)
# 2. User level: ~/.gdocs/ (home directory)
def get_config_dir() -> Path:
    """Find the config directory, preferring project-level over user-level."""
    # Check project level first
    project_config = Path.cwd() / '.gdocs'
    if project_config.exists() and (project_config / 'credentials.json').exists():
        return project_config

    # Fall back to user level
    return Path.home() / '.gdocs'

CONFIG_DIR = get_config_dir()
CREDENTIALS_FILE = CONFIG_DIR / 'credentials.json'
TOKEN_FILE = CONFIG_DIR / 'token.json'


def get_credentials():
    """Get or refresh OAuth credentials."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                # Create user config directory if it doesn't exist
                user_config = Path.home() / '.gdocs'
                user_config.mkdir(parents=True, exist_ok=True)

                print("Error: credentials.json no encontrado", file=sys.stderr)
                print("", file=sys.stderr)
                print("Ubicaciones buscadas:", file=sys.stderr)
                print(f"  1. Proyecto: {Path.cwd() / '.gdocs' / 'credentials.json'}", file=sys.stderr)
                print(f"  2. Usuario:  {user_config / 'credentials.json'}", file=sys.stderr)
                print("", file=sys.stderr)
                print("Para obtener credentials.json:", file=sys.stderr)
                print("1. Ve a https://console.cloud.google.com/", file=sys.stderr)
                print("2. Crea un proyecto y habilita las APIs de Drive, Docs, Sheets y Slides", file=sys.stderr)
                print("3. Crea credenciales OAuth 2.0 tipo 'Desktop app'", file=sys.stderr)
                print("4. Descarga el archivo JSON y cópialo a una de las ubicaciones anteriores", file=sys.stderr)
                print("", file=sys.stderr)
                print(f"El directorio {user_config} ha sido creado para ti.", file=sys.stderr)
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds


def get_services(creds):
    """Build Google API service clients."""
    return {
        'drive': build('drive', 'v3', credentials=creds),
        'docs': build('docs', 'v1', credentials=creds),
        'sheets': build('sheets', 'v4', credentials=creds),
        'slides': build('slides', 'v1', credentials=creds),
    }


def extract_doc_id_from_file(file_path: str) -> tuple[str, str]:
    """
    Extract document ID from a .gdoc/.gsheet/.gslides file.
    Returns (doc_id, file_type).
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()
    type_map = {
        '.gdoc': 'doc',
        '.gsheet': 'sheet',
        '.gslides': 'slides',
        '.gform': 'form',
    }

    file_type = type_map.get(suffix)
    if not file_type:
        raise ValueError(f"Unsupported file type: {suffix}")

    with open(path, 'r') as f:
        data = json.load(f)

    doc_id = data.get('doc_id')
    if not doc_id:
        raise ValueError(f"No doc_id found in {file_path}")

    return doc_id, file_type


def format_text_run(text_run: dict) -> str:
    """Format a text run with markdown styling based on its textStyle."""
    content = text_run.get('content', '')
    if not content or content == '\n':
        return content

    text_style = text_run.get('textStyle', {})

    # Check for link
    link = text_style.get('link', {})
    url = link.get('url', '')

    # Check for formatting
    is_bold = text_style.get('bold', False)
    is_italic = text_style.get('italic', False)
    is_strikethrough = text_style.get('strikethrough', False)
    is_code = text_style.get('weightedFontFamily', {}).get('fontFamily', '').lower() in ['courier new', 'consolas', 'monaco', 'menlo', 'monospace']

    # Strip trailing newline for formatting, add back later
    trailing_newline = content.endswith('\n')
    text = content.rstrip('\n')

    if not text:
        return '\n' if trailing_newline else ''

    # Apply code formatting first (no other formatting inside code)
    if is_code:
        text = f'`{text}`'
    else:
        # Apply formatting in order: strikethrough, then bold, then italic
        if is_strikethrough:
            text = f'~~{text}~~'
        if is_bold:
            text = f'**{text}**'
        if is_italic:
            text = f'*{text}*'

    # Apply link
    if url:
        text = f'[{text}]({url})'

    if trailing_newline:
        text += '\n'

    return text


def get_list_prefix(paragraph: dict, list_info: dict) -> str:
    """Get the markdown list prefix for a paragraph based on its bullet."""
    bullet = paragraph.get('bullet', {})
    if not bullet:
        return ''

    list_id = bullet.get('listId', '')
    nesting_level = bullet.get('nestingLevel', 0)

    # Get list properties
    list_props = list_info.get(list_id, {}).get('listProperties', {})
    nesting_levels = list_props.get('nestingLevels', [])

    # Determine if ordered or unordered
    is_ordered = False
    if nesting_level < len(nesting_levels):
        glyph_type = nesting_levels[nesting_level].get('glyphType', '')
        glyph_symbol = nesting_levels[nesting_level].get('glyphSymbol', '')
        # Ordered lists have glyphType like DECIMAL, ALPHA, ROMAN, etc.
        is_ordered = glyph_type in ['DECIMAL', 'ALPHA', 'UPPER_ALPHA', 'ROMAN', 'UPPER_ROMAN']

    indent = '  ' * nesting_level
    prefix = '1. ' if is_ordered else '- '

    return indent + prefix


def read_google_doc(services, doc_id: str) -> str:
    """Read a Google Doc and return its content as markdown."""
    try:
        doc = services['docs'].documents().get(documentId=doc_id).execute()

        content = []
        title = doc.get('title', 'Untitled')
        content.append(f"# {title}\n\n")

        # Get list information for bullet/numbered lists
        lists = doc.get('lists', {})

        for element in doc.get('body', {}).get('content', []):
            if 'paragraph' in element:
                paragraph = element['paragraph']
                para_style = paragraph.get('paragraphStyle', {})
                named_style = para_style.get('namedStyleType', 'NORMAL_TEXT')

                # Build paragraph text with formatting
                para_text = []
                for elem in paragraph.get('elements', []):
                    if 'textRun' in elem:
                        para_text.append(format_text_run(elem['textRun']))
                    elif 'inlineObjectElement' in elem:
                        # Handle inline images
                        para_text.append('[image]')

                text = ''.join(para_text).rstrip('\n')

                if not text.strip():
                    content.append('\n')
                    continue

                # Apply heading styles
                heading_map = {
                    'TITLE': '# ',
                    'HEADING_1': '## ',
                    'HEADING_2': '### ',
                    'HEADING_3': '#### ',
                    'HEADING_4': '##### ',
                    'HEADING_5': '###### ',
                    'HEADING_6': '###### ',
                }

                # Check for list
                list_prefix = get_list_prefix(paragraph, lists)

                if list_prefix:
                    content.append(f"{list_prefix}{text}\n")
                elif named_style in heading_map:
                    # Title is already used for doc title, so headings start at ##
                    content.append(f"{heading_map[named_style]}{text}\n\n")
                else:
                    content.append(f"{text}\n\n")

            elif 'table' in element:
                table = element['table']
                rows = table.get('tableRows', [])

                if not rows:
                    continue

                table_data = []
                for row in rows:
                    row_cells = []
                    for cell in row.get('tableCells', []):
                        cell_text = []
                        for cell_content in cell.get('content', []):
                            if 'paragraph' in cell_content:
                                for elem in cell_content['paragraph'].get('elements', []):
                                    if 'textRun' in elem:
                                        cell_text.append(elem['textRun'].get('content', '').strip())
                        row_cells.append(' '.join(cell_text).replace('|', '\\|'))
                    table_data.append(row_cells)

                if table_data:
                    # Normalize column count
                    max_cols = max(len(row) for row in table_data)
                    for row in table_data:
                        while len(row) < max_cols:
                            row.append('')

                    # Output as markdown table
                    content.append('\n')
                    # Header row
                    content.append('| ' + ' | '.join(table_data[0]) + ' |\n')
                    content.append('| ' + ' | '.join(['---'] * max_cols) + ' |\n')
                    # Data rows
                    for row in table_data[1:]:
                        content.append('| ' + ' | '.join(row) + ' |\n')
                    content.append('\n')

        return ''.join(content)

    except HttpError as e:
        raise Exception(f"Error reading Google Doc: {e}")


def read_google_sheet(services, sheet_id: str) -> str:
    """Read a Google Sheet and return its content as text."""
    try:
        # Get spreadsheet metadata
        spreadsheet = services['sheets'].spreadsheets().get(spreadsheetId=sheet_id).execute()
        title = spreadsheet.get('properties', {}).get('title', 'Untitled')

        content = [f"# {title}\n\n"]

        # Get all sheets
        for sheet in spreadsheet.get('sheets', []):
            sheet_title = sheet.get('properties', {}).get('title', 'Sheet')
            content.append(f"## {sheet_title}\n\n")

            # Get values
            range_name = f"'{sheet_title}'"
            result = services['sheets'].spreadsheets().values().get(
                spreadsheetId=sheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])
            if values:
                # Format as markdown table
                if len(values) > 0:
                    # Header
                    header = values[0]
                    content.append('| ' + ' | '.join(str(cell) for cell in header) + ' |\n')
                    content.append('| ' + ' | '.join(['---'] * len(header)) + ' |\n')

                    # Data rows
                    for row in values[1:]:
                        # Pad row to match header length
                        padded_row = row + [''] * (len(header) - len(row))
                        content.append('| ' + ' | '.join(str(cell) for cell in padded_row) + ' |\n')

                content.append('\n')
            else:
                content.append("(empty sheet)\n\n")

        return ''.join(content)

    except HttpError as e:
        raise Exception(f"Error reading Google Sheet: {e}")


def read_google_slides(services, presentation_id: str) -> str:
    """Read a Google Slides presentation and return its text content."""
    try:
        presentation = services['slides'].presentations().get(
            presentationId=presentation_id
        ).execute()

        title = presentation.get('title', 'Untitled')
        content = [f"# {title}\n\n"]

        for i, slide in enumerate(presentation.get('slides', []), 1):
            content.append(f"## Slide {i}\n\n")

            for element in slide.get('pageElements', []):
                if 'shape' in element:
                    shape = element['shape']
                    if 'text' in shape:
                        for text_element in shape['text'].get('textElements', []):
                            if 'textRun' in text_element:
                                text = text_element['textRun'].get('content', '')
                                if text.strip():
                                    content.append(text)

                elif 'table' in element:
                    table = element['table']
                    content.append("\n[TABLE]\n")
                    for row in table.get('tableRows', []):
                        row_texts = []
                        for cell in row.get('tableCells', []):
                            cell_text = []
                            if 'text' in cell:
                                for text_element in cell['text'].get('textElements', []):
                                    if 'textRun' in text_element:
                                        cell_text.append(text_element['textRun'].get('content', '').strip())
                            row_texts.append(' '.join(cell_text))
                        content.append(' | '.join(row_texts) + '\n')
                    content.append("[/TABLE]\n")

            content.append('\n---\n\n')

        return ''.join(content)

    except HttpError as e:
        raise Exception(f"Error reading Google Slides: {e}")


def read_file(file_path: str) -> str:
    """
    Read content from a Google Drive file (.gdoc, .gsheet, .gslides).
    Returns the text content.
    """
    doc_id, file_type = extract_doc_id_from_file(file_path)

    creds = get_credentials()
    services = get_services(creds)

    if file_type == 'doc':
        return read_google_doc(services, doc_id)
    elif file_type == 'sheet':
        return read_google_sheet(services, doc_id)
    elif file_type == 'slides':
        return read_google_slides(services, doc_id)
    elif file_type == 'form':
        return f"[Google Form - cannot read content directly]\nForm ID: {doc_id}"
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def list_folder(folder_path: str, recursive: bool = False) -> list[dict]:
    """
    List contents of a folder, identifying Google files.
    Returns list of dicts with file info.
    """
    path = Path(folder_path)
    if not path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if not path.is_dir():
        raise ValueError(f"Not a directory: {folder_path}")

    files = []
    pattern = '**/*' if recursive else '*'

    for item in path.glob(pattern):
        if item.is_file():
            suffix = item.suffix.lower()
            file_info = {
                'path': str(item),
                'name': item.name,
                'type': 'unknown',
            }

            if suffix == '.gdoc':
                file_info['type'] = 'google_doc'
            elif suffix == '.gsheet':
                file_info['type'] = 'google_sheet'
            elif suffix == '.gslides':
                file_info['type'] = 'google_slides'
            elif suffix == '.gform':
                file_info['type'] = 'google_form'
            elif suffix in ['.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.md', '.csv']:
                file_info['type'] = 'regular_file'
            elif suffix in ['.jpg', '.jpeg', '.png', '.gif', '.svg']:
                file_info['type'] = 'image'
            else:
                file_info['type'] = 'other'

            files.append(file_info)

    return files


def cmd_auth(args):
    """Authenticate with Google (first-time setup)."""
    print("Autenticando con Google...")
    creds = get_credentials()
    print(f"Autenticación exitosa! Token guardado en {TOKEN_FILE}")


def cmd_read(args):
    """Read content from a Google file."""
    try:
        content = read_file(args.file)
        print(content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_list(args):
    """List contents of a folder."""
    try:
        files = list_folder(args.folder, recursive=args.recursive)

        if args.json:
            print(json.dumps(files, indent=2))
        else:
            for f in files:
                type_icon = {
                    'google_doc': '[DOC]',
                    'google_sheet': '[SHEET]',
                    'google_slides': '[SLIDES]',
                    'google_form': '[FORM]',
                    'regular_file': '[FILE]',
                    'image': '[IMG]',
                    'other': '[?]',
                }.get(f['type'], '[?]')
                print(f"{type_icon} {f['path']}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Read content from Google Drive files'
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # auth command
    auth_parser = subparsers.add_parser('auth', help='Authenticate with Google')
    auth_parser.set_defaults(func=cmd_auth)

    # read command
    read_parser = subparsers.add_parser('read', help='Read a Google file')
    read_parser.add_argument('file', help='Path to .gdoc/.gsheet/.gslides file')
    read_parser.set_defaults(func=cmd_read)

    # list command
    list_parser = subparsers.add_parser('list', help='List folder contents')
    list_parser.add_argument('folder', help='Folder path')
    list_parser.add_argument('-r', '--recursive', action='store_true', help='Recursive listing')
    list_parser.add_argument('--json', action='store_true', help='Output as JSON')
    list_parser.set_defaults(func=cmd_list)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
