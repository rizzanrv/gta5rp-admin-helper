#!/bin/bash

echo "========================================"
echo "GTA5RP Admin Tool - Build Script"
echo "========================================"
echo

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "[ERROR] main.py not found. Run this script from project root."
    exit 1
fi

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "[INFO] PyInstaller not found. Installing..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install PyInstaller"
        exit 1
    fi
fi

echo "[INFO] Cleaning previous builds..."
rm -rf build dist *.spec

echo "[INFO] Building executable..."
echo

pyinstaller \
    --noconsole \
    --onefile \
    --name "GTA5RP-Admin-Tool" \
    --clean \
    --noconfirm \
    --add-data "configs:configs" \
    --hidden-import=PyQt6 \
    --hidden-import=PyQt6.QtCore \
    --hidden-import=PyQt6.QtGui \
    --hidden-import=PyQt6.QtWidgets \
    --hidden-import=pynput \
    --hidden-import=pynput.keyboard \
    --hidden-import=requests \
    --hidden-import=PIL \
    --hidden-import=aiosqlite \
    --hidden-import=psutil \
    --hidden-import=dotenv \
    --collect-all PyQt6 \
    main.py

if [ $? -ne 0 ]; then
    echo
    echo "[ERROR] Build failed. Check output above."
    exit 1
fi

echo
echo "========================================"
echo "[SUCCESS] Build completed!"
echo "========================================"
echo
echo "Executable location: dist/GTA5RP-Admin-Tool"
echo
echo "IMPORTANT: Don't forget to create .env file next to the executable!"
echo
echo "Next steps:"
echo "1. Copy .env.example to dist/.env"
echo "2. Add your OCR API key to dist/.env"
echo "3. Test the executable"
echo
