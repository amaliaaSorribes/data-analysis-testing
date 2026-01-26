# 🚀 Proyecto versión Web 

Este proyecto permite gestionar meetings y user stories (US) de forma interactiva a través de un chat web. Incluye backend en FastAPI y un frontend simple servido con Python.

---

## ⚡ Cómo iniciar la web

Ejecutar comando `./start.sh` desde la raíz

---

## 📝 Opciones disponibles en el chat

1. Añadir meeting y transcript

    - Permite subir un archivo .md con el transcript del meeting.
    - Primero se pide la fecha del meeting en formato YYYY-MM-DD para guardarse correctamente.
    - Se conecta con el agente `US_creator_agent_individual.py` para crear la funcionalidad y la US

2. Listar meetings

    - Muestra los meetings creados con sus transcripts y funcionales para comprobar creación y existentes.

3. Listar US's en backlog

    - Lista todas las user stories disponibles en backlog en su correspondiente carpeta `to-do`, `in-progress` o `done`.

4. Ver una US específica

    - Permite buscar una US por su ID y mostrar su contenido en mardown formateado.

5. Simular cambio de estado de una US

    - Cambia el estado de una US entre to-do, in-progress y done, subiendo o bajandola.

6. Revisar US Done y proponer cambios (no implementada)

- **TO DO** Planificada para revisar US en estado Done y sugerir cambios a servicios conectada al agente en desarollo.

---

## 🔄 Navegación

- Escribe `"opciones"` para ver el listado de las opciones.

- Y `"exit"` o `"quit"` para deseleccionar una opción y volver al menú principal.