# gdocs - Integración con Google Drive

Plugin de Claude Code para leer y escribir archivos de Google Drive (Docs, Sheets, Slides) directamente desde la línea de comandos.

## Capacidades

| Acción | Google Docs | Google Sheets | Google Slides |
|--------|-------------|---------------|---------------|
| **Leer** | ✅ Texto completo | ✅ Todas las hojas | ✅ Texto de slides |
| **Crear** | ✅ Desde Markdown | ❌ | ❌ |
| **Actualizar** | ✅ | ❌ | ❌ |

## Requisitos

- Python 3.10 o superior
- Google Drive File Stream instalado y configurado
- Cuenta de Google con acceso a los archivos

## Instalación

### 1. Instalar el plugin

```bash
claude plugins add entaina/gdocs
```

### 2. Configurar credenciales

```bash
/gdocs:setup
```

El comando te guiará interactivamente:

1. **Validar e instalar dependencias** de Python

2. **Elegir ubicación** de las credenciales:
   - **Proyecto** (`.gdocs/`) - Recomendado para equipos, se añade a `.gitignore`
   - **Usuario** (`~/.gdocs/`) - Para uso personal en todos los proyectos

3. **Obtener `credentials.json`** de Google Cloud:
   - Si ya tienes un proyecto → te guía para crear y descargar las credenciales
   - Si necesitas crear uno nuevo → te guía paso a paso por todo el proceso

### 3. Autenticarse

```bash
/gdocs:auth
```

Se abrirá el navegador para autorizar el acceso a Google Drive.

## Comandos

### `/gdocs:setup` - Configuración

Valida Python, instala dependencias, configura la ubicación de credenciales y guía para obtener `credentials.json`.

```bash
/gdocs:setup
```

### `/gdocs:auth` - Autenticación

Autentica con Google OAuth para habilitar lectura y escritura. Requiere haber ejecutado `/gdocs:setup` primero.

```bash
# Autenticar lectura y escritura
/gdocs:auth

# Solo lectura
/gdocs:auth read

# Solo escritura
/gdocs:auth write
```

### `/gdocs:read` - Leer archivos

Lee el contenido de un archivo de Google Drive.

```bash
# Leer un Google Doc
/gdocs:read "/path/to/documento.gdoc"

# Leer un Google Sheet
/gdocs:read "/path/to/hoja.gsheet"

# Leer un Google Slides
/gdocs:read "/path/to/presentacion.gslides"
```

### `/gdocs:write` - Crear o actualizar documentos

Crea un nuevo Google Doc o actualiza uno existente.

```bash
# Crear documento con contenido
/gdocs:write "/path/to/carpeta" "Nombre Doc" -c "# Título

Contenido en Markdown..."

# Crear desde archivo
/gdocs:write "/path/to/carpeta" "Nombre Doc" -f contenido.md

# Actualizar documento existente
/gdocs:write "/path/to/documento.gdoc" -c "Nuevo contenido"

# Sobrescribir si existe
/gdocs:write "/path/to/carpeta" "Nombre Doc" -c "Contenido" --force
```

## Rutas de Google Drive

### macOS

```bash
# Mi unidad
/Users/{usuario}/Library/CloudStorage/GoogleDrive-{email}/My Drive/

# Unidades compartidas
/Users/{usuario}/Library/CloudStorage/GoogleDrive-{email}/Shared drives/{nombre}/
```

### Windows

```bash
# Mi unidad
G:\My Drive\

# Unidades compartidas
G:\Shared drives\{nombre}\
```

## Formato Markdown

Al escribir documentos, el Markdown se convierte automáticamente:

| Markdown | Google Docs |
|----------|-------------|
| `# Título` | Heading 1 |
| `## Subtítulo` | Heading 2 |
| `### Sección` | Heading 3 |
| `- Item` | Lista con viñetas |
| `**texto**` | Negrita |

## Solución de Problemas

### "Python 3 no encontrado" o "Python 3.10+ requerido"

Instala Python 3.10 o superior:
- macOS: `brew install python3`
- Ubuntu/Debian: `sudo apt install python3`
- Windows: https://www.python.org/downloads/

### "ModuleNotFoundError: No module named 'google'"

Ejecuta `/gdocs:setup` para instalar las dependencias.

### "credentials.json no encontrado"

Ejecuta `/gdocs:setup` para configurar las credenciales.

### "User is not a test user"

Si tu app OAuth está en modo "Testing":
1. Ve a Google Cloud Console → APIs & Services → OAuth consent screen
2. Añade tu email en "Test users"

### "Token has been expired"

```bash
/gdocs:auth
```

### "Folder not found"

- Verifica que Google Drive File Stream está sincronizado
- La ruta debe ser completa y existir en Google Drive

## Estructura del Plugin

```
gdocs/                          # Plugin
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── commands/
│   ├── setup.md               # Configuración de credenciales
│   ├── auth.md                # Autenticación OAuth
│   ├── read.md
│   └── write.md
├── skills/
│   └── gdocs/
│       └── SKILL.md
└── scripts/
    ├── gdrive_reader.py
    ├── gdrive_writer.py
    └── requirements.txt
```

### Credenciales (fuera del plugin)

Las credenciales se buscan en este orden:

```
# 1. Nivel de proyecto (prioridad)
.gdocs/
├── credentials.json
├── token.json
└── token_write.json

# 2. Nivel de usuario (fallback)
~/.gdocs/
├── credentials.json
├── token.json
└── token_write.json
```

**Recomendación:**
- **Equipos**: Usar `.gdocs/` en el proyecto (añadir a `.gitignore`)
- **Personal**: Usar `~/.gdocs/` en el home

## Licencia

MIT
