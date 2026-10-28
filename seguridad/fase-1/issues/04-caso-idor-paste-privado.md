### Actor malicioso

Atacante anónimo, sin token.

### Objetivo del atacante

Leer el contenido de un paste marcado como privado que no le pertenece.

### Categoría

I · Divulgación de información

### Carta de Cornucopia

AZ3

### Escenario (Dado, Cuando, Entonces)

Dado un paste con public=False y un identificador conocido o adivinable
Cuando un anónimo pide la consulta paste con ese id
Entonces la API devuelve el título y el contenido del paste privado

### Componente afectado

`POST /graphql`, consulta `paste(id)`, `core/views.py` `resolve_paste`

### CWE

CWE-639

### Requerimientos que lo mitigan

#12
