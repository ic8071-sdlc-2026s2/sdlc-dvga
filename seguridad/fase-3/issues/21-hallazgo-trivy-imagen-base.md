### Herramienta

Trivy

### Predicción antes de correr la herramienta

Esperábamos que la imagen base aportara CVE del sistema operativo además de los de las dependencias.

### Descripción del hallazgo

`trivy image` sobre la imagen construida desde la base `python:3.10` completa reporta 551 vulnerabilidades HIGH/CRITICAL del sistema operativo (534 HIGH, 17 CRITICAL) además de las de Python. Es la mayor parte del ruido del gate.

### Ubicación

`app/Dockerfile` (FROM python:3.10)

### CWE

CWE-1395

### Severidad

Alta

### Trazabilidad (casos de abuso o requerimientos)

#15

### Decisión

Corregir

### Justificación

La salida correcta no es baselinar cientos de CVE del SO: es cambiar la base a `python:3.10-slim`. Medido: con slim los CVE del SO bajan de 551 a 53 (todos sin parche disponible) y la imagen de 1.21 GB a 354 MB. Se aplica en la fase 5 y se cierra este hallazgo.
