# Mapa de la app · DVGA

Este documento es andamiaje para la fase 1. Describe qué hace Damn Vulnerable
GraphQL Application (DVGA), cómo está organizada y qué datos guarda, para que su
equipo pueda dibujar el DFD y escribir los casos de abuso. No es una lista de
debilidades: esas las encuentra usted con las herramientas y el análisis de las
fases siguientes.

## Qué es

DVGA es una implementación deliberadamente insegura de una API GraphQL hecha con
Flask. GraphQL expone un solo endpoint, `/graphql`, que recibe por POST un
documento con consultas (`query`), mutaciones (`mutation`) y suscripciones
(`subscription`). A diferencia de REST, no hay una ruta por recurso: el cliente
pide los campos que quiere y el servidor los resuelve.

El dominio es un gestor de *pastes* (fragmentos de texto, como Pastebin): cada
paste tiene un título, un contenido, un dueño, una dirección IP, un agente de
usuario y banderas de público/privado y de autodestrucción (`burn`). Hay además
un modelo de usuarios con contraseña y un registro de auditoría.

El stack: Python 3.10, Flask 2.2 con `Flask-GraphQL` y `graphene` 2.x
(más `graphene-sqlalchemy`), SQLAlchemy sobre una base SQLite en un archivo, y
`gevent`/`flask-sockets` para las suscripciones por WebSocket. La autenticación
usa tokens JWT emitidos por `flask-graphql-auth`.

## Cómo se arranca y se puebla

La base se reconstruye y se puebla en cada arranque: `app.py` ejecuta
`setup.py`, que borra la base, crea las tablas y carga datos de ejemplo (dos
usuarios, un dueño `DVGAUser`, dos pastes privados y diez públicos). No hay que
llamar ninguna ruta de inicialización. La ruta `GET /start_over` reconstruye la
base a mano, útil para dejar un estado limpio entre pruebas.

Cuentas de ejemplo que crea `setup.py`:

| Usuario | Contraseña | Correo |
|:---|:---|:---|
| `admin` | `changeme` | `admin@blackhatgraphql.com` |
| `operator` | `password123` | `operator@blackhatgraphql.com` |

## Modos de operación

DVGA tiene dos niveles de dificultad que cambian qué defensas están activas:
**Beginner** (easy) y **Expert** (hard). El nivel se guarda en la tabla
`servermode` y se cambia con `GET /difficulty/<easy|hard>` o con el encabezado
`X-DVGA-MODE: Expert`. En modo easy, varias protecciones (límite de profundidad,
límite de costo, lista de denegación de operaciones, bloqueo de introspección) no
se aplican. El laboratorio trabaja en el modo por omisión, easy.

## Roles

DVGA no tiene un control de acceso real por sesión sobre los pastes: la mayoría
de las operaciones son anónimas. Los papeles que existen en el diseño son:

- **Anónimo.** Cualquier cliente que llega al endpoint. Puede consultar y crear
  pastes, buscar, leer el registro de auditoría y llamar los resolvers del
  sistema.
- **admin / operator.** Usuarios con contraseña que pueden iniciar sesión
  (`mutation login`) y recibir un token JWT. Algunos campos (por ejemplo la
  contraseña de un usuario) solo se muestran si el token identifica a `admin`.

El token se envía en el cuerpo de la consulta o en una cabecera, según el campo.
La firma del token y la identidad que transporta son parte de lo que su equipo
debe examinar.

## Endpoints y campos principales

El endpoint GraphQL es `POST /graphql`. La interfaz interactiva GraphiQL está en
`GET /graphiql` (protegida por una cookie). Rutas HTML de apoyo: `/`, `/about`,
`/solutions`, `/create_paste`, `/import_paste`, `/upload_paste`, `/my_pastes`,
`/public_pastes`, `/audit`, `/start_over`, `/difficulty/<level>`.

Campos del esquema GraphQL (en `core/views.py`):

| Tipo | Campo | Acceso previsto | Qué hace |
|:---|:---|:---|:---|
| Query | `pastes(public, limit, filter)` | anónimo | Lista pastes; `filter` busca por título o contenido |
| Query | `paste(id, title)` | anónimo | Devuelve un paste por id o título |
| Query | `search(keyword)` | anónimo | Busca en pastes y usuarios |
| Query | `users(id)` | anónimo | Lista usuarios |
| Query | `me(token)` | con token | Datos del usuario del token |
| Query | `audits` | anónimo | Registro de auditoría de operaciones GraphQL |
| Query | `systemHealth` | anónimo | Ejecuta `uptime` en el servidor |
| Query | `systemDebug(arg)` | (diagnóstico) | Ejecuta `ps <arg>` en el servidor |
| Query | `systemDiagnostics(username, password, cmd)` | admin | Ejecuta un comando si las credenciales son válidas |
| Query | `systemUpdate` | anónimo | Simula una carga de trabajo |
| Query | `readAndBurn(id)` | anónimo | Lee y borra un paste de autodestrucción |
| Query | `deleteAllPastes` | (operación destructiva) | Borra todos los pastes |
| Mutation | `createPaste`, `editPaste`, `deletePaste` | anónimo | Alta, edición y borrado de pastes |
| Mutation | `uploadPaste(filename, content)` | anónimo | Escribe un archivo en el servidor |
| Mutation | `importPaste(host, port, path, scheme)` | anónimo | Trae contenido de una URL con `curl` |
| Mutation | `createUser(userData)` | anónimo | Crea un usuario |
| Mutation | `login(username, password)` | anónimo | Inicia sesión y devuelve tokens JWT |
| Subscription | `paste` | anónimo | Notifica pastes nuevos por WebSocket |

La columna "Acceso previsto" describe la intención del diseño. Parte de su trabajo
en las fases 1, 2 y 4 es comprobar si la app de verdad respeta esa intención, y
si las operaciones del sistema (`systemDebug`, `systemDiagnostics`, `importPaste`,
`uploadPaste`) tratan con cuidado lo que reciben.

## Datos que guarda

Tablas en SQLite (`core/models.py`):

- **users**: `id`, `username`, `email`, `password` (en texto plano).
- **pastes**: `id`, `title`, `content`, `public`, `user_agent`, `ip_addr`,
  `owner_id`, `burn`.
- **owners**: `id`, `name`.
- **audits**: `id`, `gqloperation`, `gqlquery`, `timestamp`.
- **servermode**: `id`, `hardened` (el nivel de dificultad).

## Particularidades de GraphQL que conviene conocer

- **Introspección.** GraphQL permite preguntar por su propio esquema con la
  consulta `__schema`. Es muy útil para desarrollar y muy útil para un atacante:
  revela todos los tipos, campos y argumentos. Pregúntese si debería estar
  disponible para cualquiera.
- **Lotes (batching).** El endpoint acepta un arreglo JSON de varias consultas en
  una sola petición. Piense qué pasa si el arreglo trae cientos de consultas.
- **Profundidad y alias.** Una consulta puede anidar campos relacionados muchos
  niveles o pedir el mismo campo muchas veces con alias. Sin límite, eso es un
  vector de denegación de servicio.
- **Un solo endpoint, muchas operaciones.** Las herramientas que razonan por ruta
  HTTP (como un escáner web clásico) ven un solo endpoint. Para analizar GraphQL
  con ZAP se importa el esquema por introspección (modo `graphql`).

## Dónde vive cada parte en `app/`

```
app/
  app.py                 punto de entrada; configuración de Flask y claves
  config.py              host, puerto, base de datos y límites de profundidad/costo
  setup.py               reconstruye y puebla la base en cada arranque
  core/
    views.py             el esquema: Query, Mutations, Subscription y los resolvers
    models.py            modelos User, Paste, Owner, Audit, ServerMode
    security.py          utilidades de "seguridad": credenciales, lista de denegación, límites
    middleware.py        middlewares de profundidad, costo, introspección y nombre de operación
    helpers.py           ejecución de comandos, decodificación de JWT, manejo de archivos
    directives.py        directivas GraphQL propias
    view_override.py     vista GraphQL personalizada y manejo de errores
    parser.py            cálculo de profundidad y campos de una consulta
  db/                    datos de ejemplo (títulos, contenidos, dueños, agentes)
  templates/             páginas HTML y GraphiQL
  static/                CSS y JavaScript
  Dockerfile             imagen de la app (python:3.10)
  requirements.txt       dependencias de Python con sus versiones
```

## Para la fase 1

- Recorra la API con GraphiQL (`/graphiql`) o con `curl` contra `/graphql`. Cree
  un paste, búsquelo, consúltelo por id y lea el registro de auditoría.
- Lance una consulta de introspección (`{__schema{types{name}}}`) y vea cuánto
  revela.
- Para cada carta de Cornucopia que le toque, pregúntese: en esta API GraphQL,
  ¿quién podría hacer algo que el diseño no quería? Piense en los campos del
  sistema, en los pastes privados y en el token.
- Las defensas que trae DVGA (en `core/middleware.py` y `core/security.py`) solo
  se activan en modo Expert. Corregir una debilidad no es cambiar de modo: es
  cambiar el código del resolver para que la operación sea segura en cualquier
  modo.
