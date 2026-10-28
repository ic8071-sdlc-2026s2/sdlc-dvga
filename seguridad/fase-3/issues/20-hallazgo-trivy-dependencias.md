### Herramienta

Trivy

### Predicción antes de correr la herramienta

Esperábamos varias dependencias de Python con CVE conocidos por las versiones viejas pinneadas en requirements.txt.

### Descripción del hallazgo

`trivy fs app/` reporta 23 vulnerabilidades HIGH/CRITICAL en las dependencias de Python (PyJWT 2.0.1, gevent 22.10.2, h11 0.14.0, certifi 2022.12.7, urllib3 1.26.13, Werkzeug 2.2.2, Flask 2.2.2, python-engineio/socketio). Sobre la imagen construida el conteo sube.

### Ubicación

`app/requirements.txt`

### CWE

CWE-1395

### Severidad

Alta

### Trazabilidad (casos de abuso o requerimientos)

#15

### Decisión

Aceptar el riesgo con justificación

### Justificación

Trazado al requerimiento de dependencias. Subir las versiones rompería la paridad con DVGA 2.2.0 (graphene 2.x). Se baselinan en `seguridad/fase-5/.trivyignore.yaml` con statement por CVE; es la decisión de arquitectura de la fase 5.
