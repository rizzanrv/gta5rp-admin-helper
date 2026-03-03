# Frequently Asked Questions

## General Questions

### What is this application for?

GTA5RP Admin Tool helps server administrators track closed reports and monitor playtime norms automatically using OCR technology.

### Is it free?

Yes, the application is free and open source under MIT license. However, the OCR.space API has usage limits on the free tier.

### Does it work with other games/servers?

The application is specifically designed for GTA5RP but could be adapted for similar use cases with modifications to the OCR pattern matching.

## Installation & Setup

### What Python version do I need?

Python 3.9 or higher is required.

### Where do I get an OCR API key?

Sign up for free at [OCR.space](https://ocr.space/ocrapi). The free tier includes 25,000 requests per month.

### Can I use my own OCR service?

Yes! Set the `OCR_ENDPOINT` in your `.env` file to point to your custom OCR service.

### Do I need to install anything else?

No, all dependencies are listed in `requirements.txt` and installed via pip.

## Usage

### Why isn't my report being detected?

Common reasons:
- Wrong resolution setting
- Report text not visible in screenshot
- OCR API rate limit reached
- Network connectivity issues
- Report text obscured by other windows

### Can I use a different hotkey instead of Enter?

Currently, only Enter is supported. This may be configurable in future versions.

### How do I change the overlay position?

Currently, the overlay is positioned on the right side of the screen. You can modify `ui/overlay.py` to change the position.

### Does the application work with multiple monitors?

The application captures from the primary monitor. Multi-monitor support may be added in future versions.

## Technical Questions

### Where is my data stored?

All statistics are stored locally in `reports.db` SQLite database in the project directory.

### Is my data sent anywhere?

Only screenshots are sent to the OCR API for text recognition. No other data is transmitted.

### Can I export my statistics?

Currently, you can access the SQLite database directly. CSV/Excel export may be added in future versions.

### How much disk space does it use?

Minimal - the database file is typically under 1MB. Temporary screenshots are deleted after processing.

### Does it affect game performance?

No, the application runs independently and only captures screenshots when you press Enter.

## Troubleshooting

### "OCR_API_KEY not found" error

Make sure you:
1. Created `.env` file from `.env.example`
2. Added your API key to the file
3. Saved the file

### "Module not found" errors

Run:
```bash
pip install -r requirements.txt
```

### Application won't start

Check:
1. Python version (3.9+)
2. All dependencies installed
3. `.env` file configured
4. Check `app.log` for errors

### Overlay not showing

Try:
1. Restarting the application
2. Checking if it's behind other windows
3. Verifying screen resolution settings

### Timer not tracking game time

Verify:
1. Game process name matches (GTA5.exe or ragemp_v.exe)
2. Game is actually running
3. Try manual pause/resume

### High API usage

Each Enter press = 1 API request. To reduce usage:
- Only press Enter for new reports
- Use manual +1/-1 for corrections
- Consider self-hosted OCR endpoint

## Privacy & Security

### Is my screen being recorded?

No. Screenshots are only captured when you press Enter and are immediately deleted after OCR processing.

### What permissions does it need?

- Screen capture (for screenshots)
- Keyboard monitoring (for Enter key)
- Network access (for OCR API)
- File system (for database)

### Is it safe to use?

Yes, the code is open source and can be reviewed. The application only sends screenshots to OCR API and stores statistics locally.

### Can I use it without internet?

No, internet connection is required for OCR API calls. However, you could set up a local OCR service.

## Development

### Can I contribute?

Yes! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### How do I report bugs?

Open an issue on [GitHub](https://github.com/rizzanrv/gta5rp-admin-tool/issues) with:
- Description of the problem
- Steps to reproduce
- Your environment details
- Relevant log entries

### Can I request features?

Absolutely! Open a feature request issue on GitHub.

### How do I build an executable?

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## API Limits

### What are OCR.space free tier limits?

- 500 requests per day
- 25,000 requests per month
- Max file size: 1MB

### What happens if I exceed limits?

OCR requests will fail until the limit resets. Consider:
- Upgrading to paid tier
- Using custom OCR endpoint
- Reducing usage

### How do I check my API usage?

Log in to your OCR.space dashboard to view usage statistics.

## Still Have Questions?

- Check the [documentation](USAGE.md)
- Open an issue on [GitHub](https://github.com/rizzanrv/gta5rp-admin-tool/issues)
- Contact via Telegram: [@unbrokenflex](https://t.me/unbrokenflex)
