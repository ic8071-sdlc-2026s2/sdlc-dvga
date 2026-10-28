### Actor malicioso

Atacante anónimo que envía consultas al endpoint GraphQL.

### Objetivo del atacante

Ejecutar comandos del sistema operativo en el servidor que corre la app.

### Categoría

E · Elevación de privilegios

### Carta de Cornucopia

VE6

### Escenario (Dado, Cuando, Entonces)

Dado el resolver systemDebug, que pasa su argumento a la shell con os.popen
Cuando el atacante envía el argumento "aux; id" a la consulta systemDebug
Entonces el servidor ejecuta el comando inyectado y devuelve el uid del proceso

### Componente afectado

`POST /graphql`, consulta `systemDebug(arg)`, `core/helpers.py` `run_cmd`

### CWE

CWE-78

### Requerimientos que lo mitigan

#11
