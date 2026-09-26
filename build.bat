@echo off
title HashForge - EXE Builder
color 0A

echo ============================================
echo        HASHFORGE - EXE BUILD SYSTEM
echo ============================================
echo.

cd /d "D:\EX-Project\Hash Forge Pro"

echo [1/4] Checking project files...
if not exist "ver15.py" (
    echo ERROR: ver15.py not found!
    pause
    exit /b 1
)

if not exist "logo.ico" (
    echo ERROR: logo.ico not found!
    pause
    exit /b 1
)

if not exist "logo.jpeg" (
    echo ERROR: logo.jpeg not found!
    pause
    exit /b 1
)

echo Project files found.
echo.

echo [2/4] Installing/updating PyInstaller...
python -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo ERROR: PyInstaller installation failed.
    pause
    exit /b 1
)

echo.

echo [3/4] Cleaning previous build...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "HashForge.spec" del /q "HashForge.spec"

echo.

echo [4/4] Building HashForge.exe...
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --clean ^
    --name "HashForge" ^
    --icon="logo.ico" ^
    --add-data "logo.ico;." ^
    --add-data "logo.jpeg;." ^
    "ver15.py"

if errorlevel 1 (
    echo.
    echo ============================================
    echo       BUILD FAILED
    echo ============================================
    pause
    exit /b 1
)

echo.
echo ============================================
echo       BUILD SUCCESSFUL
echo ============================================
echo.
echo EXE created at:
echo D:\EX-Project\Hash Forge Pro\dist\HashForge.exe
echo.

pause