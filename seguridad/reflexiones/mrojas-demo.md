# Reflexión de María Rojas (@mrojas-demo)

Reflexión de ejemplo del demo. En un equipo real, cada integrante sube la suya
desde su propia cuenta y el nombre del archivo es su usuario de GitHub.

## Sesión 2 · Rol: Arquitectura

La decisión que tomé fue dónde poner las fronteras de confianza del DFD
(`seguridad/fase-2/dfd.drawio.svg`). Al principio solo veía dos: Internet/la API
y la API/la base. La tercera, la de identidad **dentro** de la API, costó
justificarla porque DVGA casi no usa el token: muchos resolvers son anónimos. La
evidencia que me convenció fue el caso #4 (IDOR de pastes privados) y el #5
(`deleteAllPastes` sin rol): el diseño asume un dueño o un administrador, pero el
código no lo verifica. Esa frontera «existe en el diseño y el código la cruza
mal» es la que mejor explica los riesgos R-03 y R-05 de la matriz.

## Sesión 3 · Rol: AppSec

Lo que no esperaba: que `p/default` de Semgrep sí marcara la inyección SQL del
filtro (`core/views.py:320`) con `avoid-sqlalchemy-text`. Había predicho que no
la vería, como pasa con otras apps. Aun así escribí la regla propia
`sql-text-con-formato` (requerimiento #10) porque `avoid-sqlalchemy-text` marca
cualquier uso de `text()`, incluso el parametrizado seguro; la mía apunta solo al
patrón de interpolación. Lo que Semgrep no vio: la inyección de comandos de
`systemDebug` (`os.popen`), el IDOR ni la falta de autorización. En el pipeline
fijé todas las actions por hash y puse `permissions:` mínimos; eso previene un
ataque como el de `tj-actions/changed-files` de 2025, donde mover una etiqueta a
un commit malicioso filtró los secretos de quienes no fijaban por hash.

## Sesión 4 · Rol: DevSecOps

La prueba que revisé fue `test_inyeccion_de_comandos` (caso #3). Confirma que
`systemDebug(arg:"aux; id")` ejecuta el comando encadenado y devuelve el `uid`
del proceso. Es una debilidad que solo se ve con la app corriendo y con una
prueba que conoce el truco: ni ZAP ni Semgrep la nombraron. ZAP en modo GraphQL
importó el esquema por introspección y reportó las cabeceras ausentes, pero su
escaneo activo es lentísimo contra DVGA porque `systemUpdate` simula carga. Esa
fue la lección más clara del laboratorio: la herramienta genérica ve la
superficie; la prueba escrita desde el caso de abuso ve la lógica.

## Sesión 5 · Rol: Equipo rojo

El gate bloquea tres cosas: vulnerabilidades altas o críticas de Trivy fuera de
la línea base, pruebas `corregida` en rojo y dependencias nuevas de severidad
alta. Dejamos pasar con justificación las 28 dependencias de Python de DVGA 2.2.0
(subirlas rompe graphene 2.x) y los 53 CVE del sistema operativo sin parche en la
base slim. Si esto fuera un producto real con usuarios, no aceptaría el secreto
`dvga` ni el JWT sin verificar firma: rotaría la clave a un vault y validaría la
firma antes de leer la identidad. Aquí se mantienen porque son el reto que DVGA
enseña, pero en producción serían lo primero que corregiría.
