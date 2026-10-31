# TrafficBar 1.2.0

## What's new / Novedades
- **A more discreet bar.** Right-click the bar for:
  - **Color theme:** Dark (default), Quiet (gray), Light and High contrast. Text contrast is checked (WCAG AA).
  - **Opacity** (100 / 85 / 70 / 55 / 40 %): the bar becomes opaque when the mouse is over it, and never goes below 30 %.
  - **Page-load panel size** (100 / 80 / 65 %), with tighter rows. The panel and the tooltips follow the theme and the opacity.
  / **Una barra más discreta.** Clic derecho en la barra:
  - **Tema de color:** Oscuro (por defecto), Discreto (gris), Claro y Alto contraste. El contraste del texto está comprobado (WCAG AA).
  - **Opacidad** (100 / 85 / 70 / 55 / 40 %): la barra se vuelve opaca al pasar el ratón y nunca baja del 30 %.
  - **Tamaño del panel de carga** (100 / 80 / 65 %), con las filas más juntas. El panel y los globos de ayuda siguen el tema y la opacidad.
- Dependency updates (PyInstaller 6.22.3, hooks 2026.9, setuptools 84.2.1, packaging 26.3). / Dependencias actualizadas.

## Notes / Notas
- Themes apply to the bar, the page-load panel, tooltips and the dialogs of the bar; History, Report and the traffic monitor keep their dark look. / Los temas se aplican a la barra, al panel de carga, a los globos de ayuda y a los diálogos de la barra; Historial, Informe y el monitor de tráfico conservan su aspecto oscuro.
- **Requires Windows 10 or 11 (64-bit).** / **Requiere Windows 10 u 11 (64 bits).**
- **The executables are not code-signed**; SmartScreen may warn ("More info" → "Run anyway"). Check the SHA-256 below, or verify
  the build with `gh attestation verify <file> --repo xev777/TrafficBar`. / **Los ejecutables no están firmados**; SmartScreen puede
  avisar. Comprueba el SHA-256 o verifica la compilación con `gh attestation verify`.
- The installer offers to install Npcap if it is missing (needed only by the traffic monitor). / El instalador ofrece instalar Npcap
  si falta (solo lo necesita el monitor de tráfico).
- Licensed under **GPL-3.0**. / Licencia **GPL-3.0**.

Full history: [CHANGELOG.md](CHANGELOG.md). / Historial completo: [CHANGELOG.md](CHANGELOG.md).
