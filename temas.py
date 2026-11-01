"""Temas de color y opacidad de la barra flotante.

Cada tema define la paleta que usa trafficbar.py (BG, FG, ACC, BTN…). `aplicar()` los copia a las variables del
módulo; la barra se reconstruye para estrenarlos. Los contrastes de texto están comprobados en las pruebas (WCAG ≥ 4.5).
"""
TEMAS = {
    # nombre: (etiqueta del menú, paleta)
    "dark": ("Oscuro (por defecto)", dict(bg="#1b2a41", fg="#e8eef7", acc="#3fa9f5", btn="#27405f",
                                            field="#0f1a2b", muted="#8ea3bd", accbtn="#1f6fa8", accfg="#ffffff",
                                            pbg="#14202f", row="#182638", track="#1d4a70", bartxt="#ffffff", grid="#1d2c42")),
    "quiet": ("Discreto (gris)", dict(bg="#2b2b2b", fg="#d0d0d0", acc="#9a9a9a", btn="#3a3a3a",
                                      field="#202020", muted="#9a9a9a", accbtn="#555555", accfg="#101010",
                                      pbg="#232323", row="#2b2b2b", track="#4a4a4a", bartxt="#ffffff", grid="#303030")),
    "light": ("Claro", dict(bg="#f2f4f7", fg="#1c2430", acc="#2b6cb0", btn="#d9dfe7",
                            field="#ffffff", muted="#4f5d6e", accbtn="#2b6cb0", accfg="#ffffff",
                            pbg="#ffffff", row="#eef1f5", track="#bcd3ee", bartxt="#1c2430", grid="#d3dae3")),
    "contrast": ("Alto contraste", dict(bg="#000000", fg="#ffffff", acc="#ffd400", btn="#1f1f1f",
                                        field="#000000", muted="#cfcfcf", accbtn="#0050c8", accfg="#000000",
                                        pbg="#000000", row="#141414", track="#003a8c", bartxt="#ffffff", grid="#2e2e2e")),
}
DEFECTO = "dark"
OPACIDADES = (100, 85, 70, 55, 40)      # % de opacidad ofrecidos en el menú
ESCALAS_PANEL = ((1.0, "Normal (100 %)"), (0.8, "Pequeño (80 %)"), (0.65, "Mínimo (65 %)"))
OPACIDAD_MIN = 30                        # nunca más transparente: la barra debe seguir siendo localizable


def nombre_valido(n):
    return n if isinstance(n, str) and n in TEMAS else DEFECTO


def paleta(n):
    return TEMAS[nombre_valido(n)][1]


def opacidad_valida(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v != v:
        return 100
    return int(min(100, max(OPACIDAD_MIN, v)))


def escala_panel_valida(v):
    """Solo se admiten las escalas del menú; cualquier otro valor del config.json vuelve a 100 %."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return 1.0
    return next((e for e, _ in ESCALAS_PANEL if abs(e - v) < 1e-6), 1.0)


def luminancia(h):
    def c(x):
        x /= 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)


def contraste(a, b):
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def ajustar(color, fondo, minimo=4.5):
    """Oscurece o aclara `color` lo justo para que se lea sobre `fondo` (los colores que ya se leen no cambian)."""
    if contraste(color, fondo) >= minimo:
        return color
    meta = (0, 0, 0) if luminancia(fondo) > 0.4 else (255, 255, 255)
    rgb = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    for paso in range(1, 21):
        mezcla = "#%02x%02x%02x" % tuple(round(c + (m - c) * paso / 20) for c, m in zip(rgb, meta))
        if contraste(mezcla, fondo) >= minimo:
            return mezcla
    return "#%02x%02x%02x" % meta


def ventana(nombre, tipo="A"):
    """Colores de las ventanas secundarias. Tipo A (Historial, Informe, Monitor): fondo = pbg, tarjetas = bg.
    Tipo B (cuota, programas, tienda, ayuda): fondo = bg, tarjetas = campo."""
    p = paleta(nombre)
    bg, panel = (p["pbg"], p["bg"]) if tipo == "A" else (p["bg"], p["field"])
    v = dict(BG=bg, PANEL=panel, FG=p["fg"], MUTED=p["muted"], ACC=p["acc"], FIELD=p["field"], BTN=p["btn"],
             GRID=p["grid"], ACCBTN=p["accbtn"], ACCFG=p["accfg"])
    v["DOWN_C"] = ajustar("#3fa9f5", p["field"])
    v["UP_C"] = ajustar("#ffa94d", p["field"])
    v["WARN"] = ajustar("#ffd166", p["field"])
    v["HOT"] = ajustar("#ff9f43", p["field"])
    v["OKC"] = ajustar("#7fd6a6", p["field"])
    v["DIM"] = ajustar("#5f7390", p["field"], 3.0)
    v["ALERT"] = ajustar("#ff6b6b", bg)
    return v
