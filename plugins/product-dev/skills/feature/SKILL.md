---
name: feature
description: Gestionar features - crear nuevos, listar existentes, o continuar trabajo pendiente
argument-hint: "[descripción del feature a crear]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Feature Management

Gestiona features del proyecto: crea nuevos, lista existentes, o detecta automáticamente el trabajo pendiente.

**Input:** $ARGUMENTS (opcional - descripción del feature a crear)

## Comportamiento

### Sin argumentos → Listar y Recomendar

1. Buscar `features/*/feature.json`
2. Mostrar cada feature con: ID, título, estado, progreso, lista de tareas
3. **Detectar siguiente acción** para features en progreso:

| Task Status | Siguiente Comando |
|-------------|-------------------|
| `defined` | `/product-dev:plan {task_path}` |
| `planned` | `/product-dev:code {task_path}` |
| `in_progress` | `/product-dev:code {task_path}` |

Buscar la primera tarea no completada (ordenadas por priority) y recomendar el comando apropiado.

**Ejemplo de salida:**
```
FEATURES DEL PROYECTO
=====================

ID: 2025-12-19-175523-crm-rails-tailwind-postgresql
Título: CRM con Rails, Tailwind y PostgreSQL
Estado: in_progress
Progreso: [███████░░░░░░░░░] 43% (3/7 tareas)

  Tareas:
  ✓ 001 - Setup del Proyecto
  ✓ 002 - CRUD de Empresas
  ✓ 003 - CRUD de Contactos
  ○ 004 - CRUD de Oportunidades (planned)    ← PRIMERA PENDIENTE
  ○ 005 - Dashboard con Metricas (defined)
  ○ 006 - Busqueda (defined)
  ○ 007 - Vista Pipeline (defined)

═══════════════════════════════════════════════════════════════
📍 SIGUIENTE ACCIÓN:

/product-dev:code features/.../tasks/004-crud-oportunidades
═══════════════════════════════════════════════════════════════


```

Si no hay features:
```
No hay features creados todavía.

Para crear uno nuevo:
/product-dev:feature "Descripción de lo que quieres construir..."
```

### Con descripción → Crear Feature

1. **Verificar solapamiento** con features existentes (revisar títulos, descripciones, PRDs)
   - Si hay solapamiento potencial, alertar y pedir confirmación
2. **Generar ID**: `{YYYY-MM-DD-hhmmss}-{slug}`
   - Slug: palabras clave, lowercase, sin acentos, guiones, max 30 chars
3. **Crear estructura**:
   ```
   features/{id}/
   features/{id}/feature.json
   ```
4. **Crear feature.json**:
   ```json
   {
     "version": "1.0",
     "id": "{id}",
     "title": "{título inferido}",
     "description": "{descripción}",
     "original_request": "{texto exacto del usuario}",
     "created_at": "{ISO timestamp}",
     "updated_at": "{ISO timestamp}",
     "status": "created",
     "progress": 0,
     "current_phase": "initial",
     "tasks": []
   }
   ```

   **IMPORTANTE:** El campo `original_request` debe contener el texto EXACTO que el usuario proporcionó como argumento, sin modificaciones ni interpretaciones. Esto preserva la intención original para referencia futura.

5. **Validar** que se creó correctamente

**Report de creación:**
```
Feature creado exitosamente!

## Metadata
id: `{id}`
created_at: `{timestamp}`

## Detalles
Título: {título}
Ubicación: features/{id}/

## Request Original
> {original_request}

## Análisis de Solapamiento
Features revisados: {N}
Solapamientos detectados: {M}
{lista de solapamientos si hay}

## Siguiente Paso
/product-dev:prd {id}
```
