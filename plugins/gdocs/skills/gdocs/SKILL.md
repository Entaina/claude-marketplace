---
name: Google Drive Integration
description: "Conocimiento sobre integración con Google Drive para leer y escribir archivos (Docs, Sheets, Slides). Se activa cuando el usuario menciona Google Drive, Google Docs, archivos .gdoc/.gsheet/.gslides, quiere leer o escribir documentos en la nube, o usa comandos como /gdocs:setup, /gdocs:auth, /gdocs:read, /gdocs:write."
version: 1.0.0
---

# Integración con Google Drive

Permite leer y escribir archivos de Google Drive directamente desde Claude Code.

## Capacidades

| Acción | Google Docs | Google Sheets | Google Slides |
|--------|-------------|---------------|---------------|
| **Leer** | Texto completo | Todas las hojas como tabla | Texto de todas las diapositivas |
| **Crear** | Desde Markdown | No soportado | No soportado |
| **Actualizar** | Reemplazar contenido | No soportado | No soportado |

## Comandos Disponibles

| Comando | Propósito | Ejemplo |
|---------|-----------|---------|
| `/gdocs:setup` | Configurar credenciales | `/gdocs:setup` |
| `/gdocs:auth` | Autenticarse con Google | `/gdocs:auth` |
| `/gdocs:read` | Leer contenido de un archivo | `/gdocs:read /ruta/archivo.gdoc` |
| `/gdocs:write` | Crear o actualizar un Doc | `/gdocs:write "/ruta/carpeta" "Nombre" -c "Contenido"` |

## Formato de Archivos Google

Los archivos de Google Drive en el sistema de archivos local son archivos JSON con extensiones especiales:

### Archivo .gdoc
```json
{
  "doc_id": "1abc123...",
  "url": "https://docs.google.com/document/d/1abc123..."
}
```

### Archivo .gsheet
```json
{
  "doc_id": "1xyz789...",
  "url": "https://docs.google.com/spreadsheets/d/1xyz789..."
}
```

### Archivo .gslides
```json
{
  "doc_id": "1def456...",
  "url": "https://docs.google.com/presentation/d/1def456..."
}
```

## Rutas Típicas de Google Drive

### macOS con Google Drive File Stream

```
# Mi unidad
/Users/{usuario}/Library/CloudStorage/GoogleDrive-{email}/My Drive/

# Unidades compartidas
/Users/{usuario}/Library/CloudStorage/GoogleDrive-{email}/Shared drives/{nombre}/
```

### Windows

```
# Mi unidad
G:\My Drive\

# Unidades compartidas
G:\Shared drives\{nombre}\
```

## Flujo de Trabajo

```
1. Configuración inicial (solo una vez)
   └── /gdocs:setup
       └── Elige ubicación y obtén credentials.json

2. Autenticación
   └── /gdocs:auth
       └── Se abre navegador para autorizar

3. Lectura de archivos
   └── /gdocs:read <ruta.gdoc>
       └── Muestra contenido como Markdown

4. Escritura de documentos
   └── /gdocs:write <carpeta> <nombre> -c <contenido>
       └── Crea o actualiza el documento
```

## Autenticación

### Tokens generados

| Archivo | Propósito | Permisos |
|---------|-----------|----------|
| `token.json` | Lectura | drive.readonly, docs.readonly, sheets.readonly, slides.readonly |
| `token_write.json` | Escritura | drive, documents |

### Renovación de tokens

Los tokens se renuevan automáticamente. Si expiran:
1. Elimina el archivo de token correspondiente
2. Ejecuta `/gdocs:auth` nuevamente

## Conversión Markdown ↔ Google Docs

### Al escribir (Markdown → Google Docs)

| Markdown | Resultado |
|----------|-----------|
| `# Título` | Heading 1 |
| `## Subtítulo` | Heading 2 |
| `### Sección` | Heading 3 |
| `- Item` | Lista con viñetas |
| `**negrita**` | Texto en negrita |

### Al leer (Google Docs → Markdown)

| Google Docs | Resultado |
|-------------|-----------|
| Título del documento | `# Título` |
| Tablas | Formato `[TABLE]...[/TABLE]` |
| Listas | `- Item` |

## Configuración de Credenciales

Las credenciales se buscan en este orden:

| Ubicación | Descripción | Uso |
|-----------|-------------|-----|
| `.gdocs/` | Nivel de proyecto | Equipos (compartir credenciales) |
| `~/.gdocs/` | Nivel de usuario | Uso personal en todos los proyectos |

### Configuración inicial

1. **Configurar credenciales**:
   ```bash
   /gdocs:setup
   ```
   Te guiará para elegir ubicación y obtener `credentials.json` de Google Cloud.

2. **Autenticarse**:
   ```bash
   /gdocs:auth
   ```
   Abre el navegador para autorizar acceso a Google Drive.

### Archivos de configuración

```
.gdocs/                   # o ~/.gdocs/
├── credentials.json      # OAuth client (de Google Cloud Console)
├── token.json            # Token de lectura (generado)
└── token_write.json      # Token de escritura (generado)
```

## Solución de Problemas

### "credentials.json no encontrado"

Ejecuta `/gdocs:setup` para configurar las credenciales.

Si prefieres hacerlo manualmente:
```bash
# Verificar ubicaciones (busca en este orden):
ls .gdocs/credentials.json        # 1. Nivel de proyecto
ls ~/.gdocs/credentials.json      # 2. Nivel de usuario

# Crear directorio:
mkdir -p .gdocs                   # Para proyecto (añadir a .gitignore)
# o
mkdir -p ~/.gdocs                 # Para usuario
```

### "Access blocked: This app's request is invalid"

- El tipo de credencial debe ser "Desktop app" (no "Web application")
- Verifica la configuración de OAuth consent screen

### "User is not a test user"

Si la app está en modo Testing:
1. Ve a Google Cloud Console → APIs & Services → OAuth consent screen
2. Añade tu email en "Test users"

### "Token has been expired or revoked"

```bash
# Eliminar tokens y re-autenticar
rm .gdocs/token*.json       # Si usas nivel de proyecto
rm ~/.gdocs/token*.json     # Si usas nivel de usuario
/gdocs:auth
```

### "Folder not found"

- Verifica que la ruta existe y es accesible
- Las rutas deben ser de Google Drive File Stream
- Para Shared Drives, usa la ruta completa: `Shared drives/NombreDrive/Carpeta`

### "Permission denied"

- Verifica que tienes acceso al archivo/carpeta en Google Drive
- Para escribir en Shared Drives, necesitas permisos de "Contributor" o superior

## Limitaciones

1. **Solo lectura para Sheets y Slides**: No se pueden crear ni modificar
2. **Formateo básico**: Solo headings, listas y negritas al escribir
3. **Sin imágenes**: Las imágenes en documentos no se procesan
4. **Sin comentarios**: Los comentarios de Google Docs no se incluyen
5. **Rutas locales requeridas**: Necesita Google Drive File Stream instalado

## Scripts Internos

Los comandos utilizan estos scripts Python:

| Script | Uso |
|--------|-----|
| `gdrive_reader.py auth` | Autenticación de lectura |
| `gdrive_reader.py read <ruta>` | Leer archivo |
| `gdrive_writer.py auth` | Autenticación de escritura |
| `gdrive_writer.py create <carpeta> <nombre>` | Crear documento |
| `gdrive_writer.py update <ruta.gdoc>` | Actualizar documento |

## Requisitos

- Python 3.10+
- Google Drive File Stream instalado y configurado
- Credenciales OAuth (ejecuta `/gdocs:setup` para configurar)
