### Actor malicioso

Atacante anónimo en fase de reconocimiento.

### Objetivo del atacante

Obtener el esquema completo (tipos, campos y argumentos ocultos) para planear otros ataques.

### Categoría

I · Divulgación de información

### Carta de Cornucopia

VE10

### Escenario (Dado, Cuando, Entonces)

Dado el endpoint GraphQL expuesto, que no debería revelar su esquema a cualquiera
Cuando el atacante envía la consulta de introspección __schema
Entonces la API devuelve el esquema completo con todos los tipos y campos del servidor

### Componente afectado

`POST /graphql`, consulta de introspección `__schema`

### CWE

CWE-200

### Requerimientos que lo mitigan

#14
