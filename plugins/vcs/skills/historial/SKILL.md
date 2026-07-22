---
name: historial
description: Muestra el historial de commits del repositorio en formato fácil de usar
argument-hint: "[número-de-commits]"
allowed-tools: Bash(git log:*) Bash(git rev-parse:*)
---

# VCS Historial - Mostrar Historial de Commits

Muestra el historial de commits del repositorio en un formato fácil de usar.

**Uso**: `/vcs:historial [número-de-commits]`

## Implementación

Muestra el historial de commits usando `git log` con formato optimizado para personas no técnicas. Muestra los commits en un formato claro y legible con información esencial.

Pasos a ejecutar:
1. Comprobar si estamos en un repositorio git
2. Usar `git log` con formato personalizado para mostrar:
   - Hash del commit (versión corta)
   - Fecha del commit
   - Nombre del autor
   - Mensaje del commit
3. Limitar al número de commits indicado en `$ARGUMENTS` (predeterminado: 10)
4. Formatear la salida de forma limpia y legible con saltos de línea apropiados entre commits
5. Usar un formato visual claro que separe cada entrada de commit con líneas en blanco
6. Incluir espaciado y formato apropiados para legibilidad en pantalla de terminal

## Ejemplos

```bash
/vcs:historial
/vcs:historial 5
/vcs:historial 20
```

Esto hará:
- Mostrar los últimos 10 commits (o el número especificado)
- Mostrar cada commit con hash, fecha, autor y mensaje
- Formatear la salida para lectura fácil con saltos de línea apropiados
- Incluir líneas en blanco entre commits para mejor separación visual
- Usar formato consistente que sea fácil de escanear en salida de terminal

## Formato de Salida

Cada commit debe mostrarse con:
- Espaciado de línea apropiado entre entradas
- Separación visual clara usando líneas en blanco
- Sangría y formato consistentes
- Estructura fácil de leer que evite visualización de texto comprimido

Ejemplo de formato de salida:
```
📋 **Historial del Repositorio** (Últimos 10 commits)

**abc123** - *2025-09-10* por **Autor**
mensaje del commit aquí

**def456** - *2025-09-10* por **Autor**
otro mensaje de commit

**ghi789** - *2025-09-10* por **Autor**
tercer mensaje de commit
```
