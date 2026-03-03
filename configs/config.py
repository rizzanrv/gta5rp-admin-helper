"""Configuration module for OCR and application settings."""

import os
from pathlib import Path
from typing import Final
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OCR Configuration
OCR_API_KEY: Final[str] = os.getenv("OCR_API_KEY", "")
OCR_LANGUAGE: Final[str] = os.getenv("OCR_LANGUAGE", "rus")
OCR_ENGINE: Final[str] = os.getenv("OCR_ENGINE", "2")
OCR_ENDPOINT: Final[str] = os.getenv("OCR_ENDPOINT", "https://api.ocr.space/parse/image")

# Database Configuration
DATABASE_PATH: Final[Path] = Path("reports.db")

# Game Process Names
GAME_PROCESSES: Final[list[str]] = ["GTA5.exe", "ragemp_v.exe"]

# Norm Timer (in seconds)
NORM_DURATION: Final[int] = 4 * 60 * 60  # 4 hours

# Validate required configuration
if not OCR_API_KEY:
    raise ValueError(
        "OCR_API_KEY not found in environment variables or .env file. "
        "Please add a valid key from https://ocr.space/ocrapi"
    )