# Quick Start Guide

Get up and running with GTA5RP Admin Tool in 5 minutes.

## Prerequisites

- Python 3.9+ installed
- Git (optional)
- OCR.space API key (free)

## Installation (5 steps)

### 1. Get the Code

```bash
git clone https://github.com/rizzanrv/gta5rp-admin-tool.git
cd gta5rp-admin-tool
```

Or download ZIP and extract.

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

```bash
# Copy example config
cp .env.example .env

# Edit .env and add your API key
# Get free key at: https://ocr.space/ocrapi
```

Edit `.env`:
```env
OCR_API_KEY=your_key_here
OCR_LANGUAGE=rus
OCR_ENGINE=2
```

### 5. Run

```bash
python main.py
```

## First Use

1. **Main window appears** - Shows statistics and controls
2. **Overlay appears** - Transparent counter on right side of screen
3. **Start your game** - Timer starts automatically
4. **Open a report** - In-game
5. **Press Enter** - Report detected and counted

## Basic Controls

- **Enter** (anywhere) - Detect report from screenshot
- **+1** button - Manually add report
- **-1** button - Manually remove report
- **Set** button - Set exact count
- **Pause/Resume** - Control norm timer

## Troubleshooting

### "OCR_API_KEY not found"
→ Make sure you created `.env` file and added your API key

### "Module not found"
→ Run `pip install -r requirements.txt`

### Reports not detected
→ Check resolution setting matches your screen (Full HD or 4K)

### Timer not working
→ Make sure game process name is GTA5.exe or ragemp_v.exe

## Next Steps

- Read [full documentation](docs/USAGE.md)
- Check [examples](docs/EXAMPLES.md)
- Join community via [Telegram](https://t.me/unbrokenflex)

## Need Help?

- [FAQ](docs/FAQ.md) - Common questions
- [GitHub Issues](https://github.com/rizzanrv/gta5rp-admin-tool/issues) - Bug reports
- [Telegram](https://t.me/unbrokenflex) - Direct support

---

**That's it! You're ready to track reports efficiently. Good luck!** 🚀
