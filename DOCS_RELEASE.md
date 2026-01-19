2) Estructura incremental por releases (por sprint / user stories)
/releases/indice_releases.md

Qué contiene

Lista de releases con fecha y link

Para cada release:

objetivo del sprint

stories incluidas

docs acumulados afectados (links)

Secciones

# Índice de releases

## Release 1.0 (fecha)

## Release 1.1 (fecha)

/releases/release-1.0_2026-01-XX/indice.md

Qué contiene

Resumen del sprint

Lista de US/commits y links

“Cambios en documentación acumulada” (archivos tocados)

Secciones

# Release 1.0

## Objetivo

## Historias incluidas

## Documentos afectados

/releases/release-1.0_2026-01-XX/US-101_crear_carrito.md

Qué contiene

ID único (US-101)

Fecha

Contexto / problema

Qué se añadió/modificó:

endpoints (exactos)

cambios en schema Mongo (si aplica)

eventos nuevos (si aplica)

Links a docs acumulados relevantes

Nota de compatibilidad

Secciones

# US-101 Crear carrito

## Identificación

## Descripción

## Cambios

## Impacto en APIs

## Impacto en MongoDB

## Links

## Notas

(Repites el patrón para otras US: añadir item, aplicar promos, proceder al pago, etc.)

3) Checklist de “qué deberíamos encontrarnos” en CADA doc de microservicio

Para que sea consistente, cada doc “de servicio” debería traer:

## Responsabilidad

## Dependencias

colas/eventos (si aplica)

Mongo colecciones

llamadas a otros servicios

## Endpoints (si es síncrono)

método + path

request/response (JSON ejemplo)

errores (4xx/5xx)

## Modelo de datos (colecciones y campos clave)

## Flujos (2–3 bullets)

## Consideraciones (idempotencia, timeouts, límites)

Si quieres, en el siguiente paso te puedo dejar:

una plantilla Markdown estándar (para microservicio y para user story de release)

un ejemplo completo ya relleno (por ejemplo 20_cart_service.md + US-102_add_item_to_cart.md) para que lo copiéis/peguéis y escaléis rápido.