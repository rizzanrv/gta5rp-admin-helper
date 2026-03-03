# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-03

### Added
- Initial release
- Automatic report detection via OCR
- Support for Full HD and 4K resolutions
- Local SQLite database for statistics
- Transparent overlay window
- Playtime norm timer (4 hours)
- Manual report adjustments (+1, -1, set value)
- Statistics display (day/week/month)
- Dark theme interface
- Global keyboard listener for Enter key
- Game process detection (GTA5.exe, RAGE Multiplayer)
- Configurable OCR endpoint support
- Comprehensive logging system
- Type hints throughout codebase
- Full documentation and docstrings

### Changed
- Migrated from PyQt5 to PyQt6
- Improved error handling and logging
- Enhanced code structure with proper type hints
- Better configuration management via .env

### Fixed
- Temporary screenshot file cleanup issues
- OCR API response handling for multiple formats

## [Unreleased]

### Planned
- Multi-language support for UI
- Custom screenshot regions
- Export statistics to CSV/Excel
- Dark/Light theme toggle
- Hotkey customization
- System tray integration
