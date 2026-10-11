 <p align="center">
  <img width="140" alt="HashForge Logo" src="https://github.com/user-attachments/assets/e3f7db16-feaa-47fd-b2fd-f3fa3850f880" />
</p>

<h1 align="center">HashForge</h1>

<p align="center">
  <strong>Professional Multi-Algorithm File Hash Generator</strong>
</p>

<p align="center">
  Generate file hashes locally, verify file integrity, export reports, and manage file-analysis workflows with a modern Windows desktop application.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0.1-00B4FF?style=for-the-badge" alt="Version 2.0.1">
  <img src="https://img.shields.io/badge/Release-Available-success?style=for-the-badge" alt="Release Available">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge" alt="Windows">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/UI-Tkinter-2C2C2C?style=for-the-badge" alt="Tkinter">
  <img src="https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge" alt="Proprietary License">
</p>

<p align="center">
  <a href="https://github.com/GodNikhilYT/HashForge/releases/latest">
    <img src="https://img.shields.io/badge/Download-HashForge_v2.0.1-087F6B?style=for-the-badge" alt="Download HashForge v2.0.1">
  </a>
</p>

---

## 📥 Download HashForge v2.0.1

**Latest version: v2.0.1**

Download HashForge for Windows from the official GitHub Releases page.

### Installation

1. Open the [HashForge Releases](https://github.com/GodNikhilYT/HashForge/releases/latest) page.
2. Download `HashForge_Setup_v2.0.1.exe` from the release assets.
3. Double-click the downloaded installer.
4. Follow the installation wizard.
5. Launch HashForge from the Start Menu or desktop shortcut.

> **Note:** The installer must be uploaded to the GitHub Release before the download will be available. If the asset is missing, check the repository's Releases page.

---

## 📌 About

**HashForge** is a Windows desktop application for file-integrity verification and cryptographic hashing.

It provides a desktop interface for generating hash values from local files and supports workflows for scanning, verification, report exporting, history management, and duplicate-file analysis, depending on the features enabled in the current build.

The core hashing workflow is designed to process files locally without requiring them to be uploaded to a remote hashing service.

---

## ✨ Features

### 🔐 File Hashing
- Generate hash values for local files.
- Multi-algorithm hashing support.
- Local file-processing workflow.
- File-integrity verification.
- File and folder scanning, where enabled.

### 🖥️ Professional Dashboard
- Modern Tkinter desktop interface.
- Dashboard statistics.
- Sidebar navigation.
- Scan, Verify, Export, History, Duplicates, and Settings sections.
- Custom HashForge logo and application icon.
- Multiple interface themes, where supported by the build.

### 📊 Reports & History
- Export hash results.
- PDF reports, where enabled.
- CSV reports, where enabled.
- Scan history management.
- Duplicate-file analysis.

### 📦 Windows Application
- Standalone executable packaging with PyInstaller.
- Windows installer created with Inno Setup.
- Start Menu shortcut.
- Optional desktop shortcut.
- Custom application branding.
- Uninstaller support.

### 🔄 Automatic Updates

HashForge can use GitHub Releases as a distribution channel for new application versions when the updater is included and configured in the build.

Expected update workflow:

```text
New HashForge Version
          |
          v
     GitHub Release
          |
          v
    Check for Updates
          |
          v
 Update Available Notice
          |
          v
   Download Installer
          |
          v
    Install New Version
```

The automatic update workflow requires a correctly configured updater, compatible version checking, and a published installer asset.

---

## 🧮 Supported Hash Algorithms

HashForge uses Python's `hashlib` architecture. The algorithms available in a particular release depend on the application implementation and runtime environment.

| Algorithm | Digest Size |
|---|---:|
| MD5 | 128 bits |
| SHA-1 | 160 bits |
| SHA-224 | 224 bits |
| SHA-256 | 256 bits |
| SHA-384 | 384 bits |
| SHA-512 | 512 bits |

**Security recommendation:** Use SHA-256 or stronger for security-sensitive integrity verification. MD5 and SHA-1 are not recommended when collision resistance is required.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Tkinter | Desktop GUI |
| `hashlib` | Hash generation |
| Pillow | Image and logo handling |
| ReportLab | PDF report generation, where enabled |
| PyInstaller | Executable packaging |
| Inno Setup | Windows installer creation |
| GitHub Releases | Release distribution |

---

## 📂 Project Structure

The development project may contain the following files:

```text
HashForge/
│
├── ver16.py
├── hashforge_updater.py
├── logo.ico
├── logo.jpeg
├── build.bat
├── setup.iss
├── README.md
├── LICENSE.txt
├── .gitignore
│
├── build/
├── dist/
└── installer/
```

The exact project structure depends on the current source version. Files such as `hashforge_updater.py` should only be included if they actually exist in the repository.

Build-generated folders such as `build/`, `dist/`, and `installer/` can be excluded from source-control commits unless they are intentionally used to distribute release artifacts.

---

## 💻 Run From Source

### Requirements

- Windows
- Python 3.x
- Pillow
- PyInstaller for executable builds
- ReportLab if PDF reporting is enabled

### Install dependencies

Open Command Prompt in the project directory and run:

```bash
python -m pip install --upgrade pillow pyinstaller reportlab
```

### Launch HashForge

Run the current application source:

```bash
python ver16.py
```

Make sure the filename matches the Python file in your project.

---

## 📦 Build the Windows EXE

If the project includes a configured `build.bat`, execute:

```bat
build.bat
```

Alternatively, for a compatible application using `ver16.py`, `logo.ico`, and `logo.jpeg`:

```bat
python -m PyInstaller --noconfirm --clean --onefile --windowed --name HashForge --icon "logo.ico" --add-data "logo.ico;." --add-data "logo.jpeg;." "ver16.py"
```

The expected output is:

```text
dist\HashForge.exe
```

Test the executable before creating the installer. Additional dependencies or data files may need to be included according to the application source.

---

## 🧰 Build the Windows Installer

HashForge uses Inno Setup to package the standalone executable into a Windows installer.

1. Build the application using PyInstaller.
2. Confirm that `dist\HashForge.exe` exists.
3. Open `setup.iss` in Inno Setup Compiler.
4. Check the icon and executable paths.
5. Compile the script.
6. Test installation, launching, and uninstallation.

Expected installer filename:

```text
HashForge_Setup_v2.0.1.exe
```

The installer should include the standalone executable and create shortcuts according to the selected setup options.

Users should not need a separate Python installation when the application and its required dependencies are correctly bundled.

---

## 🔄 GitHub Releases & Versioning

**Repository:** [GodNikhilYT/HashForge](https://github.com/GodNikhilYT/HashForge)

- [View all releases](https://github.com/GodNikhilYT/HashForge/releases)
- [Download the latest release](https://github.com/GodNikhilYT/HashForge/releases/latest)
- [View repository source code](https://github.com/GodNikhilYT/HashForge/tree/main)

### Publishing a release

1. Update the application version.
2. Update the version in the Inno Setup script.
3. Build the standalone executable.
4. Compile and test the installer.
5. Create a Git tag such as `v2.0.1`.
6. Create a GitHub Release for that tag.
7. Upload `HashForge_Setup_v2.0.1.exe` as a release asset.
8. Verify the release page and download link.

Keep the application version, installer version, and release tag synchronized.

For future releases, use a higher version number than the previously published version.

---

## 🔒 Security & Integrity

- Use the same hashing algorithm when comparing files.
- Matching hash values indicate matching digests, but do not independently prove that a file is trustworthy.
- Use SHA-256 or stronger when appropriate for security-sensitive integrity checking.
- Download installers from trusted release sources.
- Consider code-signing the executable and installer for production distribution.
- Restrict access to official release publishing permissions.

---

## 🛡️ Privacy

The core hashing workflow is designed for local file processing. Network activity may occur if a particular build implements update checking or other online functionality.

Review the actual source code and release configuration before making broader claims about data collection or network behavior.

---

## 📄 License

HashForge is proprietary software.

**Copyright © 2026 Nikhil Choudhary. All rights reserved.**

See [LICENSE.txt](https://github.com/GodNikhilYT/HashForge/blob/main/LICENSE.txt) for the complete license terms.

Third-party libraries remain subject to their respective licenses.

---

## 👨‍💻 Author

**Nikhil Choudhary**

HashForge — Professional File Integrity & Hashing Software

[GitHub Repository](https://github.com/GodNikhilYT/HashForge)

---

## ⚠️ Disclaimer

HashForge is intended for legitimate file-integrity verification, software development, testing, and administrative purposes.

Users are responsible for ensuring that their use of the application complies with applicable laws, organizational policies, and third-party software licenses.
