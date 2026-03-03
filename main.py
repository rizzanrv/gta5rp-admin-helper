"""Main application entry point."""

import sys
import logging
from PyQt6.QtWidgets import QApplication

from app.main_window import ReportCounterApp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        logger.info("Starting GTA5RP Admin Tool")
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        window = ReportCounterApp()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logger.exception("Fatal error during application startup")
        sys.exit(1)