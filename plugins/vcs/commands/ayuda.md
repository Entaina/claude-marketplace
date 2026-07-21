---
description: Muestra información de ayuda sobre todos los comandos VCS disponibles
---

# VCS Ayuda - Ayuda del Sistema de Control de Versiones

Muestra información útil sobre todos los comandos VCS disponibles.

**Uso**: `/vcs:ayuda`

## Implementación

Muestra una guía de ayuda completa para todos los comandos VCS, diseñada para que personas no técnicas entiendan los conceptos y uso del control de versiones.

Pasos a ejecutar:
1. Mostrar una visión general de qué es el control de versiones
2. Listar todos los comandos VCS disponibles con descripciones
3. Proporcionar ejemplos de flujo de trabajo común
4. Incluir consejos de resolución de problemas
5. Mostrar conceptos de git explicados en términos simples

## Ejemplos

```bash
/vcs:ayuda
```

Esto mostrará:

### Comandos del Sistema de Control de Versiones (VCS)

El control de versiones te ayuda a rastrear cambios en tus archivos a lo largo del tiempo, como tener un historial de guardado para todo tu proyecto.

#### Comandos Disponibles:

- **`/vcs:iniciar`** - Iniciar control de versiones en esta carpeta
- **`/vcs:guardar [descripción-archivos] [-m "mensaje"]`** - Guardar cambios actuales con una descripción (genera mensaje automáticamente si no se proporciona, soporta selección de archivos en lenguaje natural)
- **`/vcs:cargar [commit]`** - Volver a una versión guardada anterior (muestra historial si no se especifica commit)
- **`/vcs:historial [número]`** - Ver todos los guardados anteriores
- **`/vcs:diferencias`** - Ver qué cambios has hecho desde el último guardado
- **`/vcs:etiquetar [mensaje]`** - Marcar hitos importantes (genera marca de tiempo automáticamente si no hay mensaje)
- **`/vcs:limpiar [archivos...]`** - Descartar cambios y volver a estado limpio (puede seleccionar archivos específicos o limpiar todo)
- **`/vcs:ayuda`** - Mostrar esta información de ayuda

#### Flujo de Trabajo Común:

1. **Iniciar un nuevo proyecto**: `/vcs:iniciar`
2. **Hacer cambios en tus archivos**
3. **Comprobar qué cambió**: `/vcs:diferencias` para ver tu progreso
4. **Guardar tu progreso**: `/vcs:guardar "Añadida nueva funcionalidad"` o simplemente `/vcs:guardar` para mensaje generado automáticamente
5. **Guardar archivos específicos**: `/vcs:guardar "archivos JavaScript" -m "Corregir errores"` para confirmaciones selectivas
6. **Continuar trabajando y guardando**: `/vcs:guardar "Corregido error"` o `/vcs:guardar`
7. **Marcar hitos importantes**: `/vcs:etiquetar "versión 1.0"` o `/vcs:etiquetar` para marca de tiempo
8. **Comprobar tu historial**: `/vcs:historial` o `/vcs:cargar` para ver todos los guardados
9. **Volver atrás si es necesario**: `/vcs:cargar abc123f` o `/vcs:cargar versión-1-0`
10. **Descartar cambios no deseados**: `/vcs:limpiar` para empezar de nuevo o `/vcs:limpiar archivo-específico.js`

#### Consejos:

- Guarda frecuentemente con mensajes descriptivos, o deja que el sistema los genere automáticamente
- Usa `/vcs:diferencias` antes de guardar para ver qué cambió y obtener análisis inteligente de impacto
- Guarda archivos específicos usando lenguaje natural: `/vcs:guardar "todos los archivos JavaScript"` o `/vcs:guardar "archivos en carpeta src"`
- Crea etiquetas para hitos importantes como lanzamientos o funcionalidades principales
- Usa `/vcs:cargar` sin parámetros para ver el historial y elegir qué versión cargar
- Los mensajes de confirmación manuales deben describir lo que hiciste
- Los mensajes generados automáticamente analizan tus cambios y crean descripciones apropiadas
- Usa `/vcs:limpiar` para descartar cambios no deseados y empezar de nuevo
- Siempre puedes volver a cualquier guardado o etiqueta anterior

#### Mensajes de Confirmación Generados Automáticamente:

Cuando usas `/vcs:guardar` sin un mensaje, el sistema:
- Analiza qué archivos has cambiado
- Entiende el tipo de trabajo que has realizado
- Genera un mensaje de confirmación profesional como:
  - `feat: add user login functionality`
  - `fix: resolve database connection issue`
  - `docs: update installation guide`
  - `config: setup development environment`
