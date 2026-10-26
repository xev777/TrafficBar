"""Comprobación MANUAL de versión nueva (nunca automática, nunca descarga ni instala nada).

Solo se ejecuta cuando el usuario pulsa «Buscar actualizaciones»: una petición HTTPS a la API pública de GitHub
(releases/latest del repositorio de TrafficBar). No envía ningún dato del usuario. El resultado se muestra y,
si hay versión nueva, se ofrece abrir la página de la versión en el navegador.
"""
import json
import re
import urllib.error
import urllib.request

import blocklists

API = "https://api.github.com/repos/xev777/TrafficBar/releases/latest"
PREFIJO_PAGINA = "https://github.com/xev777/TrafficBar/releases/"
MAX_BYTES = 256 * 1024


def version_tupla(v):
    """'v1.2.3' -> (1, 2, 3); None si no es una versión numérica simple."""
    m = re.fullmatch(r"v?(\d{1,4})\.(\d{1,4})\.(\d{1,4})", str(v).strip())
    return tuple(int(x) for x in m.groups()) if m else None


def analizar(cuerpo, actual):
    """(hay_nueva, version_nueva, url) a partir del JSON de GitHub; None si la respuesta no es fiable."""
    try:
        d = json.loads(cuerpo)
        tag, url = d.get("tag_name", ""), d.get("html_url", "")
    except (ValueError, AttributeError):
        return None
    nueva, vigente = version_tupla(tag), version_tupla(actual)
    if nueva is None or vigente is None or not str(url).startswith(PREFIJO_PAGINA):
        return None
    if d.get("prerelease") or d.get("draft"):
        return (False, actual, "")
    return (nueva > vigente, tag.lstrip("v"), url if nueva > vigente else "")


def comprobar(actual, abrir=None, timeout=10):
    """Consulta GitHub. Devuelve lo mismo que analizar(); None si no hay red o la respuesta no es válida."""
    req = urllib.request.Request(API, headers={"User-Agent": "TrafficBar (comprobacion manual)",
                                               "Accept": "application/vnd.github+json"})
    try:
        with (abrir or blocklists._abrir)(req, timeout) as r:
            cuerpo = r.read(MAX_BYTES + 1)
        if len(cuerpo) > MAX_BYTES:
            return None
        return analizar(cuerpo.decode("utf-8", "replace"), actual)
    except (urllib.error.URLError, OSError, ValueError):
        return None
