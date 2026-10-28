### Actor malicioso

Atacante anónimo que envía consultas al endpoint GraphQL.

### Objetivo del atacante

Agotar los recursos del servidor y dejar la app sin servicio.

### Categoría

D · Denegación de servicio

### Carta de Cornucopia

AZ8

### Escenario (Dado, Cuando, Entonces)

Dado el endpoint GraphQL con batching habilitado y sin límite de profundidad en modo Beginner
Cuando el atacante envía un arreglo de 50 consultas en una sola petición
Entonces la API ejecuta las 50 consultas sin rechazar ni limitar el lote

### Componente afectado

`POST /graphql`, lote de consultas; `core/middleware.py`

### CWE

CWE-770

### Requerimientos que lo mitigan

#15
