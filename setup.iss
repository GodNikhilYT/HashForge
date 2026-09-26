#define MyAppName "HashForge"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "HashForge"
#define MyAppExeName "HashForge.exe"

[Setup]
AppId={{B7E9F4A1-6D8C-4F2B-91E5-HASHFORGE2026}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\HashForge
DefaultGroupName=HashForge

OutputDir=D:\EX-Project\Hash Forge Pro\installer
OutputBaseFilename=HashForge_Setup

Compression=lzma
SolidCompression=yes

SetupIconFile=D:\EX-Project\Hash Forge Pro\logo.ico

UninstallDisplayIcon={app}\HashForge.exe

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

PrivilegesRequired=admin

DisableProgramGroupPage=yes

WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "D:\EX-Project\Hash Forge Pro\dist\HashForge.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autodesktop}\HashForge"; Filename: "{app}\HashForge.exe"; WorkingDir: "{app}"
Name: "{group}\HashForge"; Filename: "{app}\HashForge.exe"; WorkingDir: "{app}"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Icons]
Name: "{autodesktop}\HashForge"; Filename: "{app}\HashForge.exe"; WorkingDir: "{app}"; Tasks: desktopicon
Name: "{group}\HashForge"; Filename: "{app}\HashForge.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\HashForge.exe"; Description: "Launch HashForge"; Flags: nowait postinstall skipifsilent