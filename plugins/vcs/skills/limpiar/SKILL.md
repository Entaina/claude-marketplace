---
name: limpiar
description: Descarta cambios no confirmados para restaurar el repositorio a estado limpio
argument-hint: "[archivos...]"
disable-model-invocation: true
allowed-tools: Bash(git status:*) Bash(git diff:*) Bash(git rev-parse:*)
---

# VCS Limpiar - Restablecer a Estado Limpio

Descarta modificaciones y archivos sin rastrear para devolver el repositorio a un estado limpio que coincida con el commit actual. Puede limpiar todos los cambios o archivos específicos. Esto elimina cambios sin confirmar y archivos nuevos.

**Uso**: `/vcs:limpiar [archivos...]`

## Implementación

Limpia el directorio de trabajo descartando modificaciones y eliminando archivos sin rastrear. Puede operar sobre todos los cambios o archivos específicos. Este comando restaura archivos para que coincidan exactamente con el estado del commit actual.

Pasos a ejecutar:
1. Comprobar si estamos en un repositorio git
2. Analizar los parámetros (`$ARGUMENTS`) para determinar el modo de limpieza:
   - Si se proporcionan archivos específicos: limpiar solo esos archivos
   - Si no se especifican archivos: limpiar todos los cambios (limpieza completa)
3. Comprobar estado actual del repositorio para ver qué se limpiará:
   - **Modo selectivo**: Solo analizar archivos especificados para estado de modificación/sin rastrear
   - **Modo completo**: Analizar todos los archivos modificados y archivos sin rastrear
4. Si no hay cambios que limpiar:
   - **Modo selectivo**: Informar al usuario que los archivos especificados ya están limpios
   - **Modo completo**: Informar al usuario que el repositorio ya está limpio
   - Salir sin realizar acción
5. Si hay cambios que limpiar:
   - **Analizar y resumir cambios** usando la misma inteligencia que `vcs:diferencias`:
     - Ejecutar `git diff` y `git diff --cached` para entender los cambios reales
     - Analizar qué tipo de trabajo se perderá (funcionalidades, correcciones, configuración, etc.)
     - Identificar qué partes del proyecto se ven afectadas
     - Determinar el alcance e impacto de los cambios que se descartan
   - **Mostrar resumen completo** con formato apropiado:
     - **Resumen del Trabajo**: Qué tipo de trabajo se perderá permanentemente
     - **Impacto del Proyecto**: Qué partes del proyecto se ven afectadas
     - **Análisis Detallado de Archivos**: Para cada archivo modificado, explicar qué cambios se perderán
     - **Archivos Sin Rastrear**: Listar archivos nuevos que serán eliminados
     - Usar lenguaje claro y no técnico con espaciado apropiado
   - **Pedir confirmación explícita** con advertencia clara sobre pérdida de datos
   - Requerir que el usuario escriba "yes" o "y" para confirmar (sin distinción de mayúsculas)
6. Después de la confirmación:
   - **Modo selectivo**:
     - Usar `git checkout HEAD -- <archivo1> <archivo2> ...` para restablecer archivos modificados específicos
     - Usar `rm <archivo>` para eliminar archivos sin rastrear específicos
     - Preservar otros cambios sin confirmar que no estén en la lista de archivos especificados
   - **Modo completo**:
     - Ejecutar `git reset --hard HEAD` para descartar todas las modificaciones
     - Ejecutar `git clean -fd` para eliminar archivos y directorios sin rastrear
   - Mostrar confirmación de la operación de limpieza con resumen
7. Gestionar casos especiales:
   - **Validación de archivos**: Verificar que los archivos especificados existen en modo selectivo
   - **Soporte de patrones glob**: Gestionar patrones como `*.js`, `src/**/*`
   - Repositorio sin commits (recién inicializado)
   - Problemas de permisos con archivos sin rastrear
   - Archivos que no se pueden eliminar

## Características de Seguridad

- **Múltiples confirmaciones**: Advertencias claras sobre pérdida permanente de datos
- **Vista previa detallada**: Muestra exactamente qué se perderá antes de limpiar
- **Consentimiento explícito**: Requiere escribir confirmación, no solo pulsar Enter
- **Sin acción en repositorio limpio**: Omite operación si no hay nada que limpiar
- **Gestión de errores**: Gestiona con gracia archivos que no se pueden eliminar

## Ejemplos

### Limpiar Todos los Cambios
```bash
/vcs:limpiar
```

Esto hará:
- Analizar el estado actual del repositorio
- Mostrar qué archivos se verán afectados
- Pedir confirmación antes de proceder
- Descartar todas las modificaciones y eliminar archivos sin rastrear
- Devolver el repositorio a estado limpio coincidiendo con el commit actual

### Limpiar Archivos Específicos
```bash
/vcs:limpiar src/auth.js README.md
```

Limpiar solo los archivos especificados, preservando otros cambios sin confirmar.

```bash
/vcs:limpiar *.js
```

Limpiar todos los archivos JavaScript en el directorio actual usando patrones glob.

```bash
/vcs:limpiar src/components/**/*
```

Limpiar todos los archivos en el directorio components y subdirectorios.

### Ejemplo de Interacción de Limpieza Completa:
```
🧹 **Análisis de Limpieza del Repositorio**

## Trabajo que se perderá permanentemente:
**Correcciones de errores y mejoras de documentación** - Mejoras de calidad del código

## Impacto en el proyecto:
**Lógica de aplicación principal y documentación del proyecto** - Archivos esenciales del proyecto

---

## Análisis Detallado de Cambios a Descartar:

**📄 `src/main.js`** - Lógica Principal de la Aplicación
- **Qué se perderá**: Correcciones de errores de autenticación y mejoras de gestión de errores
- **Por qué importa**: Estas correcciones resuelven problemas de inicio de sesión y mejoran la experiencia de usuario
- **Impacto**: Los usuarios pueden seguir experimentando problemas de autenticación

**📄 `README.md`** - Documentación del Proyecto
- **Qué se perderá**: Instrucciones de instalación y ejemplos de uso
- **Por qué importa**: Ayuda a nuevos desarrolladores a comenzar con el proyecto
- **Impacto**: La configuración del proyecto puede no estar clara para nuevos contribuidores

**📄 `config.json`** - Configuración de la Aplicación
- **Qué se perderá**: Configuración actualizada de conexión a base de datos
- **Por qué importa**: Asegura que la aplicación se conecte al entorno de desarrollo correcto
- **Impacto**: La aplicación puede fallar al iniciarse correctamente

## Archivos que serán eliminados:

**📄 `temp_notes.txt`** - Archivo nuevo (142 bytes)
**📄 `debug.log`** - Archivo nuevo (1.2 KB)

---

⚠️  **ADVERTENCIA CRÍTICA: ¡Esta acción no se puede deshacer!**

**Perderás permanentemente**:
- Correcciones importantes de errores en la aplicación principal
- Mejoras de documentación para colaboración del equipo
- Cambios de configuración para el entorno de desarrollo
- 2 archivos nuevos con notas e información de depuración

**Impacto total**: 5 archivos se verán afectados

Escribe "yes" para proceder con la limpieza: _
```

Después de la confirmación:
```
✅ **¡Repositorio Limpiado Correctamente!**

**Acciones realizadas**:
- Descartadas modificaciones en 3 archivos
- Eliminados 2 archivos sin rastrear
- El repositorio ahora coincide con el commit: abc123d - "feat: add user authentication"

Tu directorio de trabajo ahora está limpio y coincide exactamente con el commit actual.
```

### Ejemplo de Interacción de Limpieza Selectiva:
```
🧹 **Análisis de Limpieza Selectiva del Repositorio**

## Archivos solicitados para limpieza:
`src/auth.js`, `README.md`

## Trabajo que se perderá permanentemente en archivos seleccionados:
**Mejoras de autenticación y actualizaciones de documentación** - Correcciones específicas

## Impacto en el proyecto:
**Sistema de autenticación y documentación del proyecto** - Solo componentes seleccionados

---

## Análisis Detallado de Cambios a Descartar:

**📄 `src/auth.js`** - Lógica de Autenticación
- **Qué se perderá**: Mejoras de validación de inicio de sesión y gestión de errores
- **Por qué importa**: Estos cambios corrigen errores de autenticación
- **Impacto**: Los usuarios pueden seguir experimentando problemas de inicio de sesión

**📄 `README.md`** - Documentación del Proyecto
- **Qué se perderá**: Instrucciones de instalación actualizadas
- **Por qué importa**: Ayuda a nuevos desarrolladores a entender el proceso de configuración
- **Impacto**: La documentación de configuración permanece desactualizada

## Archivos que permanecerán sin cambios:

**📄 `config.json`** - Cambios de configuración preservados
**📄 `src/main.js`** - Cambios de aplicación principal preservados
**📄 `temp_notes.txt`** - Archivo sin rastrear preservado

---

⚠️  **ADVERTENCIA: ¡Esta acción no se puede deshacer!**

**Perderás permanentemente cambios en**:
- `src/auth.js` - Mejoras de autenticación
- `README.md` - Actualizaciones de documentación

**Cambios preservados**: 3 otros archivos modificados permanecerán intactos

Escribe "yes" para proceder con la limpieza selectiva: _
```

**Advertencia**: Este comando destruye permanentemente el trabajo sin confirmar. En modo selectivo, solo se ven afectados los archivos especificados, preservando otros cambios. Usa con precaución y solo cuando estés seguro de que quieres perder cambios en los archivos seleccionados.
