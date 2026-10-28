### Actor malicioso

Atacante anónimo con una lista de contraseñas.

### Objetivo del atacante

Adivinar la contraseña de la cuenta admin para tomar su sesión.

### Categoría

S · Suplantación

### Carta de Cornucopia

AT2

### Escenario (Dado, Cuando, Entonces)

Dado la cuenta admin de DVGA, que inicia sesión por la mutación login
Cuando el atacante envía 100 contraseñas incorrectas seguidas a la mutación login
Entonces la API responde a todas sin bloquear, retrasar ni limitar la cuenta

### Componente afectado

`POST /graphql`, mutación `login`

### CWE

CWE-307

### Requerimientos que lo mitigan

#9
