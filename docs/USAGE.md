# Usage Guide

Complete guide for using GTA5RP Admin Tool.

## Starting the Application

```bash
python main.py
```

## Main Window

The main window displays:
- Current statistics (Day/Week/Month)
- Log of recent activities
- Control buttons
- Resolution selector
- Norm timer

### Statistics Display

- **Day**: Reports closed today
- **Week**: Reports closed this week (ISO week)
- **Month**: Reports closed this month

### Control Buttons

- **+1**: Manually add one report
- **-1**: Manually remove one report
- **Set**: Set today's count to specific value
- **Reset All**: Clear all statistics (confirmation required)

### Resolution Selector

Choose your screen resolution:
- Full HD (1920x1080)
- 4K (3840x2160)

This affects the screenshot capture area for OCR.

## Overlay Window

A transparent overlay appears on the right side of your screen showing:
- Current day's report count
- Updates in real-time

The overlay:
- Stays on top of all windows
- Doesn't interfere with clicks
- Can't be accidentally closed

## Automatic Report Detection

1. Open a report in-game
2. Press **Enter** key
3. Application captures screenshot
4. OCR processes the image
5. If new report ID found, counter increments

### What Happens

```
Enter pressed → Screenshot captured → OCR processing → 
Report ID extracted → Check if new → Update counter
```

### Log Messages

- `Enter pressed → capturing screenshot...` - Screenshot started
- `🔄 Processing screenshot...` - OCR in progress
- `Found report #12345` - Report ID detected
- `New report #12345 counted` - Counter incremented
- `Report #12345 already counted — skipping` - Duplicate detected
- `⚠️ Report not found in text` - No report in screenshot
- `❌ OCR Error: ...` - OCR service error

## Norm Timer

Tracks your playtime to meet the 4-hour norm.

### Features

- Starts automatically when game launches
- Pauses when game closes
- Shows progress as percentage
- Displays overtime after norm completion
- Pause/Resume button for manual control

### Timer Display

- `Norm: 2:30:00 / 4:00:00 (62%)` - In progress
- `Norm: 4:00:00 / 4:00:00 (100%)` - Completed
- `Norm: 4:30:00 / 4:00:00 (112%) +0:30:00` - Overtime

### Detected Game Processes

- GTA5.exe
- ragemp_v.exe (RAGE Multiplayer)

## Manual Operations

### Adding Reports

Click **+1** button or use it to correct missed detections.

### Removing Reports

Click **-1** button to remove the last report added today.

### Setting Exact Count

1. Click **Set** button
2. Enter desired count in dialog
3. Click OK

This adjusts today's count to match the specified value.

### Resetting Statistics

1. Click **Reset All** button
2. Confirm in dialog
3. All statistics cleared

**Warning**: This action cannot be undone!

## Keyboard Shortcuts

- **Enter** (global): Trigger screenshot and OCR

## Tips and Best Practices

### For Best OCR Accuracy

1. Use native screen resolution
2. Ensure report text is clearly visible
3. Avoid overlapping windows
4. Wait for report to fully load before pressing Enter

### Managing API Limits

Free OCR.space tier has limits:
- 500 requests per day
- 25,000 per month

To conserve requests:
- Only press Enter when viewing a new report
- Use manual +1/-1 for corrections
- Consider self-hosted OCR endpoint for unlimited usage

### Custom OCR Endpoint

If you have your own OCR service:

1. Edit `.env`:
   ```env
   OCR_ENDPOINT=http://your-server:5000/ocr
   ```

2. Endpoint should accept POST with `image` file
3. Return JSON with `text` field or OCR.space format

## Troubleshooting

### Reports Not Detected

- Check resolution setting matches your screen
- Ensure report text is visible in screenshot area
- Verify OCR API key is valid
- Check internet connection

### Duplicate Reports

The application tracks seen report IDs to prevent duplicates. If you need to re-count a report:
1. Restart the application
2. Or manually use +1 button

### Timer Not Starting

- Verify game process name matches detected processes
- Check if game is actually running
- Try manual pause/resume

### Overlay Not Visible

- Check if overlay is behind other windows
- Verify screen resolution
- Try restarting application

## Database

Statistics are stored in `reports.db` SQLite database.

### Backup

To backup your statistics:
```bash
cp reports.db reports_backup.db
```

### Restore

To restore from backup:
```bash
cp reports_backup.db reports.db
```

### Manual Database Access

Using SQLite browser or command line:
```bash
sqlite3 reports.db
SELECT * FROM reports;
```

## Logs

Application logs are saved to `app.log`.

View recent logs:
```bash
tail -f app.log  # Linux/macOS
Get-Content app.log -Tail 20 -Wait  # Windows PowerShell
```

## Advanced Configuration

Edit `configs/config.py` for advanced settings:
- Database path
- Game process names
- Norm duration
- Screen regions

## Getting Help

- Check [FAQ](FAQ.md)
- Open an issue on [GitHub](https://github.com/rizzanrv/gta5rp-admin-tool/issues)
- Contact via Telegram: [@unbrokenflex](https://t.me/unbrokenflex)
