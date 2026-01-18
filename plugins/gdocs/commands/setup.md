---
description: Configurar credenciales de Google Cloud para el plugin gdocs
---

# Google Docs Setup - Configuración de Credenciales

Configura la ubicación de las credenciales y guía al usuario para obtener el archivo `credentials.json` de Google Cloud.

**Uso**: `/gdocs:setup`

## Implementación

### Fase 1: Validar dependencias

1. **Verificar que Python está instalado**:
   ```bash
   python3 --version
   ```

   Si no está instalado:
   ```
   ❌ Python 3 no encontrado

   Este plugin requiere Python 3.10 o superior.

   Instalación:
   - macOS: brew install python3
   - Ubuntu/Debian: sudo apt install python3
   - Windows: https://www.python.org/downloads/
   ```
   **Terminar ejecución.**

2. **Verificar versión mínima** (3.10+):
   ```bash
   python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"
   ```

   Si la versión es inferior:
   ```
   ❌ Python 3.10+ requerido

   Versión actual: X.Y
   Versión mínima: 3.10

   Actualiza Python antes de continuar.
   ```
   **Terminar ejecución.**

3. **Instalar dependencias del plugin**:
   ```
   📦 Instalando dependencias de Python...
   ```
   ```bash
   pip3 install -r <plugin_path>/scripts/requirements.txt
   ```

   Si falla:
   ```
   ❌ Error instalando dependencias

   Intenta manualmente:
   pip3 install google-auth google-auth-oauthlib google-api-python-client
   ```

4. **Confirmar instalación exitosa**:
   ```
   ✅ Dependencias instaladas correctamente
   ```

### Fase 2: Detectar configuración existente

1. **Buscar configuración en orden de prioridad**:
   ```
   proyecto_config = .gdocs/credentials.json (directorio actual)
   usuario_config = ~/.gdocs/credentials.json (home)
   ```

2. **Evaluar estado**:
   - `CASO A`: Existe configuración de proyecto → informar y ofrecer reconfigurar
   - `CASO B`: Existe configuración de usuario pero no de proyecto → preguntar qué hacer
   - `CASO C`: No existe ninguna configuración → preguntar dónde crearla

### Fase 3: Si ya existe configuración (CASO A)

1. **Informar al usuario**:
   ```
   ✅ Configuración encontrada en: .gdocs/

   Archivos:
   - credentials.json ✓

   ¿Qué quieres hacer?

      1. Mantener configuración actual
         Todo listo. Ejecuta /gdocs:auth para autenticarte.

      2. Reconfigurar
         Eliminar configuración actual y empezar de nuevo.
   ```

### Fase 4: Si no hay configuración (CASO C)

1. **Preguntar al usuario dónde configurar**:
   ```
   📁 ¿Dónde quieres guardar las credenciales?

      1. Proyecto (.gdocs/) - Recomendado para equipos
         Las credenciales se guardan en el proyecto.
         Se añadirá automáticamente a .gitignore.

      2. Usuario (~/.gdocs/) - Para uso personal
         Las credenciales se guardan en tu home.
         Funcionan en todos los proyectos.
   ```

2. **Si elige proyecto**:
   - Crear directorio `.gdocs/`
   - Añadir `.gdocs/` al `.gitignore` del proyecto (crear si no existe)
   - Mostrar confirmación

3. **Si elige usuario**:
   - Crear directorio `~/.gdocs/` si no existe

### Fase 5: Guía para obtener credentials.json

Preguntar al usuario:
```
❓ ¿Tienes un proyecto de Google Cloud configurado para este uso?

   1. Sí, ya existe un proyecto con las APIs habilitadas
      Te guiaré para crear y descargar las credenciales.

   2. No, necesito crear uno nuevo
      Te guiaré paso a paso para crear el proyecto y las credenciales.
```

#### Si elige "Sí, ya existe un proyecto":
```
📋 Cómo obtener credentials.json de un proyecto existente:

⚠️  NOTA: Las credenciales OAuth solo se pueden descargar en el momento
    de crearlas. Necesitarás crear una nueva credencial tipo "Desktop".

1. Ve a Google Cloud Console:
   https://console.cloud.google.com/

2. Selecciona tu proyecto en el selector de la parte superior
   (Si no lo ves, pide acceso al administrador del proyecto)

3. Ve a "APIs & Services" → "Credentials":
   https://console.cloud.google.com/apis/credentials

4. Crea una nueva credencial OAuth:
   - Click en "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "Claude Code gdocs" (o el nombre que prefieras)
   - Click en "Create"

5. ¡IMPORTANTE! Descarga el JSON inmediatamente:
   - En el popup que aparece, click en "Download JSON"
   - Este es el ÚNICO momento en que puedes descargarlo

6. Renombra el archivo descargado a: credentials.json

7. Cópialo a: <ruta_destino>/credentials.json

8. Ejecuta: /gdocs:auth
```

#### Si elige "No, necesito crear uno nuevo":
```
📋 Cómo crear un proyecto de Google Cloud y obtener credentials.json:

PASO 1: Crear proyecto
──────────────────────
1. Ve a: https://console.cloud.google.com/
2. Click en el selector de proyecto (parte superior)
3. Click en "New Project"
4. Nombre: elige un nombre descriptivo (ej: "mi-empresa-gdocs")
5. Click en "Create"

PASO 2: Habilitar APIs
──────────────────────
1. Ve a: https://console.cloud.google.com/apis/library
2. Busca y habilita estas 4 APIs:
   - Google Drive API
   - Google Docs API
   - Google Sheets API
   - Google Slides API

PASO 3: Configurar OAuth consent screen
───────────────────────────────────────
1. Ve a: https://console.cloud.google.com/apis/credentials/consent
2. Selecciona "External" (o "Internal" si tienes Google Workspace)
3. Click en "Create"
4. Completa:
   - App name: nombre de tu app
   - User support email: tu email
   - Developer contact: tu email
5. Click en "Save and Continue"
6. En "Scopes": click en "Save and Continue" (no añadir nada)
7. En "Test users": añade los emails de quienes usarán la app
8. Click en "Save and Continue"

PASO 4: Crear credenciales OAuth
────────────────────────────────
1. Ve a: https://console.cloud.google.com/apis/credentials
2. Click en "Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "Claude Code gdocs" (o el nombre que prefieras)
5. Click en "Create"
6. ¡IMPORTANTE! Click en "Download JSON" en el popup
   (Este es el ÚNICO momento en que puedes descargarlo)

PASO 5: Finalizar
─────────────────
1. Renombra el archivo a: credentials.json
2. Cópialo a: <ruta_destino>/credentials.json
3. Ejecuta: /gdocs:auth
```

### Fase 6: Si hay configuración de usuario pero no de proyecto (CASO B)

1. **Preguntar al usuario qué hacer**:
   ```
   🔍 Encontré credenciales en ~/.gdocs/
      ¿Qué quieres hacer?

      1. Usar las credenciales globales (~/.gdocs/)
         Usará tu configuración personal para este proyecto.

      2. Copiar a este proyecto (.gdocs/)
         Creará una copia local para compartir con el equipo.
         Se añadirá automáticamente a .gitignore.

      3. Configurar credenciales diferentes
         Usará credenciales distintas para este proyecto.
   ```

2. **Si elige "Copiar a este proyecto"**:
   - Crear `.gdocs/`
   - Copiar `~/.gdocs/credentials.json` a `.gdocs/credentials.json`
   - Añadir `.gdocs/` a `.gitignore`
   - Informar al usuario que ejecute `/gdocs:auth`

## Gestión de .gitignore

Cuando se configura a nivel de proyecto:

1. **Verificar** que `.gdocs/` no esté ya en `.gitignore`
2. **Si .gitignore existe**, añadir al final:
   ```
   # Google Drive credentials (gdocs plugin)
   .gdocs/
   ```
3. **Si no existe**, crear con ese contenido

## Resumen final

Al terminar, mostrar:
```
✅ Configuración completada

Ubicación: .gdocs/ (proyecto)
           [o ~/.gdocs/ (usuario)]

Siguiente paso:
   /gdocs:auth    → Autenticarte con Google
```

## Solución de Problemas

### "No tengo acceso al proyecto de Google Cloud"
- Contacta al administrador del proyecto para que te añada como "Editor" o te proporcione las credenciales

### "El proyecto no tiene las APIs habilitadas"
- Ve a https://console.cloud.google.com/apis/library
- Habilita: Drive API, Docs API, Sheets API, Slides API

### "No puedo crear credenciales OAuth"
- Verifica que tienes rol de "Editor" o superior en el proyecto
- Asegúrate de que el OAuth consent screen esté configurado
