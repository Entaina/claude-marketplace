---
description: Autenticar con Google OAuth para leer y escribir archivos de Google Drive
---

# Google Docs Auth - Autenticación OAuth

Autentica con Google OAuth para obtener los tokens de acceso. Requiere que `credentials.json` ya esté configurado (usa `/gdocs:setup` primero).

**Uso**: `/gdocs:auth` (autenticar lectura Y escritura)
**Uso**: `/gdocs:auth read` (solo autenticar lectura)
**Uso**: `/gdocs:auth write` (solo autenticar escritura)

## Implementación

### Fase 1: Verificar que existe credentials.json

1. **Buscar configuración**:
   ```
   proyecto_config = .gdocs/credentials.json
   usuario_config = ~/.gdocs/credentials.json
   ```

2. **Si no existe en ninguna ubicación**:
   ```
   ❌ No se encontró credentials.json

   Ubicaciones buscadas:
   - .gdocs/credentials.json (proyecto)
   - ~/.gdocs/credentials.json (usuario)

   Ejecuta primero: /gdocs:setup
   ```
   **Terminar ejecución.**

3. **Si existe, informar qué configuración se usará**:
   ```
   📁 Usando credenciales de: .gdocs/ (proyecto)
   ```

### Fase 2: Ejecutar autenticación

1. **Determinar qué autenticar según el argumento**:
   - Sin argumento o vacío: autenticar lectura Y escritura
   - `read`: solo autenticar lectura
   - `write`: solo autenticar escritura

2. **Autenticación de lectura** (si aplica):
   ```
   🔐 Autenticando permisos de lectura...
      Se abrirá el navegador para autorizar acceso.
   ```
   ```bash
   python <plugin_path>/scripts/gdrive_reader.py auth
   ```

3. **Autenticación de escritura** (si aplica):
   ```
   🔐 Autenticando permisos de escritura...
      Se abrirá el navegador para autorizar acceso.
   ```
   ```bash
   python <plugin_path>/scripts/gdrive_writer.py auth
   ```

### Fase 3: Mostrar resumen

```
✅ Autenticación completada

Configuración: .gdocs/ (proyecto)

Tokens generados:
- Lectura: .gdocs/token.json ✓
- Escritura: .gdocs/token_write.json ✓

Ya puedes usar:
- /gdocs:read <ruta.gdoc>           → Leer archivos
- /gdocs:write <carpeta> <nombre>   → Crear documentos
```

## Solución de Problemas

### "credentials.json no encontrado"
- Ejecuta `/gdocs:setup` primero para configurar las credenciales

### "ModuleNotFoundError: No module named 'google'"
- Las dependencias no están instaladas
- Ejecuta `/gdocs:setup` para instalar las dependencias de Python

### "Access blocked: This app's request is invalid"
- Las credenciales deben ser tipo "Desktop app" (no "Web application")
- Verifica en Google Cloud Console → APIs & Services → Credentials

### "This app isn't verified"
- Es normal si la app está en modo Testing
- Click en "Advanced" → "Go to [app name] (unsafe)" para continuar

### "User is not a test user"
- Añade tu email en Google Cloud Console:
  OAuth consent screen → Test users → Add users

### El navegador no se abre
- Verifica que hay un navegador por defecto configurado
- Ejecuta el script manualmente para ver errores:
  ```bash
  python <plugin_path>/scripts/gdrive_reader.py auth
  ```

### Token expirado o inválido
- Elimina los tokens y vuelve a autenticar:
  ```bash
  rm .gdocs/token.json .gdocs/token_write.json
  /gdocs:auth
  ```

## Ejemplos

### Autenticación completa (lectura + escritura)
```bash
/gdocs:auth

# → Verifica credentials.json
# → Abre navegador para lectura
# → Abre navegador para escritura
# → Tokens guardados
```

### Solo autenticar lectura
```bash
/gdocs:auth read

# → Solo genera token.json
```

### Solo autenticar escritura
```bash
/gdocs:auth write

# → Solo genera token_write.json
```

### Re-autenticar después de error
```bash
# Si hay problemas con los tokens:
rm .gdocs/token*.json
/gdocs:auth
```
