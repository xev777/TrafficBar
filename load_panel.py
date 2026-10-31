"""Panel desplegable de carga de sitios: cada conexión en su fila, con progreso y corte."""
import time
import tkinter as tk
from tkinter import font as tkfont

from i18n import tr
from tooltip import tip
import temas

BG, PANEL, FG, MUTED, ACC = "#14202f", "#1b2a41", "#e8eef7", "#8ea3bd", "#3fa9f5"
GREEN, RED, ORANGE = "#3fb97f", "#ff6b6b", "#ffa94d"
FIELD, BTNC, ROW, TRACK, BARTXT, OFF, SHADOW = "#0f1a2b", "#27405f", "#182638", "#1d4a70", "#ffffff", "#2a3b52", "#000000"


def aplicar_paleta(nombre):
    """Colores del tema elegido para la barra (el panel de carga los comparte)."""
    global BG, PANEL, FG, MUTED, ACC, FIELD, BTNC, ROW, TRACK, BARTXT, SHADOW
    p = temas.paleta(nombre)
    BG, PANEL, FG, MUTED, ACC = p["pbg"], p["bg"], p["fg"], p["muted"], p["acc"]
    FIELD, BTNC, ROW, TRACK, BARTXT = p["field"], p["btn"], p["row"], p["track"], p["bartxt"]
    SHADOW = "#ffffff" if temas.luminancia(p["pbg"]) > 0.5 else "#000000"     # sombra del texto sobre la barra de progreso
W, ROW_H, HEAD_H, FOOT_H, MAX_ROWS = 700, 30, 84, 34, 12


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} TB"


class LoadPanel(tk.Toplevel):
    """Se despliega bajo la barra flotante. Todo se dibuja en un solo Canvas."""

    def __init__(self, app, loader, is_ad, on_cut, on_setting, get_report=None, on_report=None,
                 theme="dark", scale=1.0, opacity=100):
        aplicar_paleta(theme)
        super().__init__(app, bg=BG)
        self.k = temas.escala_panel_valida(scale)       # escala del panel: 1.0 · 0.8 · 0.65
        self.opacity = temas.opacidad_valida(opacity)
        self._links = []
        self.app, self.loader, self.is_ad = app, loader, is_ad
        self.on_cut, self.on_setting = on_cut, on_setting
        self.get_report, self.on_report = get_report, on_report
        self.pinned = False
        self.auto = False          # True si se abrió solo al empezar una carga
        self.closed_by_user = False
        self.hits = []
        compact = getattr(app, "compact", False)
        self.row_h = 22 if compact else 26       # filas más juntas; el tamaño compacto las baja más
        self.max_rows = 8 if compact else 12
        if self.k < 1:
            self.max_rows = min(self.max_rows, 8 if self.k >= 0.8 else 6)
            self.row_h = min(self.row_h, 22 if self.k >= 0.8 else 20)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.cv = tk.Canvas(self, width=int(W * self.k), height=200, bg=BG, highlightthickness=1,
                            highlightbackground=ACC)
        self.cv.pack()
        self.cv.bind("<Button-1>", self._click)
        self.row_boxes = []            # (y0, y1, fila) para los tooltips de cada conexión
        self.summary = (0, 0, 0)       # (terminadas, total, %) para el tooltip de la barra
        tip(self.cv, area=self._tip_at)
        fs = lambda base: max(6, round(base * self.k))
        self.f_bold = tkfont.Font(family="Segoe UI", size=fs(10), weight="bold")
        self.f_norm = tkfont.Font(family="Segoe UI", size=fs(9))
        self.f_big = tkfont.Font(family="Segoe UI", size=fs(12), weight="bold")
        self.f_small = tkfont.Font(family="Segoe UI", size=fs(8))
        self._set_alpha(False)
        self.bind("<Enter>", lambda e: self._set_alpha(True), add="+")
        self.bind("<Leave>", lambda e: self.after(350, self._leave), add="+")
        self.refresh()

    def _set_alpha(self, hover):
        try:
            self.attributes("-alpha", 1.0 if hover else self.opacity / 100)
        except tk.TclError:
            pass

    def _leave(self):
        try:
            x, y = self.winfo_pointerxy()
            dentro = (self.winfo_rootx() <= x < self.winfo_rootx() + self.winfo_width()
                      and self.winfo_rooty() <= y < self.winfo_rooty() + self.winfo_height())
        except tk.TclError:
            return
        self._set_alpha(dentro)

    # ---- dibujo
    def _fit(self, text, font, width):
        width *= self.k
        if font.measure(text) <= width:
            return text
        while text and font.measure(text + "…") > width:
            text = text[:-1]
        return text + "…"

    def refresh(self):
        if not self.winfo_exists():
            return
        c, now = self.cv, time.time()
        frac, active, total = self.loader.last
        rows = self.loader.rows()
        rows.sort(key=lambda r: (r["state"] != "active", r["start"]))
        shown = rows[:self.max_rows]
        h = HEAD_H + max(1, len(shown)) * self.row_h + FOOT_H + (18 if len(rows) > self.max_rows else 0)
        c.config(height=int(h * self.k))
        c.delete("all")
        self.hits = []
        self.row_boxes = []
        self._links = []

        # cabecera
        n_done = sum(r["state"] == "done" for r in rows)
        n_cut = sum(r["state"] == "cut" for r in rows)
        n_blk = sum(r["state"] == "blocked" for r in rows)
        got = sum(r["bytes"] for r in rows)
        c.create_text(16, 14, anchor="w", fill=ACC, font=self.f_big, text="Carga de sitios")
        if active:
            status = f"Cargando… {active} en curso · {human(got)}"
        elif rows:
            status = f"Carga completa · {len(rows)} recursos · {human(got)}"
        else:
            status = "En reposo — abre una página y verás aquí cómo se carga"
        c.create_text(16, 36, anchor="w", fill=MUTED, font=self.f_norm, text=status)
        self._button(W - 178, 6, 128, 26, "✂  CORTAR TODO", RED, "cut_all", enabled=bool(active))
        rep = self.get_report() if self.get_report else None
        if rep and not active:
            from privacy import GRADE_COLOR
            self._button(W - 178 - 196, 6, 188, 26,
                         f"📋 Informe de privacidad · {rep['grade']}", GRADE_COLOR[rep["grade"]],
                         "report", dark_text=True)
        self._button(W - 44, 6, 32, 26, "📌", BTNC if not self.pinned else ACC, "pin")
        # barra grande
        bx0, bx1, by0, by1 = 16, W - 16, 52, 72
        c.create_rectangle(bx0, by0, bx1, by1, fill=FIELD, outline=BTNC)
        if total:
            fx = bx0 + (bx1 - bx0) * frac
            color = GREEN if not active else ACC
            c.create_rectangle(bx0, by0, max(fx, bx0 + 4), by1, fill=color, width=0)
            if active:
                self._shimmer(bx0, by0, fx, by1, now, "#8fd0ff")
            txt = f"{int(frac * 100)} %  ·  {total - active} de {total} recursos"
            for dx, dy, col in ((1, 1, SHADOW), (0, 0, BARTXT)):      # sombra: se lee sobre cualquier color de la barra
                c.create_text((bx0 + bx1) / 2 + dx, (by0 + by1) / 2 + dy, fill=col, font=self.f_bold, text=txt)

        # filas
        y = HEAD_H
        if not shown:
            c.create_text(W / 2, y + self.row_h / 2, fill=MUTED, font=self.f_norm,
                          text="Sin actividad de navegación. ¿Está el ⏻ encendido?")
        self.summary = (total - active, total, int(frac * 100))
        for r in shown:
            self.row_boxes.append((y, y + self.row_h, r))
            self._row(y, r, now)
            y += self.row_h
        if len(rows) > self.max_rows:
            c.create_text(16, y + 9, anchor="w", fill=MUTED, font=self.f_small,
                          text=f"+ {len(rows) - self.max_rows} conexiones más")
            y += 18

        # pie
        c.create_line(0, y + 2, W, y + 2, fill=BTNC)
        c.create_text(16, y + 18, anchor="w", fill=MUTED, font=self.f_small,
                      text=f"{n_done} completos · {active} en curso · "
                           f"{n_blk} bloqueados · {n_cut} cortados")
        auto_on = self.on_setting("get")
        self._link(W - 16, y + 18, ("☑" if auto_on else "☐") + "  " + tr("Desplegar solo al cargar"),
                   "auto", anchor="e")
        self._link(W - 250, y + 18, "✕ cerrar", "close", anchor="e")

        self._escalar()
        self._place()
        self.after(120, self.refresh)

    def _row(self, y, r, now):
        c = self.cv
        st = r["state"]
        color = {"active": ACC, "done": GREEN, "cut": RED, "blocked": ORANGE}[st]
        icon = {"active": "●", "done": "✓", "cut": "✂", "blocked": "🚫"}[st]
        ad = self.is_ad(r["host"])
        if (y - HEAD_H) // self.row_h % 2 == 0:
            c.create_rectangle(1, y, W, y + self.row_h, fill=ROW, width=0)
        c.create_text(20, y + self.row_h / 2, fill=color, font=self.f_bold, text=icon)
        host = self._fit(r["host"] or "(sin nombre)", self.f_bold, 300)
        c.create_text(40, y + self.row_h / 2, anchor="w", font=self.f_bold,
                      fill=RED if ad else FG, text=host)
        kind = "publicidad / rastreo" if ad else ("HTTPS" if r["kind"] == "tunnel" else "HTTP")
        if st == "blocked":
            kind = "bloqueado por tu lista"
        elif st == "cut":
            kind += " · cortado"
        c.create_text(352, y + self.row_h / 2, anchor="w", fill=RED if ad else MUTED,
                      font=self.f_small, text=kind)
        c.create_text(548, y + self.row_h / 2, anchor="e", fill=FG, font=self.f_norm,
                      text=human(r["bytes"]) if r["bytes"] else "·")
        # mini barra
        x0, x1 = 566, 640
        m = (self.row_h - 10) // 2                   # la mini barra mide siempre 10 px de alto
        y0, y1 = y + m, y + self.row_h - m
        c.create_rectangle(x0, y0, x1, y1, fill=FIELD, width=0)
        if st == "active":
            c.create_rectangle(x0, y0, x1, y1, fill=TRACK, width=0)
            self._shimmer(x0, y0, x1, y1, now + (r["id"] % 7) * 0.13, ACC)
        else:
            c.create_rectangle(x0, y0, x1, y1, fill=color, width=0)
        if st == "active":
            self._link_box(654, y + 4, 34, self.row_h - 8, "✂", f"cut:{r['id']}", RED)

    def _shimmer(self, x0, y0, x1, y1, t, color):
        """Franja que recorre la barra: indica que la conexión sigue viva."""
        span = x1 - x0
        if span < 6:
            return
        seg = min(30, span * 0.4)
        pos = ((t * 1.3) % 1.0) * (span + seg) - seg
        a, b = max(x0, x0 + pos), min(x1, x0 + pos + seg)
        if b > a:
            self.cv.create_rectangle(a, y0, b, y1, fill=color, width=0)

    def _button(self, x, y, w, h, text, color, action, enabled=True, dark_text=False):
        fill = color if enabled else OFF
        self.cv.create_rectangle(x, y, x + w, y + h, fill=fill, width=0)
        txt = "#0b1220" if dark_text else "white"
        self.cv.create_text(x + w / 2, y + h / 2, fill=txt if enabled else MUTED,
                            font=self.f_bold, text=text)
        if enabled or action == "pin":
            self.hits.append((x, y, x + w, y + h, action))

    def _link_box(self, x, y, w, h, text, action, color):
        self.cv.create_rectangle(x, y, x + w, y + h, fill=BTNC, width=0)
        self.cv.create_text(x + w / 2, y + h / 2, fill=color, font=self.f_bold, text=text)
        self.hits.append((x, y, x + w, y + h, action))

    def _link(self, x, y, text, action, anchor="w"):
        t = self.cv.create_text(x, y, anchor=anchor, fill=ACC, font=self.f_small, text=text)
        self._links.append((t, action))             # su zona de clic se calcula tras escalar

    def _escalar(self):
        """Todo se dibuja a tamaño 100 % y se reduce al elegido; las zonas de clic y de ayuda pasan a esa escala."""
        c, k = self.cv, self.k
        if k != 1.0:
            c.scale("all", 0, 0, k, k)
            self.hits = [(a * k, b * k, d * k, e * k, f) for a, b, d, e, f in self.hits]
            self.row_boxes = [(a * k, b * k, r) for a, b, r in self.row_boxes]
        for item, action in self._links:
            bx = c.bbox(item)
            self.hits.append((bx[0] - 4, bx[1] - 4, bx[2] + 4, bx[3] + 4, action))

    # ---- tooltips
    TIPS = {
        "cut_all": "Corta todas las conexiones en curso y rechaza las nuevas durante 4 segundos.",
        "report": "Abrir el informe de privacidad de esta carga: qué sitios contactó, cuáles son "
                  "rastreadores y su nota.",
        "pin": "Fijar: el panel no se pliega solo al terminar la carga.",
        "auto": "Si está marcado, el panel se despliega solo cuando empieza una carga grande y se "
                "pliega al terminar.",
        "close": "Cerrar el panel.",
    }
    STATE_TEXT = {"active": "Descargando ahora", "done": "Terminó",
                  "cut": "Cortada por ti", "blocked": "Bloqueada por tu lista de dominios"}

    def _tip_at(self, x, y):
        for x0, y0, x1, y1, action in self.hits:
            if x0 <= x <= x1 and y0 <= y <= y1:
                return "Cortar solo esta conexión." if action.startswith("cut:") \
                    else self.TIPS.get(action)
        k = self.k
        if 52 * k <= y <= 72 * k and 16 * k <= x <= (W - 16) * k:
            done, total, pct = self.summary
            return f"{done} de {total} conexiones terminadas ({pct} %)." if total else None
        for y0, y1, r in self.row_boxes:
            if y0 <= y < y1:
                kind = "HTTPS (túnel cifrado)" if r["kind"] == "tunnel" else "HTTP"
                end = r["end"] or time.time()
                extra = "\nEstá en tu lista de publicidad / rastreo." if self.is_ad(r["host"]) else ""
                return (f"{r['host'] or '(sin nombre)'}\n{kind} · {human(r['bytes'])} · "
                        f"{max(0.0, end - r['start']):.1f} s\n{self.STATE_TEXT[r['state']]}{extra}")
        return None

    # ---- interacción
    def _click(self, e):
        for x0, y0, x1, y1, action in self.hits:
            if x0 <= e.x <= x1 and y0 <= e.y <= y1:
                if action == "cut_all":
                    self.on_cut()
                elif action.startswith("cut:"):
                    self.loader.cut_item(int(action[4:]))
                elif action == "pin":
                    self.pinned = not self.pinned
                elif action == "report" and self.on_report:
                    self.on_report()
                elif action == "auto":
                    self.on_setting("toggle")
                elif action == "close":
                    self.closed_by_user = True
                    self.destroy()
                return

    def _place(self):
        """Junto a la barra: debajo si la barra está arriba, encima si está abajo, y siempre en
        el monitor de la barra (el panel la sigue al cambiar de pantalla)."""
        h, w = self.cv.winfo_reqheight(), int(W * self.k)
        x, y = self.app.anchor_for(w + 2, h + 2)
        self.geometry(f"{w + 2}x{h + 2}+{x}+{y}")
