# SW30 - Utilidades para el Curso Software 3.0

Conjunto de utilidades para el curso de Software 3.0 de [Entaina](https://entaina.ai). Incluye comandos en español diseñados para usuarios no técnicos que simplifican operaciones comunes de desarrollo.

## Instalación

```bash
/plugin marketplace add entaina/claude-marketplace
/plugin install sw30@entaina
```

## Comandos

### Desarrollo de Features

Flujo completo para desarrollar funcionalidades de forma estructurada:

| Comando | Descripción |
|---------|-------------|
| `/feature` | Listar features existentes o crear uno nuevo |
| `/prd` | Crear documento de requisitos (PRD) para un feature |
| `/tasks` | Generar tareas (historias de usuario) a partir del PRD |
| `/plan` | Crear plan de implementación para una tarea |
| `/code` | Implementar una tarea siguiendo su plan |

### Control de Versiones (VCS)

| Comando | Descripción |
|---------|-------------|
| `/vcs:ayuda` | Muestra ayuda de todos los comandos VCS |
| `/vcs:iniciar` | Inicializa control de versiones en el directorio actual |
| `/vcs:guardar` | Guarda cambios con mensaje automático o personalizado |
| `/vcs:cargar` | Restaura una versión anterior |
| `/vcs:historial` | Ver historial de commits |
| `/vcs:diferencias` | Muestra cambios pendientes con análisis de impacto |
| `/vcs:etiquetar` | Crea etiquetas de versión para hitos |
| `/vcs:limpiar` | Descarta cambios no confirmados |

## Ejemplos de Uso

### Flujo de Desarrollo de Features

El flujo típico para desarrollar una nueva funcionalidad:

```bash
# 1. Crear un nuevo feature
/feature "Sistema de comentarios para artículos del blog"

# 2. Generar el documento de requisitos
/prd 2025-12-19-143052-comentarios-blog

# 3. Crear las tareas (historias de usuario)
/tasks 2025-12-19-143052-comentarios-blog

# 4. Planificar la primera tarea
/plan features/2025-12-19-143052-comentarios-blog/tasks/001-crear-comentario

# 5. Implementar la tarea
/code features/2025-12-19-143052-comentarios-blog/tasks/001-crear-comentario
```

### Ver features y trabajo pendiente

```bash
# Listar todos los features y ver siguiente acción recomendada
/feature
```

### Control de Versiones

#### Iniciar un proyecto
```bash
/vcs:iniciar
```

#### Guardar todos los cambios con mensaje automático
```bash
/vcs:guardar
```

#### Guardar archivos específicos con mensaje personalizado
```bash
/vcs:guardar "archivos JavaScript" -m "Corregir errores de autenticación"
```

#### Ver qué ha cambiado
```bash
/vcs:diferencias
```

#### Ver historial
```bash
/vcs:historial
/vcs:historial 20
```

#### Crear una etiqueta de versión
```bash
/vcs:etiquetar "versión 1.0"
```

#### Restaurar una versión anterior
```bash
/vcs:cargar abc123f
/vcs:cargar "versión-1-0"
```

#### Descartar todos los cambios
```bash
/vcs:limpiar
```

## Características

### Desarrollo de Features
- **Flujo Estructurado**: Desde idea hasta implementación con PRD, tareas y planes
- **Gestión de Progreso**: Seguimiento automático del estado de cada tarea
- **Detección de Conflictos**: Identifica solapamientos entre features y tareas
- **Principio de Responsabilidad Única**: Cada tarea se enfoca en una sola funcionalidad

### Control de Versiones
- **Selección de Archivos en Lenguaje Natural**: Usa descripciones como "todos los archivos JavaScript" o "archivos en la carpeta src"
- **Mensajes de Commit Automáticos**: Analiza los cambios y crea mensajes semánticos
- **Confirmaciones de Seguridad**: Las operaciones destructivas requieren confirmación explícita
- **Lenguaje No Técnico**: Toda la salida usa español claro y sin jerga técnica

## Licencia

MIT
