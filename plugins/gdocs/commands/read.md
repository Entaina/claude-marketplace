---
description: Leer contenido de archivos de Google Drive (Docs, Sheets, Slides) y mostrar como texto
---

# Google Docs Read - Leer Archivos de Google Drive

Lee el contenido de un archivo de Google Drive y lo muestra como texto formateado. Soporta Google Docs, Sheets y Slides.

**Uso**: `/gdocs:read <ruta>`

Donde `<ruta>` es la ruta a un archivo `.gdoc`, `.gsheet`, o `.gslides` en el sistema de archivos local (Google Drive File Stream).

## Implementación

Lee el contenido de un archivo de Google Drive usando la API de Google.

Pasos a ejecutar:

1. **Validar el argumento**:
   - Si no se proporciona ruta:
     ```
     ❌ Uso: /gdocs:read <ruta>

     Ejemplo: /gdocs:read "/Users/usuario/Library/CloudStorage/GoogleDrive-email@ejemplo.com/My Drive/documento.gdoc"
     ```

2. **Verificar que el archivo existe**:
   - Comprobar que la ruta proporcionada existe
   - Si no existe, mostrar error con sugerencias:
     ```
     ❌ Archivo no encontrado: <ruta>

     Verifica que:
     - La ruta es correcta
     - Google Drive File Stream está instalado y sincronizado
     - Tienes acceso al archivo en Google Drive
     ```

3. **Verificar el tipo de archivo**:
   - Extensiones soportadas: `.gdoc`, `.gsheet`, `.gslides`, `.gform`
   - Si la extensión no es soportada:
     ```
     ❌ Tipo de archivo no soportado: <extensión>

     Tipos soportados:
     - .gdoc (Google Docs)
     - .gsheet (Google Sheets)
     - .gslides (Google Slides)
     - .gform (Google Forms - solo muestra ID)
     ```

4. **Localizar el directorio del plugin**:
   - Buscar el directorio del plugin gdocs
   - Path típico: `~/.claude/plugins/entaina/gdocs/scripts/`

5. **Verificar autenticación**:
   - Buscar `token.json` en la misma ubicación donde está `credentials.json`:
     - `.gdocs/token.json` (proyecto) o `~/.gdocs/token.json` (usuario)
   - Si no existe:
     ```
     ❌ No estás autenticado para lectura

     Ejecuta primero: /gdocs:auth read
     ```

6. **Ejecutar el script de lectura**:
   ```bash
   python <plugin_path>/scripts/gdrive_reader.py read "<ruta>"
   ```

7. **Procesar y mostrar el resultado**:
   - Si hay error, mostrar mensaje descriptivo
   - Si éxito, mostrar el contenido formateado
   - Indicar el tipo de archivo leído:
     ```
     📄 Google Doc: <título>
     ─────────────────────
     <contenido>
     ```

## Formato de Salida

### Google Docs
```markdown
# Título del Documento

Contenido del documento convertido a Markdown...

- Listas convertidas
- **Negritas preservadas**

[TABLE]
Celda 1 | Celda 2
Celda 3 | Celda 4
[/TABLE]
```

### Google Sheets
```markdown
# Nombre del Spreadsheet

## Hoja 1

| Columna A | Columna B | Columna C |
| --- | --- | --- |
| Dato 1 | Dato 2 | Dato 3 |

## Hoja 2

| ... | ... |
```

### Google Slides
```markdown
# Título de la Presentación

## Slide 1

Contenido del slide...

---

## Slide 2

Contenido del siguiente slide...
```

## Ejemplos

### Leer un Google Doc
```bash
/gdocs:read "/Users/usuario/Library/CloudStorage/GoogleDrive-email@ejemplo.com/My Drive/Documentos/informe.gdoc"
```

### Leer un Google Sheet
```bash
/gdocs:read "/Users/usuario/Library/CloudStorage/GoogleDrive-email@ejemplo.com/Shared drives/Equipo/datos.gsheet"
```

### Leer un Google Slides
```bash
/gdocs:read "~/Library/CloudStorage/GoogleDrive-email@ejemplo.com/My Drive/presentacion.gslides"
```

### Leer desde Shared Drive
```bash
/gdocs:read "/Users/usuario/Library/CloudStorage/GoogleDrive-email@ejemplo.com/Shared drives/Marketing/propuesta.gdoc"
```

## Solución de Problemas

### "Token has been expired or revoked"
```bash
# Re-autenticar
/gdocs:auth read
# Luego volver a leer
/gdocs:read <ruta>
```

### "File not found" pero el archivo existe
- Verificar que Google Drive File Stream está sincronizado
- Comprobar permisos de acceso en Google Drive
- La ruta debe ser absoluta o relativa al directorio actual

### "Permission denied"
- Verificar que tienes acceso al archivo en Google Drive
- Pedir acceso al propietario del archivo si es necesario

### Contenido vacío o incompleto
- Algunos elementos (imágenes, gráficos) no se convierten a texto
- Los comentarios de Google Docs no se incluyen
- Las celdas con fórmulas muestran el valor calculado, no la fórmula
