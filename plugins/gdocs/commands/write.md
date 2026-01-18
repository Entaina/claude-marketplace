---
description: Crear o actualizar un Google Doc con contenido en formato Markdown
---

# Google Docs Write - Crear o Actualizar Documentos

Crea un nuevo Google Doc o actualiza uno existente con contenido en formato Markdown. El Markdown se convierte automáticamente a formato de Google Docs con headings, listas y negritas.

**Uso**: `/gdocs:write <carpeta> <nombre> -c "<contenido>"`
**Uso**: `/gdocs:write <carpeta> <nombre> -f <archivo>`
**Uso**: `/gdocs:write <ruta.gdoc> -c "<contenido>"` (actualizar existente)

## Argumentos

| Argumento | Descripción |
|-----------|-------------|
| `<carpeta>` | Ruta a la carpeta de Google Drive donde crear el documento |
| `<nombre>` | Nombre del documento (sin extensión .gdoc) |
| `<ruta.gdoc>` | Ruta a un archivo .gdoc existente para actualizar |

## Opciones

| Opción | Descripción |
|--------|-------------|
| `-c "<contenido>"` | Contenido en Markdown a escribir |
| `-f <archivo>` | Archivo local del que leer el contenido |
| `--force` | Sobrescribir si ya existe un documento con ese nombre |

## Implementación

Crea o actualiza un Google Doc usando la API de Google Docs.

Pasos a ejecutar:

1. **Analizar argumentos**:
   - Determinar si es crear nuevo o actualizar existente:
     - Si el primer argumento termina en `.gdoc` → modo actualizar
     - Si no → modo crear (carpeta + nombre)
   - Extraer contenido de `-c` o `-f`
   - Detectar flag `--force`

2. **Validar argumentos**:
   - **Modo crear**: verificar que se proporcionan carpeta y nombre
   - **Modo actualizar**: verificar que el archivo .gdoc existe
   - Verificar que hay contenido (de `-c`, `-f`, o preguntar)

3. **Si no hay contenido especificado**:
   - Preguntar al usuario qué contenido quiere escribir
   - O indicar que debe usar `-c` o `-f`

4. **Localizar el directorio del plugin**:
   - Path típico: `~/.claude/plugins/entaina/gdocs/scripts/`

5. **Verificar autenticación de escritura**:
   - Buscar `token_write.json` en la misma ubicación donde está `credentials.json`:
     - `.gdocs/token_write.json` (proyecto) o `~/.gdocs/token_write.json` (usuario)
   - Si no existe:
     ```
     ❌ No estás autenticado para escritura

     Ejecuta primero: /gdocs:auth write
     ```

6. **Modo CREAR - Ejecutar creación**:
   ```bash
   python <plugin_path>/scripts/gdrive_writer.py create "<carpeta>" "<nombre>" -c "<contenido>"
   # O con archivo
   python <plugin_path>/scripts/gdrive_writer.py create "<carpeta>" "<nombre>" -f "<archivo>"
   # Con --force si aplica
   python <plugin_path>/scripts/gdrive_writer.py create "<carpeta>" "<nombre>" -c "<contenido>" --force
   ```

7. **Modo ACTUALIZAR - Ejecutar actualización**:
   ```bash
   python <plugin_path>/scripts/gdrive_writer.py update "<ruta.gdoc>" -c "<contenido>"
   # O con archivo
   python <plugin_path>/scripts/gdrive_writer.py update "<ruta.gdoc>" -f "<archivo>"
   ```

8. **Procesar resultado**:
   - Si hay error (documento ya existe sin --force):
     ```
     ❌ El documento "<nombre>" ya existe en la carpeta

     Opciones:
     - Usa --force para sobrescribir
     - Elige un nombre diferente
     - Usa modo actualizar: /gdocs:write <ruta.gdoc> -c "contenido"
     ```
   - Si éxito:
     ```
     ✅ Documento creado: <nombre>

     📄 URL: https://docs.google.com/document/d/...
     📁 Ubicación: <carpeta>
     ```

## Conversión de Markdown

El contenido Markdown se convierte a formato Google Docs:

| Markdown | Google Docs |
|----------|-------------|
| `# Título` | Heading 1 |
| `## Subtítulo` | Heading 2 |
| `### Sección` | Heading 3 |
| `#### Subsección` | Heading 4 |
| `- Item` | Lista con viñetas |
| `  - Subitem` | Lista anidada |
| `**texto**` | Negrita |

## Ejemplos

### Crear documento con contenido inline
```bash
/gdocs:write "/Users/usuario/Library/CloudStorage/GoogleDrive-email@ejemplo.com/My Drive/Documentos" "Mi Informe" -c "# Informe Semanal

## Resumen

Esta semana completamos:
- Tarea 1
- Tarea 2

## Próximos pasos

**Importante**: Revisar con el equipo."
```

### Crear documento desde archivo
```bash
/gdocs:write "/Users/usuario/Library/CloudStorage/GoogleDrive-email@ejemplo.com/Shared drives/Equipo/Docs" "Especificación" -f ./spec.md
```

### Sobrescribir documento existente
```bash
/gdocs:write "/path/to/drive/folder" "Documento" -c "Nuevo contenido" --force
```

### Actualizar documento existente
```bash
/gdocs:write "/path/to/documento.gdoc" -c "# Contenido Actualizado

Este es el nuevo contenido del documento."
```

### Crear en Shared Drive
```bash
/gdocs:write "/Users/usuario/Library/CloudStorage/GoogleDrive-email@ejemplo.com/Shared drives/Marketing/Campañas" "Propuesta Q1" -c "# Propuesta de Campaña Q1

## Objetivos
- Aumentar engagement 20%
- Reducir CPA 15%"
```

## Solución de Problemas

### "Folder not found"
- Verificar que la ruta de la carpeta es correcta
- La carpeta debe existir en Google Drive
- Para Shared Drives, la ruta debe incluir "Shared drives/NombreDrive/..."

### "Permission denied"
- Verificar permisos de escritura en la carpeta de Google Drive
- En Shared Drives, necesitas ser "Contributor" o superior

### "Token has been expired or revoked"
```bash
# Re-autenticar escritura
/gdocs:auth write
# Luego volver a intentar
/gdocs:write ...
```

### El formato no se aplica correctamente
- Verificar que el Markdown está bien formateado
- Los headings necesitan espacio después de #: `# Título` (correcto) vs `#Título` (incorrecto)
- Las listas necesitan espacio después de -: `- Item` (correcto)

### Caracteres especiales mal codificados
- El contenido debe estar en UTF-8
- Evitar caracteres de control o secuencias de escape inválidas
