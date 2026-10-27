# TrafficBar 1.1.0

## What's new / Novedades
- **Click the "new program" notification to block it.** The balloon now invites you to click it; that opens the usual confirmation
  (1 h / 4 h / until you unblock) and nothing is blocked without confirming. / **Haz clic en el aviso de «programa nuevo» para
  bloquearlo.** Se abre la confirmación de siempre (1 h / 4 h / hasta desbloquear); nunca se bloquea nada sin confirmar.
- **Export to CSV from every History tab** (Traffic, Connections, Alerts, Programs, Pages), with a file name per tab. Tabs that contain
  sites or paths ask whether to omit them. / **Exportar a CSV desde cada pestaña del Historial**, con un nombre de archivo por pestaña.
  Las que contienen sitios o rutas preguntan si omitirlos.
- **Check for updates** (manual, right-click menu): one HTTPS request to GitHub, nothing is sent or downloaded, never automatic. /
  **Buscar actualizaciones** (manual, menú del clic derecho): una petición HTTPS a GitHub, no envía ni descarga nada, nunca es automático.
- **SBOM** (CycloneDX) published with each build. / **SBOM** (CycloneDX) publicado con cada compilación.

## Notes / Notas
- **Requires Windows 10 or 11 (64-bit).** / **Requiere Windows 10 u 11 (64 bits).**
- **The executables are not code-signed**; SmartScreen may warn ("More info" → "Run anyway"). Check the SHA-256 below, or verify
  the build with `gh attestation verify <file> --repo xev777/TrafficBar`. / **Los ejecutables no están firmados**; SmartScreen puede
  avisar. Comprueba el SHA-256 o verifica la compilación con `gh attestation verify`.
- The installer offers to install Npcap if it is missing (needed only by the traffic monitor). / El instalador ofrece instalar Npcap
  si falta (solo lo necesita el monitor de tráfico).
- Licensed under **GPL-3.0**. / Licencia **GPL-3.0**.

Full history: [CHANGELOG.md](CHANGELOG.md). / Historial completo: [CHANGELOG.md](CHANGELOG.md).
