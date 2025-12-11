# VCS Iniciar - Inicializar Sistema de Control de Versiones

Inicializa un nuevo repositorio de control de versiones en el directorio actual.

**Uso**: `/vcs:iniciar`

## Implementación

Inicializa un repositorio git en el directorio actual usando `git init`. Este comando proporciona una interfaz simplificada para que usuarios no técnicos puedan comenzar a utilizar control de versiones en su proyecto.

Pasos a ejecutar:
1. Ejecutar `git init` en el directorio actual
2. Crear un archivo .gitignore inicial con exclusiones comunes si no existe
3. Confirmar la inicialización exitosa
4. Proporcionar orientación sobre los siguientes pasos

## Ejemplos

```bash
/vcs:iniciar
```

Esto hará lo siguiente:
- Inicializar un nuevo repositorio git
- Crear un archivo .gitignore básico si es necesario
- Mostrar mensaje de confirmación con los siguientes pasos
