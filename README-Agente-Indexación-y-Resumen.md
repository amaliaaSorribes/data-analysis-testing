# README — Agente de Indexación y Resumen de Documentación

## 1. Objetivo del agente

Este agente tiene como objetivo **preparar la documentación para su uso eficiente con Copilot** y, en una fase posterior, **servir como base para un sistema RAG**, resolviendo el principal problema identificado:  
> la documentación existe, pero no está estructurada ni sintetizada de una forma adecuada para IA.

El agente **no responde preguntas** ni interactúa con usuarios finales.  
Su función es **procesar documentación existente y generar artefactos estructurados** que faciliten:
- navegación,
- comprensión rápida,
- reducción de alucinaciones,
- y reutilización posterior (RAG).

---

## 2. Qué problema resuelve

En entornos corporativos:
- la documentación está acumulada,
- es heterogénea,
- y contiene mucho texto poco accionable.

Esto provoca que:
- Copilot consuma demasiado contexto,
- las respuestas sean inconsistentes,
- o se mezclen documentos contradictorios.

Este agente actúa **antes** de cualquier sistema conversacional, aplicando una capa de **orden, síntesis y gobierno del conocimiento**.

---

## 3. Enfoque general

El agente trabaja en **modo batch (offline)** y sigue estos principios:

- No modifica los documentos originales.
- No unifica todo en un único mega-documento.
- Genera **outputs especializados**, cada uno con un propósito claro.
- Usa formatos simples y estándar (Markdown y JSON).
- Separa claramente:
  - contenido original,
  - metadatos estructurados,
  - y resúmenes.

Este enfoque permite:
- buen funcionamiento con Copilot,
- escalabilidad,
- y transición a RAG sin rehacer trabajo.

---

## 4. Inputs del agente

- Conjunto de documentos en formato Markdown (`.md`).
- Tipos documentales variados (procedimientos, FAQs, comunicados, tickets, etc.).
- Documentación sintética o real, sin necesidad de estructura previa perfecta.

---

## 5. Funcionamiento del agente (alto nivel)

Para cada documento, el agente:

1. **Identifica**
   - Detecta o asigna un `doc_id`.
   - Detecta tipo documental y área funcional.
   - Extrae metadatos básicos.

2. **Clasifica**
   - Por tipo, área y temática.
   - Sin inventar información cuando no hay señal suficiente.

3. **Resume**
   - Genera un resumen estructurado y accionable.
   - Extrae hechos clave, reglas, excepciones y acciones.

4. **Indexa**
   - Registra el documento en un catálogo técnico.
   - Genera índices navegables para humanos y Copilot.

---

## 6. Outputs del agente y por qué son necesarios

El agente genera **tres tipos de outputs**, cada uno con una función distinta.  
No son redundantes: **cada uno resuelve un problema diferente**.

---

### 6.1. `CATALOG.json` — Catálogo técnico de documentos

#### Qué es  
Un archivo **estructurado y orientado a máquina**, que actúa como **fuente de verdad técnica** del repositorio documental.

#### Qué aporta
- IDs únicos y consistentes (`doc_id`).
- Metadatos normalizados (tipo, área, fecha, tags, versión).
- Referencias claras a:
  - documento original
  - resumen generado.

#### Para qué se usa
- Automatización (scripts, pipelines, validaciones).
- Filtrado avanzado (por tipo, vigencia, área).
- Reindexaciones incrementales.
- Preparación para RAG (vectorizar solo lo necesario).
- Escalabilidad a cientos o miles de documentos.

#### Qué NO es
- No es un índice navegable.
- No está pensado para lectura humana ni exploración directa.

---

### 6.2. `INDEX.md` — Índice maestro navegable

#### Qué es  
Un documento **legible y navegable**, pensado para **personas y Copilot**.

#### Qué aporta
- Punto de entrada claro al repositorio.
- Organización visual por:
  - tipo documental,
  - área funcional,
  - temática.
- Enlaces directos a documentos y resúmenes.

#### Para qué se usa
- Navegación humana.
- Ayudar a Copilot a “entender” la estructura del conocimiento.
- Reducir contexto innecesario.
- Facilitar descubrimiento sin conocer IDs.

#### Qué NO es
- No sirve para automatización.
- No es una fuente fiable para procesos técnicos o RAG.

---

### 6.3. `/summaries/*.summary.md` — Resúmenes por documento

#### Qué son  
Un archivo de resumen **por cada documento original**, vinculado por `doc_id`.

#### Qué aportan
- Síntesis accionable del contenido.
- Extracción explícita de:
  - reglas,
  - excepciones,
  - acciones recomendadas.
- Reducción de ruido frente al documento completo.

#### Para qué se usan
- Consumo rápido por Copilot.
- Respuestas más consistentes.
- Posible reutilización directa como chunks en RAG.
- Actualización independiente del documento original.

---

## 7. Por qué existen varios outputs (y no uno solo)

Cada output representa **la misma información desde una perspectiva distinta**:

| Necesidad                          | CATALOG.json | INDEX.md | Summaries |
|-----------------------------------|--------------|----------|-----------|
| Automatización / pipelines        | ✅           | ❌       | ⚠️        |
| Navegación humana                 | ❌           | ✅       | ✅        |
| Copilot entiende rápido           | ❌           | ✅       | ✅        |
| Escalabilidad                     | ✅           | ❌       | ⚠️        |
| Síntesis y reducción de contexto  | ❌           | ⚠️       | ✅        |
| Preparación para RAG              | ✅           | ❌       | ✅        |

Eliminar uno de ellos:
- ahorra poco,
- limita mucho el sistema.

---

## 8. Qué NO hace este agente

- No responde preguntas.
- No decide qué documento es “correcto” si hay contradicciones.
- No elimina documentación.
- No vectoriza contenido.
- No implementa RAG.

Es una **capa previa de preparación y gobierno del conocimiento**.

---

## 9. Impacto esperado

Con este agente se espera:
- Mejor comprensión de la documentación por Copilot.
- Menor consumo de contexto.
- Menos alucinaciones.
- Base sólida y reusable para decidir si es necesario un RAG.

---

## 10. Objetivo de este README

Este documento describe **una posible aproximación**, no una decisión cerrada.

Su objetivo es:
- permitir que cada parte proponga alternativas,
- comparar enfoques con criterios claros,
- y decidir conjuntamente:
  - arquitectura,
  - implementación,
  - y nivel de complejidad.
