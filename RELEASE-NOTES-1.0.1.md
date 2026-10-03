# TrafficBar 1.0.1

## What changed / Qué cambió
- **Requires Windows 10 or 11 (64-bit), and the installer now says so.** On Windows 7/8/8.1 the program failed with cryptic
  errors ("api-ms-win-core-path-l1-1-0.dll is missing", "Failed to load Python DLL") because the Python runtime does not run
  there. / **Requiere Windows 10 u 11 (64 bits) y el instalador ahora lo dice.** En Windows 7/8/8.1 fallaba con errores
  crípticos porque el runtime de Python no funciona ahí.
- The installer and the portable zip include `LICENSE` (GPL-3.0) and `LICENCIAS-TERCEROS.md`. / El instalador y el zip portable
  incluyen la licencia GPL-3.0 y las licencias de terceros.
- UPX compression explicitly disabled. / Compresión UPX desactivada explícitamente.
- Built by GitHub Actions with a **build-provenance attestation**: verify with
  `gh attestation verify <file> --repo xev777/TrafficBar`. / Compilado en GitHub Actions con **attestation de procedencia**.

## Notes / Notas
- **The executables are not code-signed**; SmartScreen may warn ("More info" → "Run anyway"). Check the SHA-256 below. /
  **Los ejecutables no están firmados**; SmartScreen puede avisar. Comprueba el SHA-256.
- Licensed under **GPL-3.0**. / Licencia **GPL-3.0**.

Full history: [CHANGELOG.md](CHANGELOG.md). / Historial completo: [CHANGELOG.md](CHANGELOG.md).
