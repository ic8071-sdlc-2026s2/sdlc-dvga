### Herramienta

Prueba pytest

### Predicción antes de correr la herramienta

Predijimos que la prueba de IDOR fallaría: ZAP no sabe que el paste 1 es privado.

### Descripción del hallazgo

La prueba `test_idor_paste_privado` (caso #4) confirma que un anónimo lee por id un paste con public=False. Es una falla de autorización a nivel de dato que ninguna herramienta genérica detecta.

### Ubicación

`app/core/views.py` `resolve_paste`

### CWE

CWE-639

### Severidad

Alta

### Trazabilidad (casos de abuso o requerimientos)

#4, #12

### Decisión

Aceptar el riesgo con justificación

### Justificación

Trazado al caso #4 y al requerimiento #12. Queda fuera de las tres correcciones obligatorias de la fase 5 (se priorizaron SQLi, inyección de comandos y cabeceras). Se documenta el riesgo residual en la presentación.
