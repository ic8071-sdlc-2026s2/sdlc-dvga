### Herramienta

Prueba pytest

### Predicción antes de correr la herramienta

Predijimos que la prueba de systemDebug fallaría contra la app vulnerable porque el argumento llega a la shell.

### Descripción del hallazgo

La prueba `test_inyeccion_de_comandos` (caso #3) confirma que `systemDebug(arg:"aux; id")` ejecuta el comando encadenado y devuelve el uid del proceso. Ni Semgrep p/default ni ZAP lo ven; solo la prueba escrita desde el caso.

### Ubicación

`app/core/views.py` `resolve_system_debug`, `app/core/helpers.py` `run_cmd`

### CWE

CWE-78

### Severidad

Crítica

### Trazabilidad (casos de abuso o requerimientos)

#3, #11

### Decisión

Corregir

### Justificación

Trazado al caso #3 y al requerimiento #11 (V1.2.5). Se corrige en la fase 5 validando el argumento (solo PID numérico); la prueba pasa y lleva @pytest.mark.corregida.
