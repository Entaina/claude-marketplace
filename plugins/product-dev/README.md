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
| `/feature` | Listar features o crear uno nuevo | `/feature` o `/feature "descripción"` |
| `/prd` | Generar PRD para un feature | `/prd {feature_id}` |
| `/tasks` | Generar user stories desde PRD | `/tasks {feature_id}` |
| `/plan` | Crear plan de implementación | `/plan {task_path}` |
| `/code` | Implementar tarea con el plan | `/code {task_path}` |

## Flujo de Trabajo

```
/feature "Mi nueva funcionalidad"
    ↓
/prd 2025-12-20-143052-mi-funcionalidad
    ↓
/tasks 2025-12-20-143052-mi-funcionalidad
    ↓
/plan features/2025-12-20-143052-mi-funcionalidad/tasks/001-setup
    ↓
/code features/2025-12-20-143052-mi-funcionalidad/tasks/001-setup
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
