# 📚 Documentación del proyecto

Este directorio contiene la documentación funcional y técnica del sistema.
La documentación está organizada por **services** y por **releases**, permitiendo
entender tanto el estado actual como la evolución del producto en el tiempo.

Además, el proyecto incluye un **agente automático** encargado de procesar los
*transcripts* de las reuniones y transformarlos en documentación funcional y
**User Stories**, asegurando trazabilidad directa entre reuniones, funcionales
y backlog.

---

## 🧭 Estructura general

```text
agents/
├── us_creator/
docs/
├── backlog/
├── meetings/
├── releases/
├── services/ 
```

## ▶️ Cómo ejecutar el agente

Para transformar los *transcripts* de los meetings en documentación funcional y
User Stories, sigue estos pasos:

1. En caso de un **nuevo meeting**, crea una carpeta dentro de `docs/meetings/` con el formato:
    ```text
    docs/meetings/meeting-YYYY-MM-DD
    ```
    Y añade aqui un solo *transcript.md*

2. Crea un archivo .env con tu clave de OPENAI, siguiendo el ejemplo en .env.example

3. Ejecuta al agente desde la raiz del proyecto
    ```text
    cd agents/us_creator
    python3 US_creator_agent.py
    ```
Al ejecutarse, el agente:
- Genera el documento funcional si no existe.
- Crea el User Story correspondiente en el backlog.
- Añade en el User Story un enlace al documento funcional.
