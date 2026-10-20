# TrafficBar 1.0.3

## What changed / Qué cambió
- **The Windows proxy is restored when Windows shuts down or you sign out** (before, a process killed during shutdown could leave
  Internet broken until TrafficBar was opened again). / **El proxy de Windows se restaura al apagar Windows o cerrar sesión** (antes,
  un proceso terminado durante el apagado podía dejar Internet sin funcionar hasta abrir TrafficBar de nuevo).
- Tests now run in the build pipeline; GitHub Actions pinned and kept up to date. No other functional changes. / Las pruebas ahora
  corren en la compilación; acciones de GitHub fijadas y actualizadas. Sin otros cambios funcionales.

## Notes / Notas
- **Requires Windows 10 or 11 (64-bit).** / **Requiere Windows 10 u 11 (64 bits).**
- **The executables are not code-signed**; SmartScreen may warn ("More info" → "Run anyway"). Check the SHA-256 below, or verify
  the build with `gh attestation verify <file> --repo xev777/TrafficBar`. / **Los ejecutables no están firmados**; SmartScreen puede
  avisar. Comprueba el SHA-256 o verifica la compilación con `gh attestation verify`.
- The installer offers to install Npcap if it is missing (needed only by the traffic monitor). / El instalador ofrece instalar Npcap
  si falta (solo lo necesita el monitor de tráfico).
- Licensed under **GPL-3.0**. / Licencia **GPL-3.0**.

Full history: [CHANGELOG.md](CHANGELOG.md). / Historial completo: [CHANGELOG.md](CHANGELOG.md).
