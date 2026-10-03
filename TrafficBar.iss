; TrafficBar installer (Inno Setup 6).  Build:  ISCC.exe TrafficBar.iss   ->   Output\TrafficBar-Setup-1.0.exe
; Instalador de TrafficBar. Antes hay que generar dist\TrafficBar con PyInstaller (ver compilar.ps1).
; Este archivo se guarda en UTF-8 CON BOM para que los textos con tildes se vean bien.
;
; Idioma: el asistente se abre en INGLÉS y ofrece elegir ESPAÑOL. La elección se guarda en
; {app}\idioma.txt y es el idioma inicial de la aplicación (luego se cambia desde la propia barra).

#define AppName "TrafficBar"
#define AppVersion "1.0.1"
#define AppExe "TrafficBar.exe"
; Npcap is NOT bundled (its free license forbids redistribution). If it is missing the installer offers to download the
; official installer from npcap.com, checks its SHA-256 and starts it, so YOU accept Npcap's own license.
; To update: take the new file from https://npcap.com/dist/ and put its SHA-256 here.
#define NpcapVersion "1.89"
#define NpcapSha256 "8aed85e900d783d1308506e919587d3e540451947af8a82f2d04f819e44305cc"

[Setup]
AppId={{FA9D2CBD-4691-4E3A-AE9C-AB39DD6B2DE1}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=Fernando Erazo
AppPublisherURL=https://github.com/xev777/TrafficBar
AppSupportURL=https://github.com/xev777/TrafficBar/issues
VersionInfoVersion={#AppVersion}.0
VersionInfoCompany=Fernando Erazo
VersionInfoProductName=TrafficBar
VersionInfoDescription=TrafficBar installer
VersionInfoCopyright=Copyright (C) 2026 Fernando Erazo. GNU GPL v3.
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
; Program Files: only an administrator can modify the installed files (see SEGURIDAD.md, S3)
PrivilegesRequired=admin
; The bundled Python runtime does not run on Windows 7/8/8.1: say so clearly instead of a cryptic missing-DLL error
MinVersion=10.0
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=Output
OutputBaseFilename=TrafficBar-Setup-{#AppVersion}
SetupIconFile=trafficbar.ico
UninstallDisplayIcon={app}\{#AppExe}
Compression=lzma2/ultra
SolidCompression=yes
WizardStyle=modern
CloseApplications=no
RestartApplications=no
; Always ask the language, and start in English (do not follow the Windows language)
ShowLanguageDialog=yes
LanguageDetectionMethod=none

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[CustomMessages]
english.TaskDesktop=Create a desktop shortcut
spanish.TaskDesktop=Crear un acceso directo en el escritorio
english.TaskAutostart=Start TrafficBar with Windows (stays in the system tray)
spanish.TaskAutostart=Iniciar TrafficBar con Windows (queda en la bandeja del sistema)
english.RunNow=Open TrafficBar now
spanish.RunNow=Abrir TrafficBar ahora
english.NpcapAsk=TrafficBar is installed.%n%nThe traffic monitor ("Traffic") also needs Npcap, a free packet-capture driver from npcap.com that is not part of TrafficBar. The rest of the features work without it.%n%nDownload Npcap from npcap.com and start its installer now? You will see Npcap's own license and setup screens.
spanish.NpcapAsk=TrafficBar está instalado.%n%nEl monitor de tráfico ("Tráfico") necesita además Npcap, un controlador gratuito de captura de paquetes de npcap.com que no forma parte de TrafficBar. El resto de funciones no lo necesita.%n%n¿Descargar Npcap desde npcap.com y abrir su instalador ahora? Verás la licencia y las pantallas del propio Npcap.
english.NpcapDownloading=Downloading Npcap from npcap.com...
spanish.NpcapDownloading=Descargando Npcap desde npcap.com...
english.NpcapFailed=Npcap could not be downloaded or verified (no Internet connection, or the file did not match the expected checksum). Nothing was run.%n%nYou can install it later from https://npcap.com and the traffic monitor will work after that.
spanish.NpcapFailed=No se pudo descargar o verificar Npcap (sin conexión a Internet, o el archivo no coincide con la suma de control esperada). No se ejecutó nada.%n%nPuedes instalarlo más tarde desde https://npcap.com y el monitor de tráfico funcionará después.
english.DeleteData=Do you also want to delete your TrafficBar settings and history?%n%n
spanish.DeleteData=¿Quieres borrar también tu configuración y tu historial de TrafficBar?%n%n

[Tasks]
Name: "desktopicon"; Description: "{cm:TaskDesktop}"; Flags: unchecked
Name: "autostart"; Description: "{cm:TaskAutostart}"; Flags: unchecked

[Files]
Source: "dist\TrafficBar\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; GPL-3.0: the license text and third-party notices travel with the binary
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENCIAS-TERCEROS.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
; Start with Windows is registered by the app itself with YOUR user (not the administrator account that
; elevates the installer): HKCU only, no extra permissions, removed on uninstall.
Filename: "{app}\{#AppExe}"; Parameters: "--activar-inicio"; Flags: runhidden runasoriginaluser waituntilterminated; Tasks: autostart
Filename: "{app}\{#AppExe}"; Description: "{cm:RunNow}"; Flags: nowait postinstall skipifsilent runasoriginaluser

[UninstallRun]
Filename: "{app}\{#AppExe}"; Parameters: "--desactivar-inicio"; Flags: runhidden; RunOnceId: "QuitarInicio"
; Removes the Windows Firewall rules TrafficBar created ("TrafficBar block: ...")
Filename: "{app}\{#AppExe}"; Parameters: "--quitar-bloqueos"; Flags: runhidden waituntilterminated; RunOnceId: "QuitarBloqueos"
; Removes the Microsoft Store apps loopback exemptions TrafficBar created
Filename: "{app}\{#AppExe}"; Parameters: "--quitar-exenciones"; Flags: runhidden waituntilterminated; RunOnceId: "QuitarExenciones"

[UninstallDelete]
Type: files; Name: "{app}\idioma.txt"

[Code]
// Closes TrafficBar before installing/updating/uninstalling. First it asks TrafficBar to give Windows back its
// proxy setting (otherwise an abrupt close could leave you without Internet).
procedure DetenerTrafficBar(const Carpeta: String);
var
  Codigo: Integer;
begin
  if FileExists(Carpeta + '\{#AppExe}') then
    Exec(Carpeta + '\{#AppExe}', '--restaurar-proxy', '', SW_HIDE, ewWaitUntilTerminated, Codigo);
  Exec(ExpandConstant('{sys}\taskkill.exe'), '/F /IM {#AppExe}', '', SW_HIDE, ewWaitUntilTerminated, Codigo);
  Sleep(800);
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  DetenerTrafficBar(ExpandConstant('{app}'));
  Result := '';
end;

function InitializeUninstall(): Boolean;
begin
  DetenerTrafficBar(ExpandConstant('{app}'));
  Result := True;
end;

// Offers Npcap (needed only by the traffic monitor). Asks first; downloads the official installer from npcap.com, runs it
// only if its SHA-256 matches the pinned one, and lets the user go through Npcap's own license and setup screens.
procedure OfrecerNpcap;
var
  Archivo: String;
  Codigo: Integer;
begin
  if MsgBox(CustomMessage('NpcapAsk'), mbConfirmation, MB_YESNO) <> IDYES then
    Exit;
  try
    WizardForm.StatusLabel.Caption := CustomMessage('NpcapDownloading');
    DownloadTemporaryFile('https://npcap.com/dist/npcap-{#NpcapVersion}.exe', 'npcap-{#NpcapVersion}.exe', '{#NpcapSha256}', nil);
    Archivo := ExpandConstant('{tmp}\npcap-{#NpcapVersion}.exe');
    if not Exec(Archivo, '', '', SW_SHOWNORMAL, ewWaitUntilTerminated, Codigo) then
      MsgBox(CustomMessage('NpcapFailed'), mbError, MB_OK);
  except
    MsgBox(CustomMessage('NpcapFailed'), mbError, MB_OK);
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  Codigo: String;
begin
  if CurStep = ssPostInstall then
  begin
    // App language chosen in the wizard (the user can change it later from the bar)
    if ActiveLanguage = 'spanish' then Codigo := 'es' else Codigo := 'en';
    SaveStringToFile(ExpandConstant('{app}\idioma.txt'), Codigo, False);
    if (not DirExists(ExpandConstant('{sys}\Npcap'))) and (not WizardSilent) then
      OfrecerNpcap;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  Datos: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    Datos := ExpandConstant('{localappdata}\{#AppName}');
    // In a silent uninstall it NEVER asks or deletes anything of yours
    if (not UninstallSilent()) and DirExists(Datos) and
       (MsgBox(CustomMessage('DeleteData') + Datos, mbConfirmation, MB_YESNO or MB_DEFBUTTON2) = IDYES) then
      DelTree(Datos, True, True, True);
  end;
end;
