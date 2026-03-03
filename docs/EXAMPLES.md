# Usage Examples

Practical examples of using GTA5RP Admin Tool.

## Basic Usage

### Starting Your Shift

1. Launch the application:
   ```bash
   python main.py
   ```

2. The main window appears with:
   - Statistics showing 0/0/0 (day/week/month)
   - Status: "Ready. Waiting for Enter..."
   - Norm timer at 0:00:00

3. Start the game (GTA5.exe or RAGE Multiplayer)
   - Norm timer automatically starts counting

4. Open your first report in-game

5. Press **Enter** to detect the report
   - Screenshot captured
   - OCR processes the image
   - Counter increments if new report found

### During Your Shift

**Scenario 1: Normal Report Processing**
```
1. Open report #12345
2. Press Enter
3. Log shows: "Found report #12345"
4. Log shows: "New report #12345 counted"
5. Statistics update: Day: 1
```

**Scenario 2: Duplicate Report**
```
1. Open same report #12345 again
2. Press Enter
3. Log shows: "Found report #12345"
4. Log shows: "Report #12345 already counted — skipping"
5. Statistics unchanged
```

**Scenario 3: OCR Miss**
```
1. Open report but text not visible
2. Press Enter
3. Log shows: "⚠️ Report not found in text"
4. Manually click +1 button
5. Statistics update: Day: 2
```

### Ending Your Shift

1. Check your statistics:
   - Day: 15 reports
   - Week: 87 reports
   - Month: 342 reports

2. Check norm timer:
   - "Norm: 4:15:00 / 4:00:00 (106%) +0:15:00"
   - You've completed norm with 15 minutes overtime

3. Close the game
   - Timer automatically pauses

4. Close the application
   - All data saved to database

## Advanced Usage

### Manual Corrections

**Adding Missed Reports**
```
Situation: OCR missed a report
Solution: Click +1 button
Result: Counter increments by 1
```

**Removing False Positives**
```
Situation: Report was counted twice
Solution: Click -1 button
Result: Most recent report for today removed
```

**Setting Exact Count**
```
Situation: Need to sync with external system
Steps:
1. Click "Set" button
2. Enter exact count (e.g., 15)
3. Click OK
Result: Today's count set to 15
```

### Resolution Management

**Switching Resolutions**
```
Situation: Changed monitor or resolution
Steps:
1. Select new resolution from dropdown
2. Test with Enter press
3. Verify OCR works correctly
```

**Custom Resolution**
```
Situation: Using non-standard resolution
Solution: Edit ocr/processor.py
Add your resolution to SCREEN_REGIONS:
"Custom": (0, 0, 2560, 1440)
```

### Norm Timer Management

**Manual Pause**
```
Situation: Taking a break but game still running
Steps:
1. Click "Pause" button
2. Timer stops counting
3. Click "Resume" when back
```

**Checking Progress**
```
During shift: "Norm: 2:30:00 / 4:00:00 (62%)"
After norm: "Norm: 4:00:00 / 4:00:00 (100%)"
Overtime: "Norm: 5:00:00 / 4:00:00 (125%) +1:00:00"
```

## Troubleshooting Examples

### OCR Not Working

**Problem**: Reports not detected

**Diagnosis**:
```
1. Check log for errors
2. Verify API key in .env
3. Test API manually:
   curl -X POST https://api.ocr.space/parse/image \
     -F "apikey=YOUR_KEY" \
     -F "language=rus" \
     -F "file=@test.jpg"
```

**Solutions**:
- Wrong resolution: Change in dropdown
- API limit reached: Wait or upgrade
- Network issue: Check connection
- Text not visible: Adjust game settings

### Database Issues

**Problem**: Statistics not saving

**Diagnosis**:
```
1. Check if reports.db exists
2. Check file permissions
3. Look for errors in app.log
```

**Solutions**:
```bash
# Reset database
rm reports.db
python main.py

# Backup database
cp reports.db reports_backup_$(date +%Y%m%d).db

# Restore database
cp reports_backup_20260303.db reports.db
```

### Timer Not Working

**Problem**: Norm timer not counting

**Diagnosis**:
```
1. Check if game process is running
2. Verify process name matches
3. Check app.log for errors
```

**Solutions**:
```python
# Edit configs/config.py
GAME_PROCESSES = [
    "GTA5.exe",
    "ragemp_v.exe",
    "YourCustomProcess.exe"  # Add your process
]
```

## Integration Examples

### Custom OCR Endpoint

**Setup Local OCR Service**:
```python
# simple_ocr_server.py
from flask import Flask, request, jsonify
import pytesseract
from PIL import Image

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No image'}), 400
    
    image = Image.open(request.files['image'])
    text = pytesseract.image_to_string(image, lang='rus')
    
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(port=5000)
```

**Configure Application**:
```env
# .env
OCR_ENDPOINT=http://localhost:5000/ocr
```

### Database Export

**Export to CSV**:
```python
import sqlite3
import csv
from datetime import datetime

conn = sqlite3.connect('reports.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM reports')
rows = cursor.fetchall()

with open(f'reports_export_{datetime.now():%Y%m%d}.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Timestamp', 'Day', 'Week', 'Month'])
    writer.writerows(rows)

conn.close()
print('Export completed')
```

### Statistics API

**Create Simple API**:
```python
from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/stats')
def get_stats():
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM reports WHERE day = date("now")')
    today = cursor.fetchone()[0]
    
    conn.close()
    return jsonify({'today': today})

if __name__ == '__main__':
    app.run(port=8000)
```

## Automation Examples

### Auto-Start with Windows

**Create Shortcut**:
1. Right-click `main.py`
2. Create shortcut
3. Move to: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

**Or use Task Scheduler**:
```xml
<!-- task.xml -->
<Task>
  <Triggers>
    <LogonTrigger />
  </Triggers>
  <Actions>
    <Exec>
      <Command>C:\path\to\venv\Scripts\python.exe</Command>
      <Arguments>C:\path\to\main.py</Arguments>
    </Exec>
  </Actions>
</Task>
```

### Scheduled Backups

**Windows Task Scheduler**:
```batch
@echo off
set BACKUP_DIR=C:\Backups\GTA5RP
set DATE=%date:~-4,4%%date:~-10,2%%date:~-7,2%
copy reports.db "%BACKUP_DIR%\reports_%DATE%.db"
```

**Linux Cron**:
```bash
# Backup daily at 2 AM
0 2 * * * cp /path/to/reports.db /backups/reports_$(date +\%Y\%m\%d).db
```

## Best Practices

### Daily Routine

1. **Start of Shift**:
   - Launch application
   - Verify overlay visible
   - Check previous day's stats
   - Start game

2. **During Shift**:
   - Press Enter for each new report
   - Monitor log for issues
   - Use manual +1 if OCR misses
   - Check norm timer progress

3. **End of Shift**:
   - Review final statistics
   - Check norm completion
   - Backup database (optional)
   - Close application

### Weekly Maintenance

1. Check API usage
2. Review app.log for errors
3. Backup database
4. Update application if needed
5. Clean old log files

### Monthly Review

1. Export statistics to CSV
2. Analyze trends
3. Optimize OCR settings if needed
4. Update dependencies
5. Archive old backups

## Tips and Tricks

### Improving OCR Accuracy

1. Use native resolution
2. Increase in-game text size
3. Use high contrast settings
4. Ensure good lighting
5. Avoid window overlaps

### Conserving API Calls

1. Only press Enter for new reports
2. Use manual buttons for corrections
3. Don't spam Enter key
4. Consider local OCR for high volume

### Performance Optimization

1. Close unnecessary applications
2. Use SSD for database
3. Keep Python updated
4. Monitor memory usage
5. Regular database maintenance

### Data Management

1. Regular backups
2. Export monthly statistics
3. Archive old data
4. Monitor database size
5. Validate data integrity
