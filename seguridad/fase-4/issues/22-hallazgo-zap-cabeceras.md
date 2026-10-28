### Herramienta

ZAP

### Predicción antes de correr la herramienta

Predijimos que ZAP vería las cabeceras y la cookie, pero no la lógica de negocio (IDOR, autorización).

### Descripción del hallazgo

El escaneo de ZAP en modo graphql reporta cabeceras de seguridad ausentes: X-Content-Type-Options, Content-Security-Policy y la fuga del banner del servidor, además de la cookie env sin HttpOnly. Es lo único que ZAP ve desde afuera sin conocer la lógica.

### Ubicación

Todas las respuestas; `app/core/views.py` `index`

### CWE

CWE-1004

### Severidad

Media

### Trazabilidad (casos de abuso o requerimientos)

#8, #16

### Decisión

Corregir

### Justificación

Trazado al caso #8 y al requerimiento #16. Se corrige en la fase 5 agregando las cabeceras y marcando la cookie HttpOnly; la prueba `test_cabeceras_de_seguridad` lo verifica.
