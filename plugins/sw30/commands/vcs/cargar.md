---
description: Restaura el repositorio a un estado de commit, etiqueta o rama anterior
---

# VCS Cargar - Restaurar Versión Anterior

Restaura el repositorio a un estado de commit, etiqueta o rama anterior.

**Uso**: `/vcs:cargar [hash-commit-o-etiqueta-o-referencia]`

## Implementación

Restablece el repositorio a un commit, etiqueta o rama específica usando `git reset --hard`. Este comando permite a los usuarios restaurar su proyecto a cualquier estado anterior usando varios tipos de referencia.

Pasos a ejecutar:
1. Comprobar si estamos en un repositorio git
2. **Gestionar parámetro de referencia ausente**:
   - Si no se proporciona referencia de commit, mostrar historial de commits usando `git log --oneline --decorate -10`
   - Formatear el historial de forma fácil de usar mostrando:
     - Hash del commit (versión corta)
     - Mensaje del commit
     - Indicador del commit actual
   - Pedir al usuario que especifique qué commit cargar por hash, etiqueta o descripción
   - Esperar entrada del usuario y luego proceder con la referencia especificada
3. Resolver y validar la referencia proporcionada (hash de commit, nombre de etiqueta, rama o descripción):
   - Si parece un hash de commit (comienza con alfanumérico), usar directamente
   - Si coincide con un nombre de etiqueta, resolver al commit etiquetado
   - Si coincide con un nombre de rama, resolver a la cabeza de la rama
   - Si es una referencia relativa (HEAD~1, HEAD^), resolverla
   - Si es una descripción, buscar commits recientes con mensajes coincidentes
4. Comprobar estado actual del repositorio para analizar qué se perderá:
   - Archivos modificados que serán descartados
   - Archivos sin rastrear (estos permanecerán pero pueden entrar en conflicto con el estado objetivo)
   - Cambios preparados que se perderán
5. Mostrar la información del commit objetivo (hash, mensaje, fecha, autor)
6. Mostrar análisis detallado de impacto:
   - Listar archivos modificados con descripciones de cambios
   - Mostrar recuento total de archivos afectados
   - Comparar estado actual con commit objetivo
7. **Pedir confirmación explícita** con advertencia clara sobre pérdida de datos:
   - Mostrar advertencia clara sobre pérdida permanente de datos
   - Requerir que el usuario escriba "yes" o "y" para confirmar (sin distinción de mayúsculas)
   - Mostrar exactamente qué commit están cargando
   - **SIEMPRE pedir confirmación independientemente de si se proporcionaron parámetros**
8. Después de la confirmación:
   - Ejecutar `git reset --hard <referencia-resuelta>`
   - Mostrar confirmación de la operación de reinicio con detalles

## Ejemplos

```bash
/vcs:cargar
```
Mostrar historial de commits y pedir al usuario que seleccione un commit para cargar.

```bash
/vcs:cargar abc123f
```
Cargar commit específico por hash.

```bash
/vcs:cargar version-1-0
```
Cargar versión etiquetada (creada con vcs:etiquetar).

```bash
/vcs:cargar HEAD~1
```
Cargar commit anterior (referencia relativa).

```bash
/vcs:cargar main
```
Cargar cabeza de rama específica.

```bash
/vcs:cargar "add user authentication"
```
Cargar commit buscando coincidencia de descripción.

Esto hará:
- Resolver la referencia a un commit específico (hash, etiqueta, rama o descripción)
- Analizar qué cambios se perderán
- Mostrar vista previa detallada del impacto
- Pedir confirmación explícita antes de proceder
- Restablecer el repositorio a ese commit
- Mostrar confirmación con resumen detallado de la operación

**Tipos de Referencia Soportados**:
- **Hashes de commit**: `abc123f`, `a1b2c3d4e5f6`
- **Etiquetas**: `version-1-0`, `2024-03-15_14-30` (creadas por vcs:etiquetar)
- **Ramas**: `main`, `develop`, `feature-branch`
- **Relativas**: `HEAD~1`, `HEAD~2`, `HEAD^`
- **Descripciones**: Buscar coincidencias en mensajes de commit

## Características de Seguridad

- **Vista previa detallada**: Muestra exactamente qué se perderá antes de cargar
- **Confirmación explícita**: Requiere escribir "yes" para proceder, no solo pulsar Enter
- **Advertencias claras**: Múltiples advertencias sobre pérdida permanente de datos
- **Análisis de impacto**: Compara el estado actual con el commit objetivo
- **Validación de objetivo**: Confirma que el commit objetivo existe y es accesible

## Ejemplos Interactivos

### Cuando no se proporciona referencia de commit:
```
📋 **Historial de Commits Recientes**

e03b3a7 (HEAD -> main) enhance: add selective file operations to VCS commands
1561109 enhance: add destructive operation safeguards to VCS load command
3875df4 feat: add VCS clean command with destructive operation safeguards
ebb367c feat: add VCS tag command and enhance load command functionality
3a5deda docs: enhance VCS diff command formatting and output structure
d92ebbb docs: standardize VCS command naming conventions
106e488 config: expand git permissions for full VCS functionality
ad4c039 feat: initialize Software 3.0 VCS command system

**Por favor, especifica qué commit cargar**:
- Introduce un hash de commit (ej., "1561109")
- Introduce un patrón de mensaje de commit (ej., "add destructive")
- Introduce un nombre de etiqueta (ej., "version-1-0")
- Introduce una referencia relativa (ej., "HEAD~2")

¿Qué commit te gustaría cargar? _
```

### Operación de carga estándar:
```
🔄 **Análisis de Carga del Repositorio**

**Objetivo**: Cargando commit abc123d - "feat: add user authentication system"
**Autor**: John Doe (hace 2 días)

**Estado Actual**: Tu repositorio tiene cambios sin confirmar

**Archivos que serán descartados** (2 modificados):
- `src/main.js` - 8 líneas cambiadas
- `config.json` - Configuración modificada

**Archivos que serán preparados/despreparados**:
- Los cambios actualmente preparados se perderán

---

⚠️  **ADVERTENCIA: ¡Esta acción no se puede deshacer!**
Todos los cambios sin confirmar se perderán permanentemente.
Serás movido al commit: abc123d - "feat: add user authentication system"

**Impacto total**: 2 archivos se verán afectados

Escribe "yes" para proceder con la carga: _
```

Después de la confirmación:
```
✅ **¡Repositorio Cargado Correctamente!**

**Objetivo alcanzado**: abc123d - "feat: add user authentication system"
**Acciones realizadas**:
- Descartadas modificaciones en 2 archivos
- HEAD restablecido al commit objetivo
- El directorio de trabajo ahora coincide exactamente con el objetivo

Tu repositorio está ahora en el estado solicitado.
```

**Advertencia**: Este comando destruye permanentemente el trabajo sin confirmar. Úsalo con extrema precaución y asegúrate de que quieres perder todos los cambios actuales.
