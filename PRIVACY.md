# Privacy policy / Política de privacidad

**This program will not transfer any information to other networked systems unless specifically requested by the user or the
person installing or operating it.**
**Este programa no envía información a otros sistemas en red salvo que el usuario o quien lo instala/usa lo solicite expresamente.**

## What TrafficBar stores (only on your computer) / Qué guarda (solo en tu equipo)
Settings, per-minute network usage, the programs that used the Internet, the sites you visited through the proxy, and alerts
(30 days; traffic totals 62 days). Location: `%LOCALAPPDATA%\TrafficBar` (or the `Datos` folder in the portable version).
You can delete it from *History → Delete all history* or by deleting that folder.

## What TrafficBar sends, and only when you ask / Qué envía, y solo si lo pides
| Action you request | What is sent | To whom |
|---|---|---|
| **Update block lists** (off by default) | An HTTPS request for the list you ticked | The list's own site (Peter Lowe, StevenBlack) |
| **Check for updates** (manual, right-click menu) | One HTTPS request to GitHub's public releases API; nothing about you or your PC is included (GitHub sees your IP address, as with any web request) | `api.github.com` |
| **Identify IP owners** (off by default, asks first) | The IP address only | `rdap.org` |
| **Ping / Traceroute / Site information / Site map** | The address you typed | That address |
| **Search bar** | The search text, opened in *your* browser | The search engine you chose |
| **Load a language pack / template** | Nothing (local files) | — |
| **Export CSV** (History tabs) | Nothing: the file is written where you choose | — |

**CSV exports:** the *Connections*, *Alerts*, *Programs* and *Pages* exports can contain the sites you visit and paths on your PC, as
plain text. TrafficBar asks whether to omit sites, destinations, paths and details; do not leave the file in synced folders or share it
without reviewing it. / Las exportaciones de *Conexiones*, *Alertas*, *Programas* y *Páginas* pueden contener los sitios que visitas
y rutas de tu equipo, en texto sin protección. TrafficBar pregunta si omitir sitios, destinos, rutas y detalles; no dejes el archivo
en carpetas sincronizadas ni lo compartas sin revisarlo.

No accounts, no telemetry, no analytics, no advertising, no automatic updates, no crash reports. The proxy accepts connections
from this computer only and never decrypts HTTPS.
