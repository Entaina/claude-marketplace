---
name: plan
description: Crear un plan de implementación para una tarea (Principio de Responsabilidad Única)
argument-hint: "<task_path>"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Crear Plan de Implementación

Genera un plan detallado para implementar una tarea específica siguiendo el **Principio de Responsabilidad Única**. Este plan será ejecutado por `/product-dev:code` para generar la implementación.

## Variables
task_path: $ARGUMENTS           # OBLIGATORIO - Path de la tarea

## Principio: Responsabilidad Única

Cada tarea planificada debe cumplir:

| Aspecto | Requisito |
|---------|-----------|
| **Una Funcionalidad** | Una capacidad por tarea - no agrupar |
| **Auto-contenido** | Sin dependencias de código no commiteado |
| **Trazabilidad** | Nombres claros para vincular a código/tests |
| **Testeable** | Validación pass/fail posible |
| **Reversible** | Puede revertirse sin romper otros componentes |

### Detección de Violaciones de Diseño

**CRÍTICO**: Al analizar el código existente, detectar activamente:

1. **Código Duplicado**: Misma lógica implementada en múltiples lugares
2. **Scope Creep**: Componente que hace más de lo que debería
3. **Ejemplos Redundantes**: Mismos patrones usados inconsistentemente
4. **Conflictos de Responsabilidad**: Múltiples componentes modificando lo mismo

**Si se encuentran violaciones, el plan DEBE incluir tareas de refactorización.**

## Instrucciones

### Fase 1: Localizar y Validar la Tarea

**CRÍTICO**: Antes de planificar, verificar que la tarea existe:

1. Verificar que existe `{task_path}/user-story.md`
2. Si no existe, mostrar error con el path correcto
3. Extraer el feature_id del path (segundo segmento)
4. Cargar `features/{feature_id}/feature.json` para contexto
5. Cargar `features/{feature_id}/prd.md` para requisitos

### Fase 2: Análisis del Feature

Buscar en el codebase para entender el contexto:

1. **Leer `CLAUDE.md`**: Convenciones del proyecto
2. **User Story**: Cargar `{task_path}/user-story.md`
3. **Criterios de Aceptación**: Identificar todos los escenarios
4. **PRD del Feature**: Entender el contexto completo

### Fase 3: Análisis de Código Existente (OBLIGATORIO)

**Para cada componente que podría verse afectado, realizar análisis:**

1. **Buscar implementaciones similares** en el codebase
2. **Identificar patrones** que se deben seguir
3. **Detectar código que necesita modificación** vs creación

**Crear una matriz de impacto:**
```
| Componente | Archivo Existente | Líneas | Impacto |
|------------|-------------------|--------|---------|
| Model | app/models/x.rb | 45-67 | MODIFICAR |
| Controller | app/controllers/y.rb | 12-30 | MODIFICAR |
| View | app/views/z/index.html.erb | N/A | CREAR |
| Test | spec/models/x_spec.rb | 80-95 | EXTENDER |
```

**Si se encuentra código relacionado:**
- Documentar qué existe
- Explicar cómo se reutilizará o modificará
- NO duplicar lógica existente

### Fase 4: Detección de Conflictos (OBLIGATORIO)

Verificar conflictos potenciales:

1. **Conflictos de Archivo**: Otras tareas pendientes modificando los mismos archivos
2. **Conflictos de Schema**: Migraciones que podrían conflicturar
3. **Conflictos de Rutas**: Patrones de URL que se solapan
4. **Conflictos de Tests**: Fixtures o datos de test compartidos

**Crear matriz de conflictos:**
```
| Tipo | Recurso | Otra Tarea | Resolución |
|------|---------|------------|------------|
| Archivo | users_controller.rb | task-002 | Secuenciar |
| Schema | add_column :users | task-003 | Combinar migración |
```

**Si se encuentran conflictos:**
- Documentar en el plan
- Sugerir orden de resolución
- Marcar dependencias bloqueantes

### Fase 5: Evaluación de Atomicidad

Determinar si esta tarea debe ser:
- Ejecutada como unidad única
- Dividida en sub-tareas más pequeñas
- Combinada con otra tarea relacionada

Aplicar el principio de **Responsabilidad Única**: si la tarea tiene sub-funcionalidades que pueden entenderse independientemente, considerar dividirla.

### Fase 6: Generar el Plan

Escribir el plan en `{task_path}/plan.md`

Usar el siguiente formato, reemplazando todos los placeholders con contenido real:

## Formato del Plan

```markdown
# Plan: {Título de la tarea}

## Metadata
task_path: `{task_path}`
feature_id: `{feature_id}`
created_at: `{timestamp}`
status: `planned`

## Análisis de Código Existente

### Búsqueda Realizada
<Lista de archivos y patrones encontrados relacionados con esta tarea>

### Matriz de Impacto (OBLIGATORIO)

| Componente | Archivo Existente | Líneas | Impacto |
|------------|-------------------|--------|---------|
| <componente 1> | <archivo> | <líneas> | CREAR/MODIFICAR/EXTENDER |
| <componente 2> | <archivo> | <líneas> | CREAR/MODIFICAR/EXTENDER |

**Archivos Nuevos Requeridos**: <count>
**Archivos a Modificar**: <count>

### Evaluación de Patrones

<Describir patrones encontrados y cómo se seguirán:
- Convenciones de naming
- Estructura de archivos
- Patrones de diseño en uso>

### Matriz de Conflictos

| Tipo | Recurso | Otra Tarea | Resolución |
|------|---------|------------|------------|
| <tipo> | <recurso> | <tarea> | <resolución> |

**Conflictos Encontrados**: <count> (Si > 0, documentar resolución)

## Resumen
{Descripción clara de qué se va a implementar y cómo}

## Historia de Usuario
**Como** {tipo de usuario}
**Quiero** {acción}
**Para** {beneficio}

## Archivos a Modificar
- `{ruta/archivo1.rb}` - {razón de la modificación}
- `{ruta/archivo2.rb}` - {razón de la modificación}

## Archivos a Crear
- `{ruta/nuevo1.rb}` - {propósito del archivo}
- `{ruta/nuevo2.rb}` - {propósito del archivo}

## Plan de Implementación

### Fase 1: Fundamentos
{Trabajo base necesario antes de la funcionalidad principal}

### Fase 2: Implementación Principal
{El núcleo de la funcionalidad}

### Fase 3: Integración
{Cómo se conecta con el resto del sistema}

## Pasos de Implementación

IMPORTANTE: Ejecutar cada paso en orden.

### 0. Refactorización Previa (SI SE ENCONTRARON VIOLACIONES)

**Saltar esta sección si no se encontraron violaciones de diseño**

Para cada violación detectada:

#### Violación 1: <descripción>
- **Archivo fuente**: <archivo>:<líneas> - Acción: <MANTENER|ELIMINAR|MODIFICAR>
- **Cambios específicos**:
  - [ ] Eliminar líneas X-Y de <archivo>
  - [ ] Mover lógica a <nuevo_archivo>
  - [ ] Actualizar referencias

### 1. {Nombre del paso}
- {Subtarea detallada}
- {Subtarea detallada}
- {Comando o acción específica si aplica}

### 2. {Nombre del paso}
- {Subtarea detallada}
- {Subtarea detallada}

### 3. {Nombre del paso - Tests}
- Crear tests para {funcionalidad}
- Verificar criterios de aceptación

### 4. Validación Final
- Ejecutar comandos de validación
- Verificar que todos los tests pasan

## Criterios de Aceptación
- [ ] {Criterio 1 del user-story}
- [ ] {Criterio 2 del user-story}
- [ ] {Criterio 3 del user-story}

## Comandos de Validación

```bash
# Verificar que el plan tiene todas las secciones requeridas
test -f {task_path}/plan.md

# Ejecutar tests
bin/rspec

# Verificar formato
bundle exec standard

# Verificar templates ERB
bundle exec erblint --lint-all

# Compilar assets
yarn build
```

### Comandos de Verificación de Archivos
```bash
# Verificar que todos los archivos referenciados existen
for file in $(grep -oP '`[^`]+\.(rb|erb|js|ts)`' {task_path}/plan.md | tr -d '`'); do
  test -f "$file" && echo "✓ $file" || echo "✗ $file NO ENCONTRADO"
done
```

## Notas
{Consideraciones adicionales, advertencias, o decisiones de diseño}
```

### Fase 7: Actualizar Estado de la Tarea

1. Cargar `features/{feature_id}/feature.json`
2. Encontrar la tarea en el array `tasks`
3. Cambiar `status` a `"planned"`
4. Actualizar `updated_at` del feature
5. Guardar el archivo

### Fase 8: Validar el Plan Creado

Ejecutar validaciones:

```bash
# Verificar que el plan existe
test -f {task_path}/plan.md

# Verificar secciones obligatorias
grep -q "## Metadata" {task_path}/plan.md
grep -q "## Matriz de Impacto" {task_path}/plan.md
grep -q "## Pasos de Implementación" {task_path}/plan.md
grep -q "## Criterios de Aceptación" {task_path}/plan.md

# Verificar que los archivos referenciados son válidos
grep -oP '`app/[^`]+`' {task_path}/plan.md | while read file; do
  test -e "${file//\`/}" || echo "WARNING: $file no existe"
done
```

## Report

Al finalizar, mostrar:

```
✅ Plan creado: {task_path}/plan.md

📋 Siguiente paso:
   Ejecuta /product-dev:code {task_path} para implementar este plan
```

## Consideraciones

- El plan debe ser lo suficientemente detallado para ejecutarse sin ambigüedad
- Seguir las convenciones y patrones existentes en el proyecto
- Incluir tests desde el principio (TDD cuando sea apropiado)
- Los comandos de validación deben ejecutarse sin errores al finalizar
- Documentar cualquier conflicto o dependencia encontrada
- NO duplicar lógica existente - reutilizar siempre que sea posible
