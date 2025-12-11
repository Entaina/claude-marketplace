# SW30 - Version Control System Plugin

Spanish-language Git commands designed for non-technical users. Simplifies version control with natural language file selection and auto-generated commit messages.

## Installation

```bash
/plugin marketplace add entaina/claude-marketplace
/plugin install sw30@entaina
```

## Commands

| Command | Description |
|---------|-------------|
| `/vcs:ayuda` | Display help for all VCS commands |
| `/vcs:iniciar` | Initialize version control in current directory |
| `/vcs:guardar` | Save changes with optional message or auto-generate |
| `/vcs:cargar` | Restore a previous version |
| `/vcs:historial` | View commit history |
| `/vcs:diferencias` | Show pending changes with impact analysis |
| `/vcs:etiquetar` | Create version tags for milestones |
| `/vcs:limpiar` | Discard uncommitted changes |

## Usage Examples

### Initialize a project
```bash
/vcs:iniciar
```

### Save all changes with auto-generated message
```bash
/vcs:guardar
```

### Save specific files with custom message
```bash
/vcs:guardar "archivos JavaScript" -m "Corregir errores de autenticación"
```

### View what changed
```bash
/vcs:diferencias
```

### View history
```bash
/vcs:historial
/vcs:historial 20
```

### Create a version tag
```bash
/vcs:etiquetar "versión 1.0"
```

### Restore a previous version
```bash
/vcs:cargar abc123f
/vcs:cargar "versión-1-0"
```

### Discard all changes
```bash
/vcs:limpiar
```

## Features

- **Natural Language File Selection**: Use descriptions like "all JavaScript files" or "files in src folder"
- **Auto-Generated Commit Messages**: Analyzes changes and creates semantic commit messages
- **Safety Confirmations**: Destructive operations require explicit "yes" confirmation
- **Non-Technical Language**: All output uses clear, jargon-free Spanish

## License

MIT
