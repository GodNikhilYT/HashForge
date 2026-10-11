#define MyAppName "HashForge"
#define MyAppVersion "2.0.1"
#define MyAppPublisher "HashForge"
#define MyAppExeName "HashForge.exe"

[Setup]
AppId={{A8E4F9D2-7B31-4C65-9A12-5F8D3E6B1024}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\HashForge
DefaultGroupName=HashForge
DisableProgramGroupPage=yes
OutputDir=D:\version 2.0.1\installer
OutputBaseFilename=HashForge_Setup_v2.0.1
SetupIconFile=D:\version 2.0.1\logo.ico
UninstallDisplayIcon={app}\HashForge.exe
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
Uninstallable=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "D:\version 2.0.1\dist\HashForge.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\HashForge"; Filename: "{app}\HashForge.exe"
Name: "{autodesktop}\HashForge"; Filename: "{app}\HashForge.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\HashForge.exe"; Description: "Launch HashForge"; Flags: postinstall nowait skipifsilent