# Matriz de riesgos

Una fila por riesgo. La columna «Caso de abuso» cita los issues con #n. El checkpoint lee solo esta tabla: no agregue otras tablas a este archivo.

| ID | Amenaza | STRIDE | Caso de abuso | Probabilidad | Impacto | Riesgo | Tratamiento |
|:---|:---|:---|:---|:---|:---|:---|:---|
| R-01 | Inyección de comandos del SO por systemDebug da ejecución remota en el servidor | E | #3 | 3 | 3 | 9 | Mitigar con #11 (corregir) |
| R-02 | Inyección SQL en el filtro de pastes expone o altera la base | T | #2 | 3 | 3 | 9 | Mitigar con #10 (corregir) |
| R-03 | deleteAllPastes sin verificar rol borra todos los pastes | E | #5 | 3 | 2 | 6 | Mitigar con #13 |
| R-04 | Lotes y consultas anidadas sin límite agotan el servidor (DoS) | D | #7 | 3 | 2 | 6 | Mitigar con #15 |
| R-05 | Lectura de pastes privados por id (IDOR) | I | #4 | 2 | 2 | 4 | Mitigar con #12 (aceptar en fase 5) |
| R-06 | Introspección habilitada revela el esquema completo para planear ataques | I | #6 | 3 | 1 | 3 | Mitigar con #14 |
| R-07 | Fuerza bruta sin bloqueo contra el login toma la cuenta admin | S | #1 | 2 | 2 | 4 | Mitigar con #9 |
| R-08 | Cabeceras ausentes y cookie sin HttpOnly facilitan XSS, sniffing y clickjacking | Configuración | #8 | 2 | 1 | 2 | Mitigar con #16 (corregir) |

## Escala

Probabilidad (P):

- **1, baja.** Requiere acceso privilegiado, conocimiento interno o una cadena de varios pasos.
- **2, media.** Un usuario registrado lo logra con herramientas comunes.
- **3, alta.** Cualquier visitante anónimo lo logra desde el navegador.

Impacto (I):

- **1, bajo.** Afecta a un usuario y se revierte sin pérdida.
- **2, medio.** Expone o altera datos de varios usuarios, o detiene una función.
- **3, alto.** Expone datos sensibles en masa, da control de administración o detiene la app.

Riesgo = P × I. De 1 a 2 es bajo, de 3 a 4 es medio y de 6 a 9 es alto.

Tratamiento: **mitigar** (con el requerimiento #n que lo cubre), **aceptar** (con justificación), **transferir** o **evitar**.

## Mapa de calor

Escriba los ID de riesgo en la celda que les corresponde.

```
            Impacto 1     Impacto 2     Impacto 3
P 3      |     R-06    |  R-03 R-04  |   R-01 R-02   |
P 2      |     R-08    |  R-05 R-07  |               |
P 1      |             |             |               |
```

## Lectura de la matriz

Los riesgos altos (6–9) son los candidatos a corregir en la fase 5: R-01
(inyección de comandos), R-02 (inyección SQL) y R-08 (cabeceras) se corrigen; el
cambio de la imagen base a slim (hallazgo #21) se trata como corrección de cadena
de suministro. R-03, R-04, R-05, R-06 y R-07 se documentan: se aceptan con
justificación o quedan para una iteración futura, porque el laboratorio exige al
menos tres correcciones trazadas, no todas.
