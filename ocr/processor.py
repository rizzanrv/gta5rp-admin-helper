"""OCR processing module for screenshot capture and text recognition."""

import os
import re
import time
import logging
import threading
from typing import Optional, Callable, Set
import requests
from PIL import ImageGrab
from PyQt6.QtCore import QObject, pyqtSignal

from configs.config import OCR_API_KEY, OCR_LANGUAGE, OCR_ENGINE, OCR_ENDPOINT

logger = logging.getLogger(__name__)


class OCRSignals(QObject):
    """Qt signals for OCR processor events."""
    
    log_message = pyqtSignal(str)
    status_update = pyqtSignal(str)


class OCRProcessor:
    """Handles screenshot capture and OCR text recognition."""
    
    SCREEN_REGIONS = {
        "Full HD": (0, 0, 1920, 1080),
        "4K": (0, 0, 3840, 2160)
    }

    def __init__(
        self, 
        resolution: str = "Full HD", 
        on_new_report_callback: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Initialize OCR processor.
        
        Args:
            resolution: Screen resolution preset ("Full HD" or "4K")
            on_new_report_callback: Callback function to execute when new report is detected
        """
        self.resolution = resolution
        self.screen_region = self.SCREEN_REGIONS[self.resolution]
        self.last_report_id: Optional[int] = None
        self.on_new_report = on_new_report_callback
        self.seen_report_ids: Set[int] = set()
        self.signals = OCRSignals()

    def set_resolution(self, resolution: str) -> None:
        """
        Update screen resolution settings.
        
        Args:
            resolution: Screen resolution preset ("Full HD" or "4K")
        """
        self.resolution = resolution
        self.screen_region = self.SCREEN_REGIONS[self.resolution]

    def process_screenshot(self) -> None:
        """Start screenshot processing in a background thread."""
        threading.Thread(target=self._process, daemon=True).start()

    def _process(self) -> None:
        """Internal method to process screenshot and perform OCR."""
        path = "temp_screenshot.jpg"

        self.signals.log_message.emit("Enter pressed → capturing screenshot...")
        self.signals.status_update.emit("🔄 Processing screenshot...")
        logger.info("Starting screenshot capture and OCR processing")

        try:
            screenshot = ImageGrab.grab(bbox=self.screen_region)
            screenshot.save(path)
            logger.debug(f"Screenshot saved to {path}")

            with open(path, "rb") as f:
                # Use custom endpoint if configured, otherwise use OCR.space API
                if OCR_ENDPOINT.startswith("http://") or OCR_ENDPOINT.startswith("https://"):
                    response = requests.post(
                        OCR_ENDPOINT,
                        files={"image": f},
                        data={
                            "apikey": OCR_API_KEY,
                            "language": OCR_LANGUAGE,
                            "OCREngine": OCR_ENGINE,
                        },
                        timeout=10
                    )
                else:
                    # Fallback to default OCR.space endpoint
                    response = requests.post(
                        "https://api.ocr.space/parse/image",
                        files={"image": f},
                        data={
                            "apikey": OCR_API_KEY,
                            "language": OCR_LANGUAGE,
                            "OCREngine": OCR_ENGINE,
                        },
                        timeout=10
                    )

            if response.status_code != 200:
                error_msg = f"❌ OCR server returned {response.status_code}"
                self.signals.log_message.emit(error_msg)
                logger.error(error_msg)
                return

            result = response.json()
            logger.debug(f"OCR response: {result}")

            # Handle OCR.space API response format
            if "ParsedResults" in result:
                if not result.get("ParsedResults"):
                    self.signals.log_message.emit("⚠️ OCR returned empty results")
                    return
                text = result["ParsedResults"][0].get("ParsedText", "")
            else:
                # Handle custom endpoint format
                if "error" in result:
                    error_msg = f"❌ OCR Error: {result['error']}"
                    self.signals.log_message.emit(error_msg)
                    logger.error(error_msg)
                    return
                text = result.get("text", "")

            if not text.strip():
                self.signals.log_message.emit("⚠️ OCR returned empty text")
                logger.warning("Empty OCR result")
                return

            self.signals.log_message.emit(f"OCR: {repr(text[:80])}...")
            logger.debug(f"OCR text: {text[:200]}")

            # Search for report ID pattern
            match = re.search(r"Репорт\s*#(\d+)", text, re.IGNORECASE)
            if not match:
                self.signals.log_message.emit("⚠️ Report not found in text")
                logger.debug("No report pattern found in OCR text")
                return

            current_id = int(match.group(1))
            self.signals.log_message.emit(f"Found report #{current_id}")
            logger.info(f"Detected report ID: {current_id}")

            if current_id in self.seen_report_ids:
                self.signals.log_message.emit(
                    f"Report #{current_id} already counted — skipping"
                )
                logger.debug(f"Report {current_id} already seen")
                return

            self.seen_report_ids.add(current_id)
            self.signals.log_message.emit(
                f"New report #{current_id} counted"
            )
            logger.info(f"New report {current_id} added to counter")

            if self.on_new_report:
                self.on_new_report()

        except Exception as e:
            error_msg = f"💥 Error: {e}"
            self.signals.log_message.emit(error_msg)
            logger.exception("Error during OCR processing")

        finally:
            # Clean up temporary screenshot file
            if os.path.exists(path):
                for attempt in range(5):
                    try:
                        os.remove(path)
                        logger.debug(f"Temporary file {path} removed")
                        break
                    except PermissionError:
                        logger.warning(f"Failed to remove {path}, attempt {attempt + 1}/5")
                        time.sleep(0.5)
                else:
                    warning_msg = f"⚠️ Could not delete {path} after retries"
                    self.signals.log_message.emit(warning_msg)
                    logger.error(warning_msg)

            self.signals.status_update.emit("Ready. Waiting for Enter...")
