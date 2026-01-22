## US_creator_agent

El agente **US_creator_agent** analiza cada reunión almacenada en `docs/meetings`.

Para cada meeting, sigue el siguiente flujo:

1. Verifica si ya existe un documento **funcional** asociado.
2. Si no existe, genera uno automáticamente transformando el contenido del *transcript* al formato definido en la **plantilla_funcional**.
3. Guarda el documento funcional en la **misma carpeta del meeting**.
4. A partir del funcional recién creado, genera el **User Story** correspondiente.
5. Almacena el User Story en el **backlog**, incluyendo dentro del contenido un **enlace directo al documento funcional**.

Este proceso garantiza trazabilidad entre reuniones, documentación funcional y backlog, manteniendo todo organizado y sincronizado
