### Actor malicioso

Atacante en la red o sitio malicioso que embebe la app.

### Objetivo del atacante

Aprovechar la falta de endurecimiento del navegador (robo de cookie, MIME sniffing, clickjacking).

### Categoría

Configuración

### Carta de Cornucopia

SM3

### Escenario (Dado, Cuando, Entonces)

Dado cualquier respuesta de la app y la cookie env que fija la página principal
Cuando se inspeccionan las cabeceras de la respuesta y los atributos de la cookie
Entonces falta X-Content-Type-Options nosniff y la cookie no es HttpOnly

### Componente afectado

Todas las respuestas; `core/views.py` `index` y cabeceras globales

### CWE

CWE-1004

### Requerimientos que lo mitigan

#16
