---
name: diferencias
description: Muestra cambios pendientes con resumen inteligente de impacto en el proyecto
allowed-tools: Bash(git status:*) Bash(git diff:*) Bash(git rev-parse:*)
---

# VCS Diferencias - Mostrar Cambios Pendientes

Muestra todos los cambios actuales que están pendientes de ser confirmados, con un resumen inteligente de lo que significan los cambios para tu proyecto.

**Uso**: `/vcs:diferencias`

## Implementación

Muestra todos los cambios en el directorio de trabajo y el área de preparación con un resumen significativo para usuarios no técnicos. Este comando analiza los cambios y explica su impacto en lenguaje claro.

Pasos a ejecutar:
1. Comprobar si estamos en un repositorio git
2. Ejecutar `git status --porcelain` para obtener una visión general de los archivos cambiados
3. Ejecutar `git diff` y `git diff --cached` para analizar los cambios reales
4. Analizar los cambios para entender:
   - Qué tipo de trabajo se está realizando (nuevas funcionalidades, correcciones de errores, cambios de configuración, etc.)
   - Qué partes del proyecto se ven afectadas
   - El alcance e impacto de los cambios
5. Presentar un resumen fácil de usar con formato apropiado incluyendo:
   - **Resumen de Impacto del Proyecto**: Qué significan estos cambios para el proyecto en lenguaje claro
   - **Resumen del Trabajo**: Qué tipo de trabajo se ha realizado
   - **Archivos Afectados**: Lista de archivos cambiados con explicaciones breves
   - **Evaluación de Preparación**: Si los cambios están listos para ser guardados
6. Evitar jerga técnica y centrarse en el significado práctico de los cambios
7. Asegurar saltos de línea y espaciado apropiados entre todas las secciones para legibilidad
8. Usar separadores visuales claros (como `---`) entre secciones principales
9. Formatear la salida con espaciado consistente y encabezados de sección claros

## Ejemplos

```bash
/vcs:diferencias
```

Esto mostrará:
- **"Has estado trabajando en..."** - Un resumen de lo que logran los cambios
- **"Estos cambios afectan a..."** - Qué partes de tu proyecto se ven impactadas
- **"¿Listo para guardar?"** - Si los cambios forman una unidad de trabajo completa
- Explicaciones claras y no técnicas de lo que hace cada cambio de archivo

Ejemplo de salida:
```
# 📋 Resumen de Cambios del Proyecto

## Has estado trabajando en:
**Configuración del proyecto y herramientas de desarrollo** - Mejorando la base del proyecto

## Estos cambios afectan a:
**Base del proyecto y flujo de trabajo de desarrollo** - Archivos principales de configuración del proyecto

---

## Resumen del Trabajo:
- **Archivos de configuración** - Añadida mejor configuración de gestión del proyecto
- **Herramientas de desarrollo** - Configurados ajustes del editor para consistencia
- **Estructura del proyecto** - Creado marco de colaboración en equipo organizado

## Archivos Listos para Guardar:

**📄 `.gitignore`** - Reglas de Ignorar de Git
- **Qué cambió**: Añadidos patrones de exclusión para archivos de desarrollo
- **Por qué importa**: Previene que archivos no deseados sean rastreados
- **Impacto**: Repositorio más limpio con solo archivos relevantes

**📄 `package.json`** - Configuración del Proyecto
- **Qué cambió**: Definidas dependencias del proyecto y scripts de construcción
- **Por qué importa**: Establece la estructura y herramientas del proyecto
- **Impacto**: Habilita entorno de desarrollo consistente

**📄 `.vscode/settings.json`** - Configuración del Editor
- **Qué cambió**: Configurado el editor para formato consistente
- **Por qué importa**: Asegura que todos los miembros del equipo usen el mismo estilo de código
- **Impacto**: Mejorada calidad de código y colaboración

---

## ✅ Evaluación de Preparación:
**Listo para guardar**: Estos cambios forman una configuración completa que está lista para confirmar.

**Recomendación**: Usa `vcs:guardar` para preservar esta configuración base del proyecto.
```
