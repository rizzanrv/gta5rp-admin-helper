# Architecture Overview

This document describes the architecture and design decisions of GTA5RP Admin Tool.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Main Window                          │
│                    (app/main_window.py)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Statistics  │  │  Controls    │  │  Norm Timer  │      │
│  │  Display     │  │  (+1/-1/Set) │  │  Display     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│   Keyboard   │      │     OCR      │     │   Database   │
│   Listener   │      │  Processor   │     │   Manager    │
│              │      │              │     │              │
│  (pynput)    │      │  (PIL +      │     │  (aiosqlite) │
│              │      │   requests)  │     │              │
└──────────────┘      └──────────────┘     └──────────────┘
        │                     │                     │
        │                     ▼                     │
        │             ┌──────────────┐              │
        │             │  OCR.space   │              │
        │             │     API      │              │
        │             └──────────────┘              │
        │                                           │
        └───────────────────┬───────────────────────┘
                            ▼
                    ┌──────────────┐
                    │   Overlay    │
                    │   Window     │
                    │              │
                    │  (PyQt6)     │
                    └──────────────┘
```

## Components

### 1. Main Window (`app/main_window.py`)

**Responsibility**: Application orchestration and UI management

**Key Features**:
- Initializes all components
- Manages UI state and updates
- Coordinates between components
- Handles user interactions
- Manages norm timer

**Dependencies**:
- PyQt6 for UI
- Database Manager for statistics
- OCR Processor for report detection
- Keyboard Listener for input
- Overlay Window for display

### 2. OCR Processor (`ocr/processor.py`)

**Responsibility**: Screenshot capture and text recognition

**Key Features**:
- Captures screen regions based on resolution
- Sends images to OCR API
- Parses OCR responses
- Detects report IDs using regex
- Prevents duplicate counting
- Handles multiple OCR endpoint formats

**Design Decisions**:
- Runs in background thread to avoid blocking UI
- Uses Qt signals for thread-safe communication
- Maintains set of seen report IDs
- Supports both OCR.space and custom endpoints

### 3. Database Manager (`database/manager.py`)

**Responsibility**: Persistent storage of report statistics

**Key Features**:
- Async SQLite operations
- CRUD operations for reports
- Statistics aggregation by day/week/month
- Atomic transactions

**Schema**:
```sql
CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    day TEXT NOT NULL,
    iso_week TEXT NOT NULL,
    month TEXT NOT NULL
)
```

**Design Decisions**:
- Uses aiosqlite for async operations
- Stores ISO week format for accurate weekly stats
- Separate columns for day/week/month for efficient queries

### 4. Keyboard Listener (`input/key_listener.py`)

**Responsibility**: Global keyboard event monitoring

**Key Features**:
- Listens for Enter key globally
- Emits Qt signals on key press
- Non-blocking operation

**Design Decisions**:
- Uses pynput for cross-platform support
- Runs in separate thread
- Only monitors Enter key to minimize overhead

### 5. Overlay Window (`ui/overlay.py`)

**Responsibility**: Always-on-top display of current statistics

**Key Features**:
- Transparent background
- Always on top
- Non-interactive
- Auto-positioning

**Design Decisions**:
- Frameless window for clean look
- Right-side positioning for visibility
- No taskbar presence
- Can't steal focus

### 6. Configuration (`configs/config.py`)

**Responsibility**: Centralized configuration management

**Key Features**:
- Environment variable loading
- Type-safe constants
- Validation on startup

**Design Decisions**:
- Uses python-dotenv for .env support
- Fails fast on missing required config
- Immutable configuration (Final types)

## Data Flow

### Report Detection Flow

```
1. User presses Enter
   ↓
2. Keyboard Listener emits signal
   ↓
3. Main Window receives signal
   ↓
4. OCR Processor captures screenshot
   ↓
5. Screenshot sent to OCR API
   ↓
6. OCR response parsed for report ID
   ↓
7. Check if report ID is new
   ↓
8. If new: Database Manager increments count
   ↓
9. Statistics updated in UI and Overlay
```

### Statistics Update Flow

```
1. Database operation completes
   ↓
2. Main Window calls get_statistics()
   ↓
3. Database Manager queries aggregated data
   ↓
4. Statistics returned to Main Window
   ↓
5. UI labels updated
   ↓
6. Overlay window updated
```

## Threading Model

- **Main Thread**: Qt event loop, UI updates
- **Keyboard Listener Thread**: pynput keyboard monitoring
- **OCR Processing Thread**: Screenshot capture and API calls
- **Async Operations**: Database operations (via asyncio)

## Error Handling

### Levels

1. **Fatal Errors**: Missing configuration, startup failures
   - Application exits with error message
   - Logged to console and file

2. **Recoverable Errors**: OCR failures, network issues
   - Logged with context
   - User notified via UI
   - Operation can be retried

3. **Warnings**: Duplicate reports, file cleanup issues
   - Logged for debugging
   - User may be notified
   - Operation continues

### Logging Strategy

- **INFO**: Normal operations, statistics updates
- **DEBUG**: Detailed flow, API responses
- **WARNING**: Recoverable issues, duplicates
- **ERROR**: Failed operations, API errors
- **CRITICAL**: Fatal errors, startup failures

## Design Patterns

### Observer Pattern
- Qt signals/slots for event communication
- Decouples components
- Thread-safe by design

### Repository Pattern
- Database Manager abstracts data access
- Single source of truth for statistics
- Easy to test and mock

### Strategy Pattern
- OCR endpoint can be swapped
- Resolution settings configurable
- Extensible for new features

## Security Considerations

1. **API Keys**: Stored in .env, never committed
2. **Screenshots**: Temporary files, deleted after use
3. **Database**: Local only, no remote access
4. **Permissions**: Minimal required (screen, keyboard, network)

## Performance Considerations

1. **Screenshot Capture**: Only on demand (Enter press)
2. **Database Queries**: Indexed by day/week/month
3. **OCR Processing**: Async, non-blocking
4. **Memory**: Temporary files cleaned up
5. **CPU**: Background threads for heavy operations

## Extensibility Points

1. **New OCR Providers**: Implement endpoint adapter
2. **Additional Statistics**: Extend database schema
3. **Custom Hotkeys**: Modify keyboard listener
4. **UI Themes**: Extend stylesheet system
5. **Export Formats**: Add export methods to Database Manager

## Testing Strategy

### Unit Tests
- Database operations
- OCR text parsing
- Configuration validation

### Integration Tests
- Component interaction
- Database persistence
- Signal/slot communication

### Manual Tests
- UI responsiveness
- OCR accuracy
- Cross-platform compatibility

## Future Improvements

1. **Multi-language Support**: i18n framework
2. **Plugin System**: Extensible architecture
3. **Cloud Sync**: Optional remote backup
4. **Advanced Analytics**: Charts and graphs
5. **Customizable UI**: Theme system
6. **Hotkey Configuration**: User-defined shortcuts
7. **System Tray**: Minimize to tray option
