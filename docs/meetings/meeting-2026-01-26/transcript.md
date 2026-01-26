# Transcript de reunión - 26 de enero de 2026

## Asistentes
- Product Owner: Laura García
- Tech Lead: Carlos Martínez
- Backend Dev: Ana López
- Frontend Dev: Miguel Torres

---

## Tema: Implementar lista de favoritos en el carrito

**Laura (PO):**
Buenos días a todos. Hoy quiero discutir una nueva funcionalidad que varios usuarios han solicitado: la posibilidad de guardar productos como favoritos o "wish list" directamente desde el carrito. Hemos visto en analytics que muchos usuarios añaden productos al carrito pero no finalizan la compra inmediatamente. Queremos darles la opción de moverlos a una lista de favoritos para consultarlos más tarde sin perder el espacio en el carrito.

**Carlos (Tech Lead):**
Interesante. ¿Estamos hablando de crear una nueva entidad separada del carrito o es parte del mismo?

**Laura:**
Sería una entidad separada. El usuario debería poder marcar productos como favoritos, ver su lista de favoritos, y también poder mover productos desde el carrito a favoritos y viceversa.

**Ana (Backend):**
Ok, entonces necesitaríamos un nuevo servicio o extender el Cart Service. ¿Cómo lo ves Carlos?

**Carlos:**
Yo creo que podemos extender el Cart Service. Al fin y al cabo, es gestión de productos en sesión del usuario. Añadiríamos una nueva colección en MongoDB llamada `favorites` o `wishlists`.

**Miguel (Frontend):**
¿Y en la interfaz? ¿Dónde aparecería esto?

**Laura:**
En el carrito debería haber un botón "Guardar para más tarde" o "Mover a favoritos" en cada producto. También necesitamos una página o sección nueva para ver todos los favoritos.

**Ana:**
Entonces necesitamos varios endpoints:
- POST para añadir un producto a favoritos
- GET para obtener la lista de favoritos del usuario
- DELETE para eliminar un producto de favoritos
- Y quizás un POST para mover un producto del carrito a favoritos

**Carlos:**
Exacto. Y esto solo aplica a usuarios logueados, ¿verdad?

**Laura:**
Correcto, solo usuarios logueados. Los usuarios guest no tendrían esta funcionalidad.

**Miguel:**
¿Y los favoritos tienen que mostrar el precio actual del producto?

**Ana:**
Buena pregunta. Yo diría que sí, deberíamos llamar al Pricing Service para mostrar el precio actualizado cada vez que se consulta la lista de favoritos.

**Laura:**
Sí, de hecho sería bueno mostrar si el precio ha bajado desde que lo añadieron a favoritos. Pero eso puede ser una mejora posterior.

**Carlos:**
Ok, resumiendo:
- Nueva colección `favorites` en MongoDB
- Solo para usuarios logueados (requiere userId)
- Endpoints: añadir, listar, eliminar, y mover desde carrito
- Integración con Pricing Service para precios actualizados
- Sin límite de productos en favoritos por ahora

**Laura:**
Perfecto. ¿Alguna dependencia o bloqueo que veáis?

**Ana:**
No, es bastante directo. Solo necesitamos asegurarnos de que el modelo de datos incluya: userId, productId, fecha de añadido, y quizás algún campo para notas del usuario si quieren.

**Miguel:**
Por mi parte, necesitaré el contrato de la API para empezar a integrar en el frontend.

**Carlos:**
Ok, entonces la propuesta es:
- Nuevo endpoint POST /v1/favorites para añadir productos
- GET /v1/favorites para listar todos los favoritos del usuario
- DELETE /v1/favorites/{productId} para eliminar
- POST /v1/carts/{cartId}/items/{productId}/move-to-favorites para mover del carrito a favoritos

**Laura:**
Me parece bien. ¿Plazo estimado?

**Ana:**
Yo diría un sprint. Es relativamente simple.

**Laura:**
Perfecto. Creamos la US y empezamos.

---

## Acuerdos finales:
1. Implementar lista de favoritos solo para usuarios logueados
2. Nueva colección en MongoDB: favorites
3. Cuatro endpoints nuevos en Cart Service
4. Integración con Pricing Service para precios actualizados
5. Plazo: 1 sprint
6. Sin merge de favoritos entre dispositivos en esta fase (puede ser futuro)
