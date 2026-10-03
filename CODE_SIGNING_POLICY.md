# Code signing policy

**Status: the published binaries are not digitally signed.** Windows SmartScreen may show a warning the first time you run
the installer. The project does not currently have a code-signing certificate; if one is obtained in the future, this page
will be updated with the certificate's name and the signing process.

## How to verify a download without a signature
Every release lists the SHA-256 of each file in its notes. Compare it with the file you downloaded:

```powershell
Get-FileHash .\TrafficBar-Setup-<version>.exe -Algorithm SHA256
```

If the hashes differ, do not run the file. Download only from this repository's
[Releases](https://github.com/xev777/TrafficBar/releases) page.

## How the binaries are built
Released from the source in this repository, with the build script [`compilar.ps1`](compilar.ps1): PyInstaller in folder mode
(not a self-extracting single file), Microsoft Defender scan before packaging (the build stops if the executable is flagged),
then Inno Setup for the installer. The public [GitHub Actions workflow](.github/workflows/build.yml) builds the same sources on
GitHub's servers.

## Team and roles
| Role | Person |
|---|---|
| Author / committer | Fernando Erazo ([@xev777](https://github.com/xev777)) |
| Reviewer (approves pull requests from non-committers) | Fernando Erazo ([@xev777](https://github.com/xev777)) |
| Release approver | Fernando Erazo ([@xev777](https://github.com/xev777)) |

Changes from anyone else arrive as pull requests that a reviewer must approve before merging.

## What TrafficBar does to your system (announced)
TrafficBar is a network monitor and filter. It does **only** what you ask for, and every change is reversible from the app:
* turns the Windows **proxy** (`127.0.0.1`) on/off (⏻ button) and restores it on exit;
* creates Windows Firewall rules named `TrafficBar block: …` to block a program you choose (needs administrator);
* adds Windows loopback exemptions for Microsoft Store apps you choose (needs administrator);
* optionally starts with Windows (`HKCU\…\Run`).
The uninstaller removes all of the above.

## Privacy
See [PRIVACY.md](PRIVACY.md): **this program will not transfer any information to other networked systems unless specifically
requested by the user or the person installing or operating it.**
