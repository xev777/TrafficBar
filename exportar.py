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


# ---------------------------------------------------------------- pestañas del historial
# `privado=True` omite lo que revela qué sitios visita o qué hay en el equipo (destinos, rutas, detalles, sitios).
def _hora(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def filas_conexiones(rows, privado=False):
    cab = ("hora", "programa", "puerto") if privado else ("hora", "programa", "destino", "ip", "puerto")
    out = []
    for r in rows:
        if privado:
            out.append((_hora(r["ts"]), r["proc"], r["port"]))
        else:
            out.append((_hora(r["ts"]), r["proc"], r["host"] or "", r["remote"], r["port"]))
    return cab, out


def filas_alertas(rows, privado=False):
    cab = ("hora", "tipo", "titulo", "programa") if privado else ("hora", "tipo", "titulo", "programa", "detalle")
    out = []
    for r in rows:
        base = (_hora(r["ts"]), r["kind"], r["title"], r["proc"] or "")
        out.append(base if privado else base + (r["detail"],))
    return cab, out


def filas_programas(rows, privado=False):
    cab = ("programa", "primera_vez", "ultima_vez", "conexiones") if privado else \
          ("programa", "ruta", "primera_vez", "ultima_vez", "conexiones")
    out = []
    for p in rows:
        base = (p["name"],) + (() if privado else (p["path"] or "",)) + \
               (_hora(p["first_seen"]), _hora(p["last_seen"]), p["conns"])
        out.append(base)
    return cab, out


def filas_paginas(rows, privado=False):
    cab = ("hora", "nota", "puntos", "rastreadores_activos", "bloqueados", "bytes") if privado else \
          ("hora", "sitio", "nota", "puntos", "rastreadores_activos", "bloqueados", "bytes")
    out = []
    for r in rows:
        resto = (r["grade"], r["score"], r["active_trackers"], r["protected"], r["bytes"])
        out.append((_hora(r["ts"]),) + (() if privado else (r["main"],)) + resto)
    return cab, out
