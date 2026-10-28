"""Pruebas de abuso de DVGA, escritas desde los casos de abuso de la fase 1.

Cada prueba afirma el comportamiento seguro (el «Entonces» del requerimiento).
Por eso falla mientras la app siga vulnerable: ese rojo es lo esperado en la
fase 4. Cuando el equipo corrige la debilidad en la fase 5, la prueba pasa y
lleva @pytest.mark.corregida para que el gate del release la exija.

Números de @pytest.mark.caso_abuso(N) (issues del demo):
  1 fuerza bruta en login (CWE-307)     5 deleteAllPastes sin rol (CWE-862)
  2 inyeccion SQL en el filtro (CWE-89)  6 introspeccion habilitada (GraphQL)
  3 inyeccion de comandos OS (CWE-78)    7 ataque por lotes sin limite (CWE-770)
  4 lectura de paste privado (CWE-639)   8 cabeceras de seguridad ausentes (CWE-1004)

La interfaz GraphQL vive en {app_url}/graphql y responde JSON a POST.
"""
import pytest


def gql(sesion, app_url, query, batch=False):
    payload = query if batch else {"query": query}
    return sesion.post(f"{app_url}/graphql", json=payload)


@pytest.fixture(autouse=True)
def _reset(app_url, sesion):
    # DVGA reconstruye la base con GET /start_over; deja cada prueba independiente.
    sesion.get(f"{app_url}/start_over")


@pytest.mark.caso_abuso(1)
def test_login_sin_bloqueo(app_url, sesion):
    """Dado la cuenta admin
    Cuando un atacante envia 12 contrasenas incorrectas seguidas
    Entonces la app debe bloquear o limitar, no aceptar intento tras intento."""
    q = 'mutation{login(username:"admin",password:"incorrecta"){accessToken}}'
    codigos = []
    for _ in range(12):
        r = gql(sesion, app_url, q)
        codigos.append(r.status_code)
    # Sin control anti fuerza bruta, DVGA responde 200 a los 12 intentos.
    assert any(c in (429, 423, 403) for c in codigos), (
        "No hubo bloqueo tras 12 intentos fallidos: la app no limita la fuerza bruta")


@pytest.mark.caso_abuso(2)
@pytest.mark.corregida
def test_sqli_en_filtro_de_pastes(app_url, sesion):
    """Dado el campo filter de la consulta pastes
    Cuando se inyecta una condicion SQL siempre verdadera
    Entonces la app no debe devolver pastes que no coinciden con el filtro."""
    iny = "noexiste' OR '1'='1"
    r = gql(sesion, app_url, '{pastes(filter:"%s"){title}}' % iny)
    datos = r.json().get("data", {}).get("pastes") or []
    assert len(datos) == 0, (
        f"La inyeccion SQL devolvio {len(datos)} pastes que no coinciden con el filtro")


@pytest.mark.caso_abuso(3)
@pytest.mark.corregida
def test_inyeccion_de_comandos(app_url, sesion):
    """Dado el resolver systemDebug, que pasa su argumento a la shell
    Cuando el argumento incluye un comando encadenado (; id)
    Entonces la app no debe ejecutarlo: la salida no trae el uid del proceso."""
    r = gql(sesion, app_url, '{systemDebug(arg:"aux; id")}')
    salida = (r.json().get("data") or {}).get("systemDebug", "") or ""
    assert "uid=" not in salida, (
        f"Inyeccion de comandos OS: se ejecuto 'id'. Salida: {salida[:200]}")


@pytest.mark.caso_abuso(4)
def test_idor_paste_privado(app_url, sesion):
    """Dado un paste privado (public=False) con id conocido
    Cuando un anonimo lo pide por id
    Entonces la app no debe entregar su contenido."""
    r = gql(sesion, app_url, '{paste(id:1){title content public}}')
    paste = (r.json().get("data") or {}).get("paste")
    assert not (paste and paste.get("public") is False and paste.get("content")), (
        f"IDOR: un anonimo leyo un paste privado por id: {paste}")


@pytest.mark.caso_abuso(5)
def test_delete_all_pastes_sin_autorizacion(app_url, sesion):
    """Dado el campo deleteAllPastes
    Cuando un anonimo lo invoca sin token ni rol
    Entonces la app debe rechazarlo, no borrar todos los pastes."""
    r = gql(sesion, app_url, '{deleteAllPastes}')
    cuerpo = r.json()
    rechazado = "errors" in cuerpo or (cuerpo.get("data") or {}).get("deleteAllPastes") is not True
    assert rechazado, "Un anonimo ejecuto deleteAllPastes sin autorizacion"


@pytest.mark.caso_abuso(6)
def test_introspeccion_deshabilitada(app_url, sesion):
    """Dado un entorno que no debe exponer su esquema
    Cuando se envia una consulta de introspeccion
    Entonces la app no debe devolver el esquema completo."""
    r = gql(sesion, app_url, '{__schema{types{name}}}')
    tipos = (((r.json().get("data") or {}).get("__schema") or {}).get("types")) or []
    assert len(tipos) == 0, (
        f"La introspeccion esta habilitada: el esquema expuso {len(tipos)} tipos")


@pytest.mark.caso_abuso(7)
def test_lotes_de_consultas_sin_limite(app_url, sesion):
    """Dado el endpoint GraphQL con batching habilitado
    Cuando se envia un arreglo de 50 consultas en una peticion
    Entonces la app debe limitar el lote, no ejecutarlas todas."""
    lote = [{"query": "{systemHealth}"} for _ in range(50)]
    r = gql(sesion, app_url, lote, batch=True)
    try:
        ejecutadas = sum(1 for x in r.json() if isinstance(x, dict) and x.get("data"))
    except Exception:
        ejecutadas = 0
    assert ejecutadas < 50, (
        f"Ataque por lotes: la app ejecuto {ejecutadas} de 50 consultas sin limite")


@pytest.mark.caso_abuso(8)
@pytest.mark.corregida
def test_cabeceras_de_seguridad(app_url, sesion):
    """Dado cualquier respuesta de la app
    Cuando se inspeccionan sus cabeceras
    Entonces debe traer al menos X-Content-Type-Options: nosniff."""
    r = sesion.get(f"{app_url}/")
    xcto = r.headers.get("X-Content-Type-Options", "").lower()
    assert xcto == "nosniff", (
        f"Faltan cabeceras de seguridad. X-Content-Type-Options={xcto!r}; "
        f"presentes: {list(r.headers.keys())}")
