# Installation Guide

Detailed installation instructions for GTA5RP Admin Tool.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (optional, for cloning repository)

## Platform-Specific Instructions

### Windows

1. Install Python from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. Open Command Prompt or PowerShell

3. Clone or download the repository:
   ```bash
   git clone https://github.com/rizzanrv/gta5rp-admin-tool.git
   cd gta5rp-admin-tool
   ```

4. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Configure environment:
   ```bash
   copy .env.example .env
   notepad .env
   ```
   Add your OCR API key to the `.env` file.

### Linux

1. Install Python and pip:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv git
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/rizzanrv/gta5rp-admin-tool.git
   cd gta5rp-admin-tool
   ```

3. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure environment:
   ```bash
   cp .env.example .env
   nano .env
   ```
   Add your OCR API key to the `.env` file.

### macOS

1. Install Python using Homebrew:
   ```bash
   brew install python3
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/rizzanrv/gta5rp-admin-tool.git
   cd gta5rp-admin-tool
   ```

3. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure environment:
   ```bash
   cp .env.example .env
   nano .env
   ```
   Add your OCR API key to the `.env` file.

## Getting OCR API Key

1. Visit [OCR.space](https://ocr.space/ocrapi)
2. Sign up for a free account
3. Copy your API key from the dashboard
4. Paste it into your `.env` file

Free tier limitations:
- 25,000 requests per month
- 500 requests per day
- Max file size: 1MB

## Verifying Installation

Run the application:
```bash
python main.py
```

You should see:
- Main application window
- Transparent overlay on screen
- "Ready. Waiting for Enter..." status message

## Troubleshooting

### Import Errors

If you get import errors:
```bash
pip install --upgrade -r requirements.txt
```

### Permission Errors (Linux/macOS)

The application needs accessibility permissions:
- macOS: System Preferences → Security & Privacy → Privacy → Accessibility
- Linux: May need to run with appropriate permissions

### OCR API Errors

- Verify your API key is correct in `.env`
- Check your internet connection
- Ensure you haven't exceeded API rate limits

### Database Errors

If database initialization fails:
```bash
rm reports.db
python main.py
```

## Building Executable (Optional)

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name GTA5RP-Admin-Tool main.py
```

The executable will be in the `dist/` folder.

## Next Steps

- Read [USAGE.md](USAGE.md) for usage instructions
- Check [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute
- Report issues on [GitHub](https://github.com/rizzanrv/gta5rp-admin-tool/issues)
