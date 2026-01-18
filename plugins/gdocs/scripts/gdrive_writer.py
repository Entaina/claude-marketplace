#!/usr/bin/env python3
"""
Google Drive Writer CLI Tool

Creates and updates Google Drive files (Docs) from markdown content.
Usage:
    python gdrive_writer.py create <folder_path> <filename> <content>
    python gdrive_writer.py update <gdoc_path> <content>
    python gdrive_writer.py auth  # Re-authenticate with write permissions
"""

import os
import sys
import json
import argparse
import re
import unicodedata
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes for read AND write access
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
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
TOKEN_FILE = CONFIG_DIR / 'token_write.json'  # Separate token for write access


def get_credentials():
    """Get or refresh OAuth credentials with write permissions."""
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
                print("2. Crea un proyecto y habilita las APIs de Drive y Docs", file=sys.stderr)
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
    }


def get_folder_id_from_path(services, folder_path: str) -> str:
    """
    Get the Google Drive folder ID from a local folder path.
    Works with Google Drive File Stream paths.
    """
    path = Path(folder_path)

    # Check if path exists
    if not path.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    if not path.is_dir():
        raise ValueError(f"Not a directory: {folder_path}")

    # For Google Drive File Stream, we need to find the folder by navigating
    # through the drive structure using the path components

    # Extract the relevant path components
    # Example: /Users/elafo/Library/CloudStorage/GoogleDrive-jlafora@entaina.ai/Shared drives/Productos/Metodología

    path_str = str(path)

    # Check if it's a Shared Drive path
    if 'Shared drives' in path_str:
        # Extract shared drive name and subpath
        shared_drives_idx = path_str.find('Shared drives/')
        after_shared = path_str[shared_drives_idx + len('Shared drives/'):]
        parts = after_shared.split('/')
        shared_drive_name = parts[0]
        subpath = '/'.join(parts[1:]) if len(parts) > 1 else ''

        # Find the shared drive
        results = services['drive'].drives().list(
            pageSize=100,
            fields="drives(id, name)"
        ).execute()

        shared_drive_id = None
        for drive in results.get('drives', []):
            if drive['name'] == shared_drive_name:
                shared_drive_id = drive['id']
                break

        if not shared_drive_id:
            raise ValueError(f"Shared drive not found: {shared_drive_name}")

        # If no subpath, return the shared drive root
        if not subpath:
            return shared_drive_id

        # Navigate through the subpath
        current_folder_id = shared_drive_id
        for folder_name in subpath.split('/'):
            if not folder_name:
                continue

            # Try both NFD and NFC normalizations since Drive API has inconsistent encoding
            files = []
            for normalization in ['NFD', 'NFC']:
                normalized_name = unicodedata.normalize(normalization, folder_name)
                query = f"name = '{normalized_name}' and '{current_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
                results = services['drive'].files().list(
                    q=query,
                    spaces='drive',
                    fields='files(id, name)',
                    includeItemsFromAllDrives=True,
                    supportsAllDrives=True,
                    corpora='drive',
                    driveId=shared_drive_id
                ).execute()
                files = results.get('files', [])
                if files:
                    break

            if not files:
                raise ValueError(f"Folder not found: {folder_name} in {current_folder_id}")

            current_folder_id = files[0]['id']

        return current_folder_id

    # For My Drive paths
    elif 'My Drive' in path_str:
        my_drive_idx = path_str.find('My Drive/')
        if my_drive_idx == -1:
            return 'root'

        subpath = path_str[my_drive_idx + len('My Drive/'):]

        current_folder_id = 'root'
        for folder_name in subpath.split('/'):
            if not folder_name:
                continue

            # Try both NFD and NFC normalizations since Drive API has inconsistent encoding
            files = []
            for normalization in ['NFD', 'NFC']:
                normalized_name = unicodedata.normalize(normalization, folder_name)
                query = f"name = '{normalized_name}' and '{current_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
                results = services['drive'].files().list(
                    q=query,
                    spaces='drive',
                    fields='files(id, name)'
                ).execute()
                files = results.get('files', [])
                if files:
                    break

            if not files:
                raise ValueError(f"Folder not found: {folder_name}")

            current_folder_id = files[0]['id']

        return current_folder_id

    else:
        raise ValueError(f"Unsupported path type. Must be a Google Drive path (Shared drives or My Drive): {folder_path}")


def parse_markdown_structure(markdown_content: str) -> list:
    """
    Parse markdown content into a structured list of elements.
    Each element is a dict with: type, text, indent_level, bold_ranges
    """
    elements = []
    lines = markdown_content.split('\n')

    for line in lines:
        element = {
            'original': line,
            'type': 'paragraph',
            'text': line,
            'indent_level': 0,
            'bold_ranges': [],
            'nesting_level': 0,
        }

        # Check for headers
        if line.startswith('#### '):
            element['type'] = 'heading4'
            element['text'] = line[5:]
        elif line.startswith('### '):
            element['type'] = 'heading3'
            element['text'] = line[4:]
        elif line.startswith('## '):
            element['type'] = 'heading2'
            element['text'] = line[3:]
        elif line.startswith('# '):
            element['type'] = 'heading1'
            element['text'] = line[2:]
        # Check for bullets with indentation
        elif line.lstrip().startswith('- '):
            element['type'] = 'bullet'
            # Count leading spaces to determine nesting level
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            element['nesting_level'] = indent // 2  # 2 spaces = 1 level
            element['text'] = stripped[2:]  # Remove "- "
        # Empty line
        elif not line.strip():
            element['type'] = 'empty'
            element['text'] = ''

        # Find bold text (**text**) in the text
        text = element['text']
        bold_pattern = re.compile(r'\*\*(.+?)\*\*')
        offset = 0
        new_text = text
        bold_ranges = []

        for match in bold_pattern.finditer(text):
            # Calculate position in the cleaned text
            start = match.start() - offset
            inner_text = match.group(1)
            end = start + len(inner_text)
            bold_ranges.append((start, end))
            # Update offset for removed ** markers
            offset += 4  # Two ** on each side

        # Remove ** markers from text
        new_text = bold_pattern.sub(r'\1', text)
        element['text'] = new_text
        element['bold_ranges'] = bold_ranges

        elements.append(element)

    return elements


def build_formatted_doc_requests(elements: list) -> tuple[str, list]:
    """
    Build the plain text and formatting requests from parsed elements.
    Returns (plain_text, formatting_requests).
    """
    # Build plain text first
    plain_lines = []
    for elem in elements:
        plain_lines.append(elem['text'])

    plain_text = '\n'.join(plain_lines)
    if not plain_text.endswith('\n'):
        plain_text += '\n'

    # Now build formatting requests
    # We need to track positions in the final text
    requests = []
    current_pos = 1  # Google Docs starts at index 1

    # Track bullet ranges for batch processing
    bullet_ranges = []

    for elem in elements:
        line_text = elem['text']
        line_length = len(line_text) + 1  # +1 for newline

        if elem['type'] == 'heading1':
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': current_pos, 'endIndex': current_pos + line_length},
                    'paragraphStyle': {'namedStyleType': 'HEADING_1'},
                    'fields': 'namedStyleType'
                }
            })
        elif elem['type'] == 'heading2':
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': current_pos, 'endIndex': current_pos + line_length},
                    'paragraphStyle': {'namedStyleType': 'HEADING_2'},
                    'fields': 'namedStyleType'
                }
            })
        elif elem['type'] == 'heading3':
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': current_pos, 'endIndex': current_pos + line_length},
                    'paragraphStyle': {'namedStyleType': 'HEADING_3'},
                    'fields': 'namedStyleType'
                }
            })
        elif elem['type'] == 'heading4':
            # H4 - use HEADING_4 or fall back to HEADING_3 with smaller font
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': current_pos, 'endIndex': current_pos + line_length},
                    'paragraphStyle': {'namedStyleType': 'HEADING_4'},
                    'fields': 'namedStyleType'
                }
            })
        elif elem['type'] == 'bullet':
            bullet_ranges.append({
                'start': current_pos,
                'end': current_pos + line_length,
                'nesting': elem['nesting_level']
            })

        # Add bold formatting
        for bold_start, bold_end in elem['bold_ranges']:
            abs_start = current_pos + bold_start
            abs_end = current_pos + bold_end
            if abs_end > abs_start:
                requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': abs_start, 'endIndex': abs_end},
                        'textStyle': {'bold': True},
                        'fields': 'bold'
                    }
                })

        current_pos += line_length

    # Process bullets - group consecutive bullets and apply formatting
    if bullet_ranges:
        # Group consecutive bullets
        groups = []
        current_group = [bullet_ranges[0]]

        for i in range(1, len(bullet_ranges)):
            prev = bullet_ranges[i - 1]
            curr = bullet_ranges[i]
            # Check if consecutive (allowing for some gap due to sub-bullets)
            if curr['start'] <= prev['end'] + 2:
                current_group.append(curr)
            else:
                groups.append(current_group)
                current_group = [curr]
        groups.append(current_group)

        # Apply bullet formatting to each group
        for group in groups:
            # Apply bullets to the entire range
            group_start = group[0]['start']
            group_end = group[-1]['end']

            requests.append({
                'createParagraphBullets': {
                    'range': {'startIndex': group_start, 'endIndex': group_end},
                    'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                }
            })

            # Apply nesting levels
            for bullet in group:
                if bullet['nesting'] > 0:
                    # Increase indent for nested bullets
                    for _ in range(bullet['nesting']):
                        requests.append({
                            'updateParagraphStyle': {
                                'range': {'startIndex': bullet['start'], 'endIndex': bullet['end']},
                                'paragraphStyle': {
                                    'indentFirstLine': {'magnitude': 18 * (bullet['nesting'] + 1), 'unit': 'PT'},
                                    'indentStart': {'magnitude': 18 * (bullet['nesting'] + 1), 'unit': 'PT'},
                                },
                                'fields': 'indentFirstLine,indentStart'
                            }
                        })

    return plain_text, requests


def create_google_doc_simple(services, folder_id: str, title: str, content: str, shared_drive_id: str = None) -> dict:
    """
    Create a Google Doc with the given content and proper formatting.
    Returns dict with doc_id and web link.
    """
    # Create the document
    doc = services['docs'].documents().create(body={'title': title}).execute()
    doc_id = doc['documentId']

    # Move to the target folder
    # First, get current parents
    file = services['drive'].files().get(
        fileId=doc_id,
        fields='parents',
        supportsAllDrives=True
    ).execute()

    previous_parents = ','.join(file.get('parents', []))

    # Move the file
    if shared_drive_id:
        services['drive'].files().update(
            fileId=doc_id,
            addParents=folder_id,
            removeParents=previous_parents,
            supportsAllDrives=True,
            fields='id, parents'
        ).execute()
    else:
        services['drive'].files().update(
            fileId=doc_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields='id, parents'
        ).execute()

    # Parse markdown and build formatted content
    if content.strip():
        elements = parse_markdown_structure(content)
        plain_text, format_requests = build_formatted_doc_requests(elements)

        # First insert the plain text
        requests = [{
            'insertText': {
                'location': {'index': 1},
                'text': plain_text
            }
        }]

        # Then add all formatting requests
        requests.extend(format_requests)

        services['docs'].documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()

    # Get the web link
    file_info = services['drive'].files().get(
        fileId=doc_id,
        fields='webViewLink',
        supportsAllDrives=True
    ).execute()

    return {
        'doc_id': doc_id,
        'url': file_info.get('webViewLink', f'https://docs.google.com/document/d/{doc_id}')
    }


def create_google_doc(services, folder_id: str, title: str, content: str, shared_drive_id: str = None) -> dict:
    """
    Create a Google Doc in the specified folder with the given content.
    Returns dict with doc_id and web link.
    """
    try:
        return create_google_doc_simple(services, folder_id, title, content, shared_drive_id)
    except HttpError as e:
        raise Exception(f"Error creating Google Doc: {e}")


def update_google_doc(services, doc_id: str, content: str) -> dict:
    """
    Update an existing Google Doc with new content and proper formatting.
    Replaces all content.
    """
    try:
        # Get the document to find its length
        doc = services['docs'].documents().get(documentId=doc_id).execute()

        # Calculate end index (document content length)
        end_index = 1
        for element in doc.get('body', {}).get('content', []):
            if 'endIndex' in element:
                end_index = max(end_index, element['endIndex'])

        requests = []

        # Delete existing content (if any)
        if end_index > 2:
            requests.append({
                'deleteContentRange': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': end_index - 1
                    }
                }
            })

        # Execute deletion first if needed
        if requests:
            services['docs'].documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()

        # Now insert and format new content
        if content.strip():
            elements = parse_markdown_structure(content)
            plain_text, format_requests = build_formatted_doc_requests(elements)

            # Insert plain text first
            insert_requests = [{
                'insertText': {
                    'location': {'index': 1},
                    'text': plain_text
                }
            }]

            # Add formatting requests
            insert_requests.extend(format_requests)

            services['docs'].documents().batchUpdate(
                documentId=doc_id,
                body={'requests': insert_requests}
            ).execute()

        return {'doc_id': doc_id, 'updated': True}

    except HttpError as e:
        raise Exception(f"Error updating Google Doc: {e}")


def find_doc_in_folder(services, folder_id: str, doc_name: str, shared_drive_id: str = None) -> str | None:
    """
    Find a Google Doc by name in a folder.
    Returns doc_id if found, None otherwise.
    """
    query = f"name = '{doc_name}' and '{folder_id}' in parents and mimeType = 'application/vnd.google-apps.document' and trashed = false"

    if shared_drive_id:
        results = services['drive'].files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            corpora='drive',
            driveId=shared_drive_id
        ).execute()
    else:
        results = services['drive'].files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()

    files = results.get('files', [])
    return files[0]['id'] if files else None


def create_local_gdoc_link(folder_path: str, doc_id: str, doc_name: str) -> str:
    """
    Create a local .gdoc file that links to the Google Doc.
    This allows the file to appear in Google Drive File Stream.
    """
    gdoc_path = Path(folder_path) / f"{doc_name}.gdoc"

    gdoc_content = {
        "doc_id": doc_id,
        "url": f"https://docs.google.com/document/d/{doc_id}"
    }

    with open(gdoc_path, 'w') as f:
        json.dump(gdoc_content, f)

    return str(gdoc_path)


def get_shared_drive_id_from_path(folder_path: str) -> str | None:
    """Extract shared drive ID from path if it's a Shared drives path."""
    if 'Shared drives' not in folder_path:
        return None

    # We'll need to look this up via API
    return "needs_lookup"


def cmd_auth(args):
    """Authenticate with Google (with write permissions)."""
    # Remove existing token to force re-auth
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        print(f"Token existente eliminado: {TOKEN_FILE}")

    print("Autenticando con Google (permisos de escritura)...")
    creds = get_credentials()
    print(f"Autenticación exitosa! Token guardado en {TOKEN_FILE}")


def cmd_create(args):
    """Create a new Google Doc in the specified folder."""
    try:
        creds = get_credentials()
        services = get_services(creds)

        # Read content from file or stdin
        if args.content_file:
            with open(args.content_file, 'r') as f:
                content = f.read()
        elif args.content:
            content = args.content
        else:
            content = sys.stdin.read()

        # Get folder ID
        folder_id = get_folder_id_from_path(services, args.folder)

        # Determine shared drive ID if applicable
        shared_drive_id = None
        if 'Shared drives' in args.folder:
            # Get the shared drive ID
            path_str = args.folder
            shared_drives_idx = path_str.find('Shared drives/')
            after_shared = path_str[shared_drives_idx + len('Shared drives/'):]
            shared_drive_name = after_shared.split('/')[0]

            results = services['drive'].drives().list(
                pageSize=100,
                fields="drives(id, name)"
            ).execute()

            for drive in results.get('drives', []):
                if drive['name'] == shared_drive_name:
                    shared_drive_id = drive['id']
                    break

        # Check if doc already exists
        existing_doc_id = find_doc_in_folder(services, folder_id, args.name, shared_drive_id)

        if existing_doc_id:
            if args.force:
                # Update existing doc
                result = update_google_doc(services, existing_doc_id, content)
                print(f"Documento actualizado: {args.name}")
                print(f"Doc ID: {existing_doc_id}")
                print(f"URL: https://docs.google.com/document/d/{existing_doc_id}")
            else:
                print(f"El documento '{args.name}' ya existe en la carpeta.", file=sys.stderr)
                print(f"Usa --force para sobrescribir.", file=sys.stderr)
                sys.exit(1)
        else:
            # Create new doc
            result = create_google_doc(services, folder_id, args.name, content, shared_drive_id)
            print(f"Documento creado: {args.name}")
            print(f"Doc ID: {result['doc_id']}")
            print(f"URL: {result['url']}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_update(args):
    """Update an existing Google Doc."""
    try:
        creds = get_credentials()
        services = get_services(creds)

        # Read the .gdoc file to get doc_id
        gdoc_path = Path(args.gdoc_file)
        if not gdoc_path.exists():
            print(f"Archivo no encontrado: {args.gdoc_file}", file=sys.stderr)
            sys.exit(1)

        with open(gdoc_path, 'r') as f:
            gdoc_data = json.load(f)

        doc_id = gdoc_data.get('doc_id')
        if not doc_id:
            print(f"No se encontró doc_id en {args.gdoc_file}", file=sys.stderr)
            sys.exit(1)

        # Read content from file or stdin
        if args.content_file:
            with open(args.content_file, 'r') as f:
                content = f.read()
        elif args.content:
            content = args.content
        else:
            content = sys.stdin.read()

        result = update_google_doc(services, doc_id, content)
        print(f"Documento actualizado: {gdoc_path.stem}")
        print(f"Doc ID: {doc_id}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Create and update Google Drive files'
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # auth command
    auth_parser = subparsers.add_parser('auth', help='Authenticate with Google (write permissions)')
    auth_parser.set_defaults(func=cmd_auth)

    # create command
    create_parser = subparsers.add_parser('create', help='Create a Google Doc')
    create_parser.add_argument('folder', help='Folder path (Google Drive path)')
    create_parser.add_argument('name', help='Document name (without extension)')
    create_parser.add_argument('-c', '--content', help='Content to write')
    create_parser.add_argument('-f', '--content-file', help='File to read content from')
    create_parser.add_argument('--force', action='store_true', help='Overwrite if exists')
    create_parser.set_defaults(func=cmd_create)

    # update command
    update_parser = subparsers.add_parser('update', help='Update an existing Google Doc')
    update_parser.add_argument('gdoc_file', help='Path to .gdoc file')
    update_parser.add_argument('-c', '--content', help='Content to write')
    update_parser.add_argument('-f', '--content-file', help='File to read content from')
    update_parser.set_defaults(func=cmd_update)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
