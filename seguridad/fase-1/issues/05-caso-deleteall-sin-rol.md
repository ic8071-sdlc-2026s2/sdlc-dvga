### Actor malicioso

Atacante anónimo, sin token ni rol de administración.

### Objetivo del atacante

Borrar todos los pastes del servidor sin tener privilegios para ello.

### Categoría

E · Elevación de privilegios

### Carta de Cornucopia

AZ5

### Escenario (Dado, Cuando, Entonces)

Dado el campo deleteAllPastes, una operación destructiva de administración
Cuando un anónimo lo invoca sin token ni verificación de rol
Entonces la API borra todos los pastes y responde true

### Componente afectado

`POST /graphql`, consulta `deleteAllPastes`, `core/views.py`

### CWE

CWE-862

### Requerimientos que lo mitigan

#13
