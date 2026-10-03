# TrafficBar

*(Formerly NavTool — renamed at 1.0.0 to avoid a name clash with an unrelated company. Same app, same license, same author.)*

**A floating bar for Windows that shows and controls what happens with your Internet connection** —
how pages load, who tracks you, and which programs use your network. Works with every browser.

*(Español: [README.es.md](README.es.md))*

![The TrafficBar bar: ON/OFF, page-load status, blocked count, Traffic, Report, History, Statistics, search](docs/img/bar.png)

## Screenshots

**Network monitor** — every program, who it talks to, how much it moves, with exact totals (Npcap capture).

![Network monitor window: download/upload rates, active conversations, live graph and a per-program table](docs/img/traffic-monitor.png)

<table>
<tr>
<td width="50%" valign="top"><b>Page-load panel</b> — watch each connection while a page loads and cut any of them.<br><br><img src="docs/img/page-load.png" alt="Page-load panel with progress bar and per-site connections, each with a cut button"></td>
<td width="50%" valign="top"><b>Blocked programs</b> — programs you cut off from the Internet with Windows Firewall rules, and when they expire.<br><br><img src="docs/img/blocked-programs.png" alt="Blocked programs window listing the programs without Internet access"></td>
</tr>
</table>

## What it does

| | |
|---|---|
| **Page-load bar** | Watch every connection of a page while it loads, and **cut** it with one click (pop-ups, chained loads). |
| **Privacy report** | A grade (A–F) for each page: which trackers it contacted and which TrafficBar blocked. |
| **Block lists** | Built-in list plus optional Peter Lowe / StevenBlack lists, personal list and exceptions. |
| **Network monitor** | Every program, who it talks to, how much it moves. Npcap capture, exact totals. |
| **Block a program** | Right-click a program in the monitor → Windows Firewall rules (1 h / 4 h / until you unblock). |
| **Store apps compatibility** | WhatsApp / Microsoft Store and other Store apps work with the proxy on (Windows loopback exemption, one click). |
| **Telemetry detector** | Flags when a program on your PC contacts a known telemetry/diagnostics server (crash reports, usage stats). Logs it in its own history — never blocks it. |
| **Monthly data quota** | Set your plan and billing day: usage, projection and warnings at 80 % / 100 %. |
| **History and alerts** | Per-minute usage, per-program usage, new programs, sustained uploads. Kept on your PC only. |
| **Search bar** | Up to 5 search engines, one keystroke to search in all. |
| **Languages** | English (default) and Spanish included; load more language packs (`.json`). |
| **Bar** | Large / medium / collapsed, magnetic docking, tray icon, tooltips, multi-monitor aware. |

Everything runs locally. **No telemetry, no accounts, no automatic updates.**

## Code signing

The current releases are **not digitally signed**; Windows SmartScreen may show a warning. Check the integrity of a download
against the SHA-256 published in each release's notes:

```powershell
Get-FileHash .\TrafficBar-Setup-<version>.exe -Algorithm SHA256
```

See [CODE_SIGNING_POLICY.md](CODE_SIGNING_POLICY.md) and the [privacy policy](PRIVACY.md).

## Install

Download from the [Releases](../../releases) page:

* `TrafficBar-Setup-<version>.exe` — installer (English by default; Spanish available in the first screen).
* `TrafficBar-Portable-<version>.zip` — portable, leaves nothing on the PC.

Check the SHA-256 shown in the release notes. The executables are **not code-signed**, so Windows
SmartScreen may warn ("More info" → "Run anyway").

**Requirements:** Windows 10 or 11, 64-bit. Windows 7, 8 and 8.1 are **not supported** (the Python runtime that
TrafficBar is built on does not run on them; on Windows 7 you would see "api-ms-win-core-path-l1-1-0.dll is missing").

The traffic monitor needs [Npcap](https://npcap.com) and administrator rights. TrafficBar does not bundle Npcap (its license forbids redistribution): if it is missing, **the installer offers to download it from npcap.com** (checking its SHA-256) and starts Npcap's own installer, where you accept its license. You can say no — everything except the traffic monitor works without it.

## Run from source

```powershell
python -m pip install -r requirements.txt
python trafficbar.py
```

Build the installer and the portable zip (needs [Inno Setup 6](https://jrsoftware.org/isinfo.php)):

```powershell
powershell -ExecutionPolicy Bypass -File .\compilar.ps1
```

## Tests

```powershell
python pruebas_seguridad.py    # 52 attack + regression tests (proxy, packet parser, downloads…)
python pruebas_funciones.py    # quota, program blocking, Store apps, language packs, credits
python -m pip_audit -r requirements.txt
python -m bandit -r . -ll --exclude ./dist,./build
```

## Documentation

* [SEGURIDAD.md](SEGURIDAD.md) — security audit, attacks reproduced, residual risks *(Spanish)*.
* [MEDICION.md](MEDICION.md) — does blocking ads save data? Measured. *(Spanish)*
* [TRADUCIR.md](TRADUCIR.md) — how to add a language.
* [CHANGELOG.md](CHANGELOG.md) — what changed in each version.
* [LICENCIAS-TERCEROS.md](LICENCIAS-TERCEROS.md) — third-party components and license notes.

## Contributing

Bug reports, translations and pull requests are welcome. For a new language see [TRADUCIR.md](TRADUCIR.md).
Security issues: please open a private security advisory instead of a public issue.

## License

Copyright (C) 2026 Fernando Erazo. TrafficBar is free software: you can redistribute it and/or modify it under the
terms of the **GNU General Public License version 3** (see [LICENSE](LICENSE)). It is distributed in the hope that it will be
useful, but **without any warranty**.

## Credits

Design and development: Fernando Erazo ([@xev777](https://github.com/xev777)). Programming assistance: Claude (Anthropic).
Third-party components: Npcap (user-installed), psutil, Python/Tkinter. See [LICENCIAS-TERCEROS.md](LICENCIAS-TERCEROS.md).

## Support the project

TrafficBar is free and always will be. If it's useful to you, you can support its development via PayPal
(xev667@hotmail.com) — entirely optional, and also available from the app's About screen.
