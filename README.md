# GTA5RP Admin Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A desktop application for GTA5RP server administrators to automatically track closed reports and monitor playtime norms using OCR technology.

> **Quick Start**: See [QUICKSTART.md](QUICKSTART.md) for 5-minute setup guide.

The application uses OCR to recognize report numbers on screen and automatically increments the counter when a new ID is detected. Features include manual adjustments, statistics display for day/week/month, and a transparent overlay showing the current day's report count.

---

## 👤 Developer

**La Puerta Player — Zatru Swearvyan (#10717)**

[![Telegram](https://img.shields.io/badge/Telegram-@unbrokenflex-2CA5E0?logo=telegram&logoColor=white)](https://t.me/unbrokenflex)  
[![GitHub](https://img.shields.io/badge/GitHub-rizzanrv-181717?logo=github&logoColor=white)](https://github.com/rizzanrv)

---

## ✨ Features

- 🔍 Automatic report detection via Enter key press
- 🤖 Text recognition through OCR.space API or custom endpoint
- 💾 Local SQLite database for statistics storage
- 📊 Statistics display in main window and transparent overlay
- 🖥️ Support for Full HD and 4K resolutions
- ✏️ Manual operations: +1, -1, set exact value, full reset
- ⏱️ Playtime norm timer (4 hours) - only counts when game is running
- 📈 Progress display with overtime tracking after norm completion
- 🎨 Dark theme interface
- 🏗️ Modular architecture for easy maintenance and extension

---

## 📋 Requirements

- Python 3.9+
- PyQt6
- pynput
- requests
- Pillow
- aiosqlite
- psutil (for game process detection)

See [requirements.txt](requirements.txt) for exact versions.

---

## 🚀 Installation

Quick start:

```bash
git clone https://github.com/rizzanrv/gta5rp-admin-tool.git
cd gta5rp-admin-tool
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your OCR API key
```

For detailed installation instructions, see [docs/INSTALLATION.md](docs/INSTALLATION.md).

---

## ▶️ Usage

```bash
python main.py
```

For complete usage guide, see [docs/USAGE.md](docs/USAGE.md).

---

## 📚 Documentation

- **[Quick Start](QUICKSTART.md)** - Get started in 5 minutes
- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [Usage Guide](docs/USAGE.md) - How to use the application
- [Examples](docs/EXAMPLES.md) - Practical usage examples
- [Architecture](docs/ARCHITECTURE.md) - Technical architecture overview
- [FAQ](docs/FAQ.md) - Frequently asked questions
- [Contributing](CONTRIBUTING.md) - How to contribute
- [Changelog](CHANGELOG.md) - Version history
- [Security Policy](SECURITY.md) - Security information
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community guidelines

---

## 🗂️ Project Structure

```
gta5rp-admin-tool/
├── main.py                    # Entry point
├── configs/
│   └── config.py              # OCR API configuration (via .env)
├── app/
│   └── main_window.py         # Main window and orchestration
├── ui/
│   └── overlay.py             # Transparent overlay
├── input/
│   └── key_listener.py        # Global keyboard listener
├── ocr/
│   └── processor.py           # Screenshot capture and OCR processing
├── database/
│   └── manager.py             # SQLite database operations
└── utils/
    └── __init__.py            # Reserved for utilities
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OCR Configuration
OCR_API_KEY=your_api_key_here
OCR_LANGUAGE=rus
OCR_ENGINE=2
OCR_ENDPOINT=  # Optional: custom OCR endpoint
```

### Supported Resolutions

- Full HD (1920x1080)
- 4K (3840x2160)

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📝 Notes

- On first run, `reports.db` database file is automatically created in the project root
- Norm timer only runs during active game sessions
- Application doesn't collect or transmit any data except OCR API requests
- Add `.env` to `.gitignore` to keep your API key secure (already configured)
- Logs are saved to `app.log` for troubleshooting

For more details, see [docs/FAQ.md](docs/FAQ.md).

---

## 🐛 Known Issues

- OCR accuracy depends on screen resolution and text clarity
- Temporary screenshot file may occasionally fail to delete on Windows (permission issues)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [OCR.space](https://ocr.space/) for providing free OCR API
- PyQt6 for the GUI framework
- GTA5RP community

---

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Contact via Telegram: [@unbrokenflex](https://t.me/unbrokenflex)

---

**Made with ❤️ for GTA5RP administrators**
