---
name: feature-workflow
description: "Conocimiento sobre gestión de features, PRDs, user stories, planificación e implementación. Se activa cuando el usuario trabaja con features, menciona PRD, tareas, planificación de implementación, o usa comandos como /product-dev:feature, /product-dev:prd, /product-dev:tasks, /product-dev:plan, /product-dev:code."
user-invocable: false
---

# Gestión del Ciclo de Vida de Features

Guía el proceso completo de desarrollo de features desde la concepción hasta la implementación.

## Flujo del Workflow

```
/product-dev:feature → :prd → :tasks → :plan → :code
        ↓               ↓       ↓        ↓       ↓
      Crear          Generar  Dividir  Planear  Implementar
      Feature          PRD   en Tareas  Tarea     Tarea
```

## Estructura de Archivos

```
features/
└── {YYYY-MM-DD-hhmmss}-{slug}/
    ├── feature.json          # Metadata del feature
    ├── prd.md                 # Product Requirements Document
    └── tasks/
        └── {NNN}-{slug}/
            ├── user-story.md  # Historia de usuario
            └── plan.md        # Plan de implementación
```

## Estados del Feature

| Estado | Descripción | Siguiente Paso |
|--------|-------------|----------------|
| `created` | Feature recién creado | `/product-dev:prd {id}` |
| `prd_created` | PRD generado | `/product-dev:tasks {id}` |
| `tasks_created` | Tareas generadas | `/product-dev:plan {task_path}` |
| `in_progress` | Alguna tarea en progreso | `/product-dev:code {task_path}` |
| `completed` | Todas las tareas completadas | Revisar y crear PR |

## Estados de las Tareas

| Estado | Descripción | Siguiente Paso |
|--------|-------------|----------------|
| `defined` | User story creada | `/product-dev:plan {task_path}` |
| `planned` | Plan generado | `/product-dev:code {task_path}` |
| `in_progress` | Implementación iniciada | `/product-dev:code {task_path}` |
| `completed` | Tarea finalizada | Siguiente tarea |

## Principios Clave

### 1. Fuente Única de Verdad (PRD)
- No duplicar requisitos entre PRDs
- Referenciar en vez de copiar
- Documentar solapamientos explícitamente

### 2. Independencia de Tareas
- Una funcionalidad por tarea
- Máximo 5 criterios de aceptación
- Dependencias explícitas

### 3. Responsabilidad Única (Plan)
- Un componente por responsabilidad
- Reutilizar código existente
- No duplicar lógica

## Formato de IDs

- **Feature ID**: `{YYYY-MM-DD-hhmmss}-{slug}`
  - Ejemplo: `2025-12-19-143052-crm-rails-postgres`

- **Task ID**: `{NNN}-{slug}`
  - Ejemplo: `001-crear-modelo-usuario`

## Detección de Conflictos

Al crear tareas o planes, verificar:

1. **Conflictos de archivo**: Otras tareas modificando los mismos archivos
2. **Conflictos de schema**: Migraciones que podrían conflicturar
3. **Conflictos de rutas**: URLs que se solapan
4. **Dependencias circulares**: A depende de B, B depende de A

## Priorización de Tareas

| Prioridad | Tipo | Ejemplo |
|-----------|------|---------|
| **P1** | Fundamentos | Modelos base, setup |
| **P2** | Core | CRUD principal |
| **P3** | Mejoras | Validaciones extra |
| **P4** | Opcional | UX improvements |

## Buenas Prácticas

### Al Crear Features
- Verificar solapamiento con features existentes
- Títulos claros y descriptivos
- Descripciones completas del problema a resolver

### Al Generar PRDs
- Leer CLAUDE.md primero
- Analizar código existente
- Requisitos específicos y verificables
- Alcance claramente delimitado

### Al Dividir en Tareas
- Una tarea por requisito funcional
- Ordenar por dependencias
- Criterios de aceptación testeables

### Al Planificar
- Buscar implementaciones similares
- Crear matriz de impacto
- Incluir refactorización si hay violaciones

### Al Implementar
- Seguir el plan estrictamente
- Tests junto con código
- Validar antes de marcar completado

## Comandos Disponibles

| Comando | Propósito | Argumento |
|---------|-----------|-----------|
| `/product-dev:feature` | Listar o crear features | `[descripción]` |
| `/product-dev:prd` | Generar PRD | `{feature_id}` |
| `/product-dev:tasks` | Generar user stories | `{feature_id}` |
| `/product-dev:plan` | Crear plan de implementación | `{task_path}` |
| `/product-dev:code` | Implementar tarea | `{task_path}` |

## Solución de Problemas

### "Feature no encontrado"
```bash
# Listar features existentes
ls features/*/feature.json
```

### "PRD no encontrado"
```bash
# Verificar que existe
cat features/{id}/prd.md
# Si no existe
/product-dev:prd {id}
```

### "Tarea no encontrada"
```bash
# Listar tareas del feature
ls features/{id}/tasks/*/user-story.md
```

### "Dependencia no completada"
1. Verificar estado en `feature.json`
2. Completar dependencias primero
3. Ejecutar `/product-dev:code` en orden
