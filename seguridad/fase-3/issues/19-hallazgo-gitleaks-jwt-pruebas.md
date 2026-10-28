### Herramienta

Gitleaks

### Predicción antes de correr la herramienta

Esperábamos que encontrara algún token o clave en el historial del repositorio.

### Descripción del hallazgo

Gitleaks marca dos tokens JWT en `app/tests/test_auth.py`. Son credenciales de ejemplo de la suite de pruebas del proyecto original, no secretos de producción.

### Ubicación

`app/tests/test_auth.py`

### CWE

CWE-798

### Severidad

Baja

### Trazabilidad (casos de abuso o requerimientos)

#18

### Decisión

Falso positivo

### Justificación

Trazado al hallazgo #18. Son datos de prueba del proyecto original, no un secreto en uso. Buen contraste para la clase: Gitleaks encuentra el JWT de las pruebas pero no la clave 'dvga' de app.py, que sí ve Semgrep.
