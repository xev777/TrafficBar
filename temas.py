"""Temas de color y opacidad de la barra flotante.

Cada tema define la paleta que usa trafficbar.py (BG, FG, ACC, BTN…). `aplicar()` los copia a las variables del
módulo; la barra se reconstruye para estrenarlos. Los contrastes de texto están comprobados en las pruebas (WCAG ≥ 4.5).
"""
TEMAS = {
    # nombre: (etiqueta del menú, paleta)
    "dark": ("Oscuro (por defecto)", dict(bg="#1b2a41", fg="#e8eef7", acc="#3fa9f5", btn="#27405f",
                                            field="#0f1a2b", muted="#8ea3bd", accbtn="#1f6fa8", accfg="#ffffff")),
    "quiet": ("Discreto (gris)", dict(bg="#2b2b2b", fg="#d0d0d0", acc="#9a9a9a", btn="#3a3a3a",
                                      field="#202020", muted="#9a9a9a", accbtn="#555555", accfg="#101010")),
    "light": ("Claro", dict(bg="#f2f4f7", fg="#1c2430", acc="#2b6cb0", btn="#d9dfe7",
                            field="#ffffff", muted="#4f5d6e", accbtn="#2b6cb0", accfg="#ffffff")),
    "contrast": ("Alto contraste", dict(bg="#000000", fg="#ffffff", acc="#ffd400", btn="#1f1f1f",
                                        field="#000000", muted="#cfcfcf", accbtn="#0050c8", accfg="#000000")),
}
DEFECTO = "dark"
OPACIDADES = (100, 85, 70, 55, 40)      # % de opacidad ofrecidos en el menú
OPACIDAD_MIN = 30                        # nunca más transparente: la barra debe seguir siendo localizable


def nombre_valido(n):
    return n if isinstance(n, str) and n in TEMAS else DEFECTO


def paleta(n):
    return TEMAS[nombre_valido(n)][1]


def opacidad_valida(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v != v:
        return 100
    return int(min(100, max(OPACIDAD_MIN, v)))


def luminancia(h):
    def c(x):
        x /= 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)


def contraste(a, b):
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
