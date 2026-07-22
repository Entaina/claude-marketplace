# Product Dev Plugin

Plugin para gestionar el ciclo de vida completo de desarrollo de features en Claude Code.

## Descripción

Este plugin proporciona un workflow estructurado para:

1. **Crear y gestionar features** con IDs únicos y metadata
2. **Generar PRDs** (Product Requirements Documents) automáticamente
3. **Dividir en tareas** (user stories) con criterios de aceptación
4. **Planificar implementación** con análisis de código existente
5. **Implementar tareas** siguiendo el plan paso a paso

## Instalación

### Opción 1: Plugin local

```bash
claude --plugin-dir /path/to/product-dev
```

### Opción 2: En proyecto

Copia la carpeta `product-dev` a `.claude-plugin/` de tu proyecto.

## Comandos

| Comando | Descripción | Uso |
|---------|-------------|-----|
| `/product-dev:feature` | Listar features o crear uno nuevo | `/product-dev:feature` o `/product-dev:feature "descripción"` |
| `/product-dev:prd` | Generar PRD para un feature | `/product-dev:prd {feature_id}` |
| `/product-dev:tasks` | Generar user stories desde PRD | `/product-dev:tasks {feature_id}` |
| `/product-dev:plan` | Crear plan de implementación | `/product-dev:plan {task_path}` |
| `/product-dev:code` | Implementar tarea con el plan | `/product-dev:code {task_path}` |

## Flujo de Trabajo

```
/product-dev:feature "Mi nueva funcionalidad"
    ↓
/product-dev:prd 2025-12-20-143052-mi-funcionalidad
    ↓
/product-dev:tasks 2025-12-20-143052-mi-funcionalidad
    ↓
/product-dev:plan features/2025-12-20-143052-mi-funcionalidad/tasks/001-setup
    ↓
/product-dev:code features/2025-12-20-143052-mi-funcionalidad/tasks/001-setup
```

## Estructura de Archivos

El plugin crea esta estructura en tu proyecto:

```
features/
└── {YYYY-MM-DD-hhmmss}-{slug}/
    ├── feature.json          # Metadata
    ├── prd.md                 # PRD
    └── tasks/
        └── {NNN}-{slug}/
            ├── user-story.md  # Historia de usuario
            └── plan.md        # Plan de implementación
```

## Principios

### Fuente Única de Verdad
- Cada PRD es único, sin duplicar requisitos
- Referencias en vez de copias

### Independencia de Tareas
- Una funcionalidad por tarea
- Máximo 5 criterios de aceptación
- Dependencias explícitas

### Responsabilidad Única
- Un componente por responsabilidad
- Reutilizar código existente

## Skill Incluida

El plugin incluye una skill que se activa automáticamente cuando trabajas con features, proporcionando contexto sobre el workflow y mejores prácticas.

## Requisitos

- Claude Code CLI
- Proyecto con estructura de carpetas estándar

## Licencia

MIT
