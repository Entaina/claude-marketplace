---
description: Guarda cambios en el control de versiones con mensaje automático o personalizado
---

# VCS Guardar - Añadir y Confirmar Cambios

Guarda los cambios actuales en el sistema de control de versiones con un mensaje de confirmación. Puede guardar todos los cambios o archivos que coincidan con descripciones en lenguaje natural. Usa la opción -m para mensajes de confirmación.

**Uso**: `/vcs:guardar [descripción-archivos] -m "mensaje confirmación"`
**Uso**: `/vcs:guardar [descripción-archivos]` (genera mensaje automáticamente)
**Uso**: `/vcs:guardar -m "mensaje confirmación"` (guarda todos los cambios)

## Implementación

Añade cambios y crea una confirmación con el mensaje proporcionado, o genera uno automáticamente analizando los cambios. Este comando combina `git add` y `git commit -m` en una sola operación fácil de usar con generación inteligente de mensajes de confirmación y selección de archivos en lenguaje natural.

Pasos a ejecutar:
1. Comprobar si estamos en un repositorio git
2. Analizar los argumentos del comando:
   - Extraer la opción `-m "mensaje"` si está presente
   - Identificar la descripción de archivos (todo antes de la opción -m, o el argumento completo si no hay -m)
   - Si no hay descripción de archivos: guardar todos los cambios
3. **Interpretación de Archivos**: Si se proporciona descripción de archivos, interpretar el lenguaje natural para encontrar archivos coincidentes:
   - **Archivos específicos**: "archivo1.js archivo2.py" → añadir archivos exactos
   - **Extensiones**: "todos los archivos JavaScript" → encontrar *.js
   - **Carpetas**: "todos los archivos en la carpeta src" → encontrar src/**/*
   - **Patrones**: "archivos de prueba" → encontrar *test*, *spec*, test/**/*
   - **Tipos de archivo**: "archivos de configuración" → encontrar *.json, *.yml, *.config.*, etc.
   - **Cambios recientes**: "archivos modificados" → usar git status para encontrar archivos cambiados
   - Usar git ls-files, comandos find y patrones glob para resolver descripciones
4. Preparar los archivos resueltos:
   - **Modo selectivo**: Usar `git add <archivos-resueltos>` para archivos interpretados
   - **Modo todos los cambios**: Usar `git add .` si no se proporciona descripción de archivos
4. Si no se proporciona mensaje de confirmación:
   a. Ejecutar `git status --porcelain` para obtener vista general de archivos cambiados
   b. Ejecutar `git diff` y `git diff --cached` para analizar cambios reales
   c. Analizar los cambios para determinar:
      - Tipo de trabajo (nuevas funcionalidades, correcciones de errores, configuración, documentación, etc.)
      - Ámbito de los cambios (qué partes del proyecto se ven afectadas)
      - Modificaciones clave realizadas
   d. Generar un mensaje de confirmación descriptivo en formato: "acción: descripción breve"
      - Usar verbos de acción como: add, update, fix, remove, refactor, docs, config, feat
      - Mantener el mensaje conciso pero descriptivo (50 caracteres o menos para la primera línea)
      - Incluir detalles adicionales en el cuerpo si los cambios son complejos
5. Ejecutar `git commit -m "<mensaje-confirmación>"` con el mensaje proporcionado o generado
6. Mostrar confirmación del commit con hash y resumen
7. Gestionar casos en los que no hay cambios que confirmar
8. **Validación para modo selectivo**:
   - Verificar que los archivos especificados existen y tienen cambios
   - Mostrar advertencia si los archivos no existen o no tienen modificaciones
   - Mostrar resumen de qué archivos se están guardando vs. qué queda sin preparar

## Ejemplos de Mensajes de Confirmación Generados Automáticamente

El comando analiza los cambios y crea mensajes como:
- `feat: add user authentication system`
- `fix: resolve login validation bug`
- `docs: update API documentation`
- `config: setup project build tools`
- `refactor: improve database connection handling`

## Ejemplos

### Guardar Todos los Cambios
```bash
/vcs:guardar -m "Añadida nueva funcionalidad para autenticación de usuarios"
```
Guarda todos los cambios con el mensaje de confirmación proporcionado.

```bash
/vcs:guardar
```
Guarda todos los cambios con mensaje de confirmación generado automáticamente.

### Guardar Archivos con Descripciones en Lenguaje Natural
```bash
/vcs:guardar "todos los archivos JavaScript" -m "Corregir errores de autenticación"
```
Encuentra y guarda todos los archivos .js con mensaje personalizado.

```bash
/vcs:guardar "archivos en la carpeta src"
```
Guarda todos los archivos en el directorio src/ con mensaje generado automáticamente.

```bash
/vcs:guardar "archivos de configuración" -m "Actualizar endpoints de API"
```
Guarda archivos de configuración (*.json, *.yml, *.config.*) con mensaje personalizado.

```bash
/vcs:guardar "archivos de prueba y documentación"
```
Guarda archivos de prueba (*test*, *spec*) y documentación (*.md) con mensaje generado automáticamente.

### Guardar Archivos Específicos
```bash
/vcs:guardar "src/auth.js README.md" -m "Corregir validación de inicio de sesión"
```
Guarda archivos exactos con mensaje personalizado.

```bash
/vcs:guardar "package.json yarn.lock"
```
Guarda archivos de dependencias con mensaje generado automáticamente.

### Ejemplos Avanzados
```bash
/vcs:guardar "todos los archivos modificados en la carpeta components"
```
Guarda solo los archivos cambiados en el directorio components/.

```bash
/vcs:guardar "archivos Python que fueron modificados hoy"
```
Guarda archivos .py modificados recientemente.

## Resumen del Comportamiento

**Modo todos los cambios** (predeterminado):
- Preparar todos los cambios actuales
- Analizar todos los cambios si no se proporciona mensaje y generar mensaje de confirmación inteligente
- Crear confirmación con mensaje proporcionado o generado
- Mostrar confirmación con detalles del commit

**Modo selectivo** (con parámetros de archivo):
- Validar que los archivos especificados existen y tienen cambios
- Preparar solo los archivos especificados
- Analizar solo los cambios preparados para generación de mensaje
- Mostrar resumen de qué se está confirmando vs. qué queda sin preparar
- Crear confirmación con mensaje proporcionado o generado enfocado en los archivos seleccionados
