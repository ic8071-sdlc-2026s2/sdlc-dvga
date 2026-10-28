# Presentación final · Damn Vulnerable GraphQL Application (DVGA)

De 5 a 7 minutos: revisión final de seguridad y demo en una sola.

## 1. La app y su arquitectura (1 minuto)

DVGA es una API GraphQL hecha con Flask y Graphene que gestiona *pastes*
(fragmentos de texto). Un solo endpoint, `/graphql`, recibe consultas,
mutaciones y suscripciones; GraphiQL está en `/graphiql`. Guarda pastes,
usuarios, dueños y un registro de auditoría en SQLite.

El DFD (`seguridad/fase-2/dfd.drawio.svg`) marca tres fronteras de confianza:

1. **Internet / la API.** Todo lo que entra por `/graphql` es no confiable:
   el campo `filter`, el argumento de `systemDebug`, la cookie `env`.
2. **Identidad (token JWT) dentro de la API.** El token dice quién es el
   consumidor, pero los resolvers no comprueban que la operación le corresponda
   (IDOR de pastes privados, `deleteAllPastes` sin rol).
3. **La API / la base SQLite.** El campo `filter` cruza esta frontera
   concatenado en una sentencia SQL.

## 2. Los tres riesgos más altos (1 minuto)

| Riesgo | P × I | Caso | Requerimiento |
|:---|:---|:---|:---|
| R-01 Inyección de comandos del SO (`systemDebug`) da ejecución remota | 9 | #3 | #11 (V1.2.5) |
| R-02 Inyección SQL en el filtro de pastes expone o altera la base | 9 | #2 | #10 (V1.2.4) |
| R-03 `deleteAllPastes` sin rol borra todos los pastes | 6 | #5 | #13 (V8.2.1) |

## 3. Qué encontró cada técnica (2 minutos)

Una fila por debilidad trazada. «sí» = la técnica la detectó; «no» = no la
detecta; «parcial» = la roza sin nombrarla. Resultados de corridas reales con
las versiones del curso (Semgrep 1.182.0, Gitleaks 8.30.1, Trivy 0.76.1, ZAP
2.17.0, pytest 9.1.1).

| Debilidad (CWE) | ARA / casos | SAST (Semgrep) | SCA (Trivy) | Secretos (Gitleaks) | DAST (ZAP graphql) | pytest de abuso |
|:---|:--:|:--:|:--:|:--:|:--:|:--:|
| Fuerza bruta en login (307) | sí | no | no | no | no | sí (#1) |
| Inyección SQL en el filtro (89) | sí | sí (`avoid-sqlalchemy-text` + regla propia) | no | no | no confirmado | sí (#2) |
| Inyección de comandos OS (78) | sí | no | no | no | no confirmado | sí (#3) |
| IDOR de paste privado (639) | sí | no | no | no | no | sí (#4) |
| `deleteAllPastes` sin rol (862) | sí | no | no | no | no | sí (#5) |
| Introspección habilitada (200) | sí | no | no | no | sí (el import del esquema la usa) | sí (#6) |
| Lotes / recursión sin límite (770) | sí | no | no | no | no | sí (#7) |
| Cabeceras ausentes y cookie sin HttpOnly (1004) | sí | sí (`secure-set-cookie`) | no | no | sí (cabeceras, banner) | sí (#8) |
| Secreto en el código `dvga` (798) | sí | sí (`avoid_hardcoded_config_SECRET_KEY`) | no | parcial (JWT de pruebas) | no | no |
| JWT sin verificar firma (347) | sí | sí (`unverified-jwt-decode`) | no | no | no | no |
| Dependencia vulnerable (1395) | no | no | sí (Trivy fs e imagen) | no | no | no |
| Operaciones sin bitácora (778) | sí | no | no | no | no | no |

Lección: ninguna técnica sola detecta todo. La inyección SQL aparece en SAST
(incluso en `p/default` para esta app) y en la prueba; la inyección de comandos y
el IDOR solo en las pruebas escritas desde los casos; la dependencia vulnerable
solo en el SCA; las cabeceras en SAST y en DAST. ZAP en modo GraphQL ve la
superficie HTTP (cabeceras, banner) e importa el esquema por introspección, pero
no la lógica de negocio.

> Nota de operación: el escaneo **activo** de ZAP sobre DVGA es muy lento porque
> el resolver `systemUpdate` simula carga con esperas de hasta 50 s. El modo y el
> import del esquema se validaron; el análisis activo completo excede el
> presupuesto de tiempo del runner. Por eso la inyección SQL y la de comandos se
> marcan «no confirmado» por DAST: las confirma la prueba de abuso.

## 4. Demo del gate (2 minutos)

- **Correcciones (3 + base).** Se corrigieron en `app/` la inyección SQL
  (parámetro vinculado), la inyección de comandos (`systemDebug` acepta solo un
  PID numérico) y las cabeceras (nosniff + cookie HttpOnly). Las tres pruebas
  llevan `@pytest.mark.corregida` y pasan en verde. Además se cambió la imagen
  base a `python:3.10-slim`.
- **Gate de Trivy.** Medido: la base `python:3.10` completa daba 551
  vulnerabilidades HIGH/CRITICAL del sistema operativo; con slim bajan a 53
  (todas sin parche) y la imagen pasa de 1.21 GB a 354 MB. El gate usa
  `ignore-unfixed: true` (las 53 del SO no tienen versión que instalar) y la línea
  base `seguridad/fase-5/.trivyignore.yaml` cubre las 28 de dependencias de
  Python, cada una con `statement`. Con la línea base el gate pasa; sin ella,
  bloquea.
- **Firma y procedencia.** El release va firmado con cosign (keyless) y con
  attestations de procedencia y de SBOM, verificadas con `gh attestation verify`
  y `cosign verify`.

## 5. Lo que queda pendiente (1 minuto)

- **Riesgos aceptados.** Las 28 dependencias de Python de la línea base: subirlas
  rompe la paridad con DVGA 2.2.0 (graphene 2.x). El secreto `dvga` y el JWT sin
  verificar firma (#18) son retos del propio DVGA; se documentan, no se tocan.
- **No corregido todavía.** IDOR de pastes privados (#4), `deleteAllPastes` sin
  rol (#5), introspección (#6), lotes sin límite (#7) y fuerza bruta (#1): con
  una semana más, se añadiría una capa de autorización por token en los resolvers
  y los límites de profundidad/costo que DVGA solo activa en modo Expert.
