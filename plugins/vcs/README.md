# VCS - Control de Versiones para el Curso Software 3.0

Comandos de control de versiones en español para el curso de Software 3.0 de [Entaina](https://entaina.ai). Diseñados para usuarios no técnicos: simplifican las operaciones de Git con selección de archivos en lenguaje natural y mensajes de confirmación automáticos.

> ¿Buscas el flujo de desarrollo de features (`/feature`, `/prd`, `/tasks`, `/plan`, `/code`)? Está en el plugin [product-dev](../product-dev/).

## Instalación

```bash
/plugin marketplace add entaina/claude-marketplace
/plugin install vcs@entaina
```

## Comandos

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

### Iniciar un proyecto
```bash
/vcs:iniciar
```

### Guardar todos los cambios con mensaje automático
```bash
/vcs:guardar
```

### Guardar archivos específicos con mensaje personalizado
```bash
/vcs:guardar "archivos JavaScript" -m "Corregir errores de autenticación"
```

### Ver qué ha cambiado
```bash
/vcs:diferencias
```

### Ver historial
```bash
/vcs:historial
/vcs:historial 20
```

### Crear una etiqueta de versión
```bash
/vcs:etiquetar "versión 1.0"
```

### Restaurar una versión anterior
```bash
/vcs:cargar abc123f
/vcs:cargar "versión-1-0"
```

### Descartar cambios
```bash
# Descartar todos los cambios sin confirmar
/vcs:limpiar

# Descartar solo archivos concretos
/vcs:limpiar src/app.js
```

## Características

- **Selección de Archivos en Lenguaje Natural**: Usa descripciones como "todos los archivos JavaScript" o "archivos en la carpeta src"
- **Mensajes de Commit Automáticos**: Analiza los cambios y crea mensajes semánticos
- **Confirmaciones de Seguridad**: Las operaciones destructivas requieren confirmación explícita
- **Lenguaje No Técnico**: Toda la salida usa español claro y sin jerga técnica

## Licencia

MIT
