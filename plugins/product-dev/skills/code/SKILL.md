---
name: code
description: Implementar una tarea siguiendo su plan
argument-hint: "<task_path>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Implementar Tarea

Ejecuta el plan de implementación de una tarea.

## Variables
task_path: $ARGUMENTS

## Instrucciones

### Fase 1: Validar Prerrequisitos

1. **Leer el plan**
   - Cargar `{task_path}/plan.md`
   - Si no existe, sugerir `/product-dev:plan {task_path}` primero

2. **Verificar dependencias**
   - Cargar `features/{feature_id}/feature.json`
   - Verificar que todas las tareas en `depends_on` tienen status `completed`
   - Si hay dependencias incompletas, mostrar error y sugerir orden de implementación

### Fase 2: Implementar

1. **Seguir los pasos del plan en orden estricto**
   - Cada paso debe completarse antes de pasar al siguiente
   - Si algo no está claro, preguntar antes de continuar

2. **Aplicar patrones del proyecto**
   - Respetar convenciones de `CLAUDE.md`
   - Seguir la estructura de archivos existente
   - Reutilizar código existente cuando sea posible

3. **Crear tests junto con el código**
   - Tests antes o junto con la implementación
   - Cubrir todos los criterios de aceptación

### Fase 3: Validar

1. **Ejecutar los comandos de validación del plan**
   - Tests
   - Linters
   - Build

2. **Verificar criterios de aceptación**
   - Revisar cada criterio del user-story
   - Marcar como completados en el plan si corresponde

### Fase 4: Actualizar Estado

1. Extraer feature_id del path (segundo segmento)
2. En `features/{feature_id}/feature.json`:
   - Cambiar status de la tarea a `"completed"`
   - Recalcular `progress` del feature: `(completed_tasks / total_tasks) * 100`
   - Actualizar `updated_at`
   - Si todas las tareas están completadas, cambiar `status` del feature a `"completed"`

### Fase 5: Determinar Siguiente Acción

1. **Buscar siguiente tarea pendiente** (por prioridad)
   - Si hay tareas con status `defined` → sugerir `/product-dev:plan {task_path}`
   - Si hay tareas con status `planned` → sugerir `/product-dev:code {task_path}`

2. **Si no hay más tareas** → Feature completado

## Report

Mostrar:

```
Tarea completada exitosamente!

## Trabajo Realizado
- {Resumen del trabajo en bullet points}
- {Archivos creados/modificados}
- {Tests añadidos}

## Cambios
{Output de git diff --stat}

## Progreso del Feature
{Nombre del feature}
[████████████░░░░] {X}% ({N}/{M} tareas)

Tareas:
✓ 001 - {tarea completada}
✓ 002 - {tarea completada}
→ 003 - {esta tarea - recién completada}
○ 004 - {siguiente tarea} ({status})

## Siguiente Paso
/product-dev:plan {siguiente_tarea_path}
```

O si el feature está completo:

```
🎉 Feature completado!

## {Nombre del feature}

Todas las tareas han sido implementadas:
✓ 001 - {tarea}
✓ 002 - {tarea}
✓ 003 - {tarea}

## Estadísticas
- Total de tareas: {N}
- Archivos creados: {X}
- Archivos modificados: {Y}
- Tests añadidos: {Z}

## Recomendación
Revisar los cambios con:
git diff main...HEAD

Crear PR cuando esté listo.
```

## Consideraciones

- Seguir el plan al pie de la letra
- No introducir funcionalidad no especificada
- Mantener commits atómicos y descriptivos
- Ejecutar validaciones antes de marcar como completado
- Si se encuentran problemas, documentarlos y preguntar
