### Herramienta

Semgrep

### Predicción antes de correr la herramienta

Esperábamos que un SAST con reglas de inyección marcara la concatenación de SQL del filtro de pastes.

### Descripción del hallazgo

La regla p/default `avoid-sqlalchemy-text` y la regla propia `sql-text-con-formato` marcan una sentencia SQL construida con interpolación de cadena y ejecutada con sqlalchemy.text(). El valor del campo filter llega sin parametrizar: es inyección SQL.

### Ubicación

`app/core/views.py:320`

### CWE

CWE-89

### Severidad

Alta

### Trazabilidad (casos de abuso o requerimientos)

#2, #10

### Decisión

Corregir

### Justificación

Trazado al caso #2 y al requerimiento #10 (V1.2.4). Se corrige en la fase 5 usando parámetros vinculados; la prueba `test_sqli_en_filtro_de_pastes` lo verifica. PR de corrección enlazado al cerrar.
