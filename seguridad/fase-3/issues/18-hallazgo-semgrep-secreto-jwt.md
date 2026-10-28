### Herramienta

Semgrep

### Predicción antes de correr la herramienta

Esperábamos que marcara la clave de firma del JWT escrita en el código y la decodificación de tokens sin verificar la firma.

### Descripción del hallazgo

`avoid_hardcoded_config_SECRET_KEY` marca `JWT_SECRET_KEY = 'dvga'` en app.py; `unverified-jwt-decode` marca `get_identity`, que decodifica el token con verify_signature=False. Con la clave conocida y sin verificación de firma, un atacante puede forjar tokens e identidades.

### Ubicación

`app/app.py:14`, `app/core/helpers.py:21`

### CWE

CWE-798

### Severidad

Alta

### Trazabilidad (casos de abuso o requerimientos)

#1, #5

### Decisión

Aceptar el riesgo con justificación

### Justificación

Trazado a los casos #1 y #5. DVGA usa esa clave y la decodificación sin firma como parte de su reto de forja de JWT; para conservar la paridad con el proyecto original no se cambia en el laboratorio. Se documenta y se prioriza por detrás de las tres correcciones de la fase 5.
