# Security policy / Política de seguridad

## Reporting a vulnerability / Cómo reportar una vulnerabilidad

Please **do not open a public issue** for a security problem. Use GitHub's private reporting instead:
**[Report a vulnerability](https://github.com/xev777/TrafficBar/security/advisories/new)** (Security tab → "Report a vulnerability").
I will answer as soon as I can and credit you in the fix if you wish.

Por favor **no abras un issue público** para un problema de seguridad. Usa el reporte privado de GitHub:
**[Reportar una vulnerabilidad](https://github.com/xev777/TrafficBar/security/advisories/new)** (pestaña Security → "Report a vulnerability").
Responderé en cuanto pueda y te daré crédito en la corrección si lo deseas.

## Supported versions / Versiones con soporte

Only the latest release receives fixes. / Solo la última versión publicada recibe correcciones.

## What to expect from the program / Qué hace el programa

TrafficBar sends nothing about you anywhere (see [PRIVACY.md](PRIVACY.md)). The security review, its findings and how each
one was handled are in [SEGURIDAD.md](SEGURIDAD.md). Releases are **not code-signed**; verify downloads with the SHA-256 in each
release and, from 1.0.1, with `gh attestation verify <file> --repo xev777/TrafficBar` (see [CODE_SIGNING_POLICY.md](CODE_SIGNING_POLICY.md)).
