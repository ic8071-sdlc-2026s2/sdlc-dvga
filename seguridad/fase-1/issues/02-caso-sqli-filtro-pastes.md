### Actor malicioso

Atacante anónimo que envía consultas al endpoint GraphQL.

### Objetivo del atacante

Leer o alterar filas de la base inyectando SQL por el campo de búsqueda.

### Categoría

T · Manipulación

### Carta de Cornucopia

VE2

### Escenario (Dado, Cuando, Entonces)

Dado el campo filter de la consulta pastes, que se concatena en una sentencia SQL
Cuando el atacante envía filter con una condición SQL siempre verdadera
Entonces la consulta devuelve pastes que no coinciden con el filtro pedido

### Componente afectado

`POST /graphql`, consulta `pastes(filter)`, `core/views.py:320`

### CWE

CWE-89

### Requerimientos que lo mitigan

#10
