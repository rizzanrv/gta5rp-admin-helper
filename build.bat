@echo off
chcp 65001 > nul

echo ========================================
echo GTA5RP Admin Tool - Build Script
echo ========================================
echo.

REM Check if main.py exists
if not exist "main.py" (
    echo [ERROR] main.py not found. Run this script from project root.
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] PyInstaller not found. Installing...
    pip install pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo [INFO] Cleaning previous builds...
rmdir /s /q build 2> nul
rmdir /s /q dist 2> nul
del /q *.spec 2> nul

echo [INFO] Building executable...
echo.

pyinstaller ^
    --noconsole ^
    --onefile ^
    --name "GTA5RP-Admin-Tool" ^
    --clean ^
    --noconfirm ^
    --add-data "configs;configs" ^
    --hidden-import=PyQt6 ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=pynput ^
    --hidden-import=pynput.keyboard ^
    --hidden-import=requests ^
    --hidden-import=PIL ^
    --hidden-import=aiosqlite ^
    --hidden-import=psutil ^
    --hidden-import=dotenv ^
    --collect-all PyQt6 ^
    main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Build failed. Check output above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [SUCCESS] Build completed!
echo ========================================
echo.
echo Executable location: dist\GTA5RP-Admin-Tool.exe
echo.
echo IMPORTANT: Don't forget to create .env file next to the executable!
echo.
echo Next steps:
echo 1. Copy .env.example to dist\.env
echo 2. Add your OCR API key to dist\.env
echo 3. Test the executable
echo.
pause