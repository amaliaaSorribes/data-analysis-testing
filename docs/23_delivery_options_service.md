# Delivery Options Service

## 1. Objetivo del servicio
El **Delivery Options Service** es el microservicio responsable de **calcular y exponer las opciones de entrega disponibles** para un carrito durante la sesión de compra, incluyendo costes estimados y plazos de entrega.

Este servicio permite al cliente visualizar, antes del checkout, **cómo y cuándo** recibirá su pedido.

---

## 2. Alcance funcional
Dentro del Sistema de Cart & Checkout, este servicio cubre:

- Cálculo de opciones de entrega disponibles
- Estimación de costes de transporte
- Estimación de plazos de entrega
- Compatibilidad de entrega según dirección y productos

### Fuera de alcance
- Gestión logística real
- Creación de envíos
- Tracking de pedidos
- Confirmación definitiva de entrega

---

## 3. Arquitectura y dependencias

### Tipo de servicio
- Microservicio **síncrono**
- APIs REST
- Stateless

### Dependencias internas
- Cart Service (contenido del carrito)
- Configuración logística interna
- Consumido por:
  - Cart Service
  - Checkout Service

---

## 4. Modelo de datos
Este servicio **no es owner de datos persistentes**.  
Las reglas de entrega se basan en configuración interna o servicios externos simulados.

---

## 5. Endpoints REST

### Obtener opciones de entrega
**POST** `/v1/delivery/options`

#### Request
```json
{
  "postalCode": "28001",
  "country": "ES",
  "items": [
    {
      "sku": "SKU-001",
      "quantity": 2
    }
  ]
}
