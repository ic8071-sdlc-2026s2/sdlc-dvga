# Issues del demo como archivos

En un repositorio de equipo, los casos de abuso, los requerimientos y los
hallazgos viven como **issues** de GitHub creados con los formularios de
`.github/ISSUE_TEMPLATE/`. En este demo del profesor no hay GitHub todavía, así
que cada issue se guarda como un archivo `.md` con el cuerpo exactamente como lo
rendería el formulario (`### Campo` y el valor debajo), para que `checkpoints.py`
lo parsee igual.

`profesor/scripts/crear-issues-demo.sh` crea estos issues en el orden exacto, con
sus títulos y etiquetas, en un repositorio recién creado y antes del primer push,
para que los números coincidan:

| Carpeta | Archivos | Numeración | Tipo |
|:---|:---|:---|:---|
| `seguridad/fase-1/issues/` | `01` … `08` | issues #1 a #8 | Casos de abuso |
| `seguridad/fase-1/issues/` | `09` … `16` | issues #9 a #16 | Requerimientos ASVS 5.0 |
| `seguridad/fase-3/issues/` | `17` … `21` | issues #17 a #21 | Hallazgos de Semgrep, Gitleaks y SCA |
| `seguridad/fase-4/issues/` | `22` … `24` | issues #22 a #24 | Hallazgos de ZAP y pytest |

La trazabilidad entre archivos usa esos números fijos: los casos citan
requerimientos (#9–#16), los requerimientos citan casos (#1–#8), la regla de
Semgrep cita el requerimiento #10 y las pruebas usan `@pytest.mark.caso_abuso(N)`
con N en #1–#8.
