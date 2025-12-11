# VCS Etiquetar - Crear Etiquetas de Versión

Crea una etiqueta para el commit actual para marcar hitos o versiones importantes. Las etiquetas te ayudan a identificar puntos específicos en el historial de tu proyecto que son significativos.

**Uso**: `/vcs:etiquetar [mensaje-etiqueta]`

## Implementación

Crea una etiqueta git en el commit actual con un mensaje proporcionado o una marca de tiempo generada automáticamente. Este comando proporciona una forma fácil de marcar versiones o hitos importantes en tu proyecto.

Pasos a ejecutar:
1. Comprobar si estamos en un repositorio git
2. Verificar que hay commits para etiquetar (el repositorio no está vacío)
3. Si se proporciona un mensaje de etiqueta:
   - Usar el mensaje proporcionado como nombre de la etiqueta (saneado para compatibilidad con git)
   - Eliminar caracteres especiales y espacios, reemplazar con guiones
4. Si no se proporciona mensaje de etiqueta:
   - Generar una marca de tiempo en formato: "AAAA-MM-DD_HH-MM" (usando hora local actual)
   - Usar esta marca de tiempo como nombre de la etiqueta
5. Comprobar si la etiqueta ya existe para evitar conflictos
6. Crear la etiqueta usando `git tag "<nombre-etiqueta>"`
7. Mostrar confirmación con:
   - El nombre de la etiqueta que fue creada
   - El hash del commit y mensaje al que apunta
   - Explicación de lo que representa la etiqueta
   - Instrucciones sobre cómo enviar etiquetas si es necesario

## Reglas de Nomenclatura de Etiquetas

- Convertir espacios a guiones
- Eliminar o reemplazar caracteres especiales que no sean compatibles con git
- Mantener nombres de etiqueta concisos y significativos
- Formato de marca de tiempo: AAAA-MM-DD_HH-MM (ej., "2024-03-15_14-30")

## Ejemplos

```bash
/vcs:etiquetar "versión 1.0"
```
Crea una etiqueta llamada "versión-1-0" apuntando al commit actual.

```bash
/vcs:etiquetar "lanzamiento estable"
```
Crea una etiqueta llamada "lanzamiento-estable" apuntando al commit actual.

```bash
/vcs:etiquetar
```
Crea una etiqueta con marca de tiempo actual (ej., "2024-03-15_14-30") apuntando al commit actual.

Esto hará:
- Crear una etiqueta git ligera en el commit actual
- Usar el mensaje proporcionado (saneado) o generar automáticamente marca de tiempo
- Mostrar confirmación con detalles de la etiqueta e información del commit
- Proporcionar orientación sobre cómo enviar etiquetas al repositorio remoto si es necesario

Ejemplo de salida:
```
✅ **¡Etiqueta Creada Correctamente!**

**Nombre de etiqueta**: versión-1-0
**Apunta al commit**: a1b2c3d - "feat: add user authentication system"
**Creada**: 15 de marzo de 2024 a las 14:30

Esta etiqueta marca: **versión 1.0** - Un hito significativo en tu proyecto

💡 **Consejo**: Para compartir esta etiqueta con otros, usa: `git push origin versión-1-0`
```
