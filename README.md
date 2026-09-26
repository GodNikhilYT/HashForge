<p align="center">
  <img width="140" alt="Image" src="https://github.com/user-attachments/assets/e3f7db16-feaa-47fd-b2fd-f3fa3850f880" />
</p>

<h1 align="center">HashForge</h1>

<p align="center">
  <strong>Professional Multi-Algorithm File Hash Generator</strong>
</p>

<p align="center">
  Generate file hashes locally, verify file integrity, export reports, and
  manage hashing history from a modern Windows desktop application.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge" alt="Windows">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/UI-Tkinter-2C2C2C?style=for-the-badge" alt="Tkinter">
  <img src="https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge" alt="Proprietary License">
</p>

---

## About

**HashForge** is a Windows desktop application designed for file-integrity
and cryptographic hash workflows.

The application provides a professional dashboard for generating hashes from
local files and is structured to support workflows such as scanning,
verification, exporting reports, history management, and duplicate-file
analysis.

Hashing is performed locally by the application. Files do not need to be
uploaded to a remote hashing service for the core hashing workflow.

> **Project status:** Phase 1 / UI and core project foundation.

---

## Features

### File Hashing
- Generate cryptographic hashes for local files.
- Multi-algorithm hashing architecture.
- Local processing workflow.
- File-based integrity verification foundation.

### Professional Dashboard
- Modern Tkinter desktop interface.
- Dashboard statistics.
- Navigation sidebar.
- Scan, Verify, Export, History, Duplicates, and Settings sections.
- Custom HashForge application icon and branding.

### Reports & History
- Export-oriented architecture for hash results.
- Scan/history workflow foundation.
- Designed for future report enhancements.

### Windows Distribution
- PyInstaller-based executable build.
- Inno Setup installer support.
- Desktop shortcut creation.
- Custom application icon.
- Release-ready installer workflow.

### Automatic Updates
The project includes an updater architecture designed for GitHub Releases.

The intended release workflow is:

```text
New HashForge version
        ↓
GitHub Release
        ↓
HashForge checks for updates
        ↓
Update Available notification
        ↓
HashForge_Setup.exe download
        ↓
Installer starts
        ↓
New version installed
```

Automatic updates require the updater-enabled build and a correctly configured
GitHub repository/release.

---

## Supported Hash Algorithms

The current application is designed around a multi-algorithm hashing workflow.
The exact algorithms enabled in a particular build are determined by the
application source/configuration.

Typical algorithms supported by the Python `hashlib` architecture include:

- MD5
- SHA-1
- SHA-224
- SHA-256
- SHA-384
- SHA-512

> Availability of individual algorithms can depend on the exact HashForge
> build and Python/OpenSSL environment.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Tkinter | Desktop GUI |
| `hashlib` | Cryptographic hashing |
| Pillow | Image/logo handling |
| ReportLab | PDF/report generation where enabled |
| PyInstaller | Windows executable packaging |
| Inno Setup | Windows installer |
| GitHub Releases | Application release/update distribution |

---

## Project Structure

A typical development repository can contain:

```text
HashForge/
│
├── ver15.py
├── hashforge_updater.py
├── logo.ico
├── logo.jpeg
├── build.bat
├── setup.iss
├── README.md
├── LICENSE
├── .gitignore
│
├── build/
├── dist/
└── installer/
```

Build-generated directories such as `build/`, `dist/`, and `installer/` can be
kept out of normal source-control commits when appropriate. See `.gitignore`.

---

## Requirements

For development, install:

- Python 3.x
- Tkinter
- Pillow
- PyInstaller
- ReportLab (if PDF reporting is enabled)

Example:

```bash
python -m pip install --upgrade pillow pyinstaller reportlab
```

Tkinter is normally included with the standard Windows Python distribution.

---

## Run From Source

From the project directory:

```bash
python ver15.py
```

---

## Build the Windows EXE

If the project includes the supplied build script:

```bat
build.bat
```

A PyInstaller build produces:

```text
dist\HashForge.exe
```

The exact build command may vary with the current project configuration.

---

## Build the Windows Installer

After building the executable, open the Inno Setup project:

```text
setup.iss
```

Compile it with Inno Setup Compiler.

The installer can then be distributed as:

```text
HashForge_Setup.exe
```

---

## GitHub Releases & Auto-Update

For the automatic update system, create a GitHub repository and configure
the updater with the repository in this format:

```python
GITHUB_REPOSITORY = "OWNER/REPOSITORY"
```

For example:

```python
GITHUB_REPOSITORY = "GodNikhilYT/HashForge"
```

Use the **actual** repository name in your project.

For a release, the installer asset should use the expected filename:

```text
HashForge_Setup.exe
```

Keep the application version and installer version synchronized for each
release.

Example release progression:

```text
1.0.0 → 1.0.1 → 1.1.0 → 2.0.0
```

Do not publish a release with a lower version number than the currently
installed application.

---

## Security & Integrity

HashForge is intended for local file-integrity workflows.

Important points:

- Hash values depend on the selected hashing algorithm.
- A hash is only useful for comparison when the same algorithm and file
  contents are used.
- MD5 and SHA-1 should not be treated as modern collision-resistant choices
  for security-sensitive applications.
- For security-sensitive integrity verification, prefer a modern algorithm
  such as SHA-256 or stronger where appropriate.
- Keep official installers and releases under controlled repository access.
- For production distribution, code-signing the Windows executable/installer
  is recommended.

---

## Privacy

The core hashing workflow is designed to process files locally.

HashForge should not be described as collecting or transmitting user files
unless a particular version explicitly implements such functionality.

Always review the source code and release configuration before making
privacy claims for a specific production build.

---

## License

HashForge is proprietary software.

Copyright (c) 2026 Nikhil Choudhary. All rights reserved.

See [LICENSE](https://github.com/GodNikhilYT/HashForge/blob/main/LICENSE.txt) for the complete license terms.

Third-party libraries remain subject to their own licenses.

---

## Author

**Nikhil Choudhary**

HashForge — Professional File Integrity & Hashing Software

---

## Disclaimer

HashForge is provided for legitimate file-integrity, development, testing,
and administrative purposes.

Users are responsible for ensuring that their use of the software complies
with applicable laws, organizational policies, and the licenses of any
third-party software or content they use with HashForge.
