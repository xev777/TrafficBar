"""Exportación del historial de consumo a CSV (por día y por programa).

Los textos de programas vienen de procesos ajenos: toda celda que empiece por =, +, -, @ o un
control se antepone con «'» para que Excel no la ejecute como fórmula (inyección CSV).
"""
import csv
import datetime

PELIGROSOS = ("=", "+", "-", "@", "\t", "\r")
MB = 1024 * 1024


def celda(valor):
    s = str(valor)
    return "'" + s if s.startswith(PELIGROSOS) else s


def _mb(n):
    return round((n or 0) / MB, 2)


def filas_uso(hist, since, until, limit=200):
    """[(seccion, etiqueta, bajada_MB, subida_MB)] — días del rango y programas más activos."""
    out = []
    for r in hist.daily(since, until):
        dia = datetime.date.fromtimestamp(since + int(r["d"]) * 86400).isoformat()
        out.append(("dia", dia, _mb(r["down"]), _mb(r["up"])))
    for r in hist.top_programs(since, until, limit):
        out.append(("programa", r["proc"], _mb(r["down"]), _mb(r["up"])))
    return out


def escribir_csv(ruta, filas, cabecera=("tipo", "nombre", "bajada_MB", "subida_MB")):
    with open(ruta, "w", newline="", encoding="utf-8-sig") as f:   # utf-8-sig: Excel abre bien los acentos
        w = csv.writer(f)
        w.writerow(cabecera)
        for fila in filas:
            w.writerow([celda(c) if isinstance(c, str) else c for c in fila])
    return len(filas)
