"""Transparent overlay window for displaying report count."""

from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class OverlayWindow(QWidget):
    """Transparent overlay displaying the current day's report count."""

    def __init__(self) -> None:
        """Initialize overlay window."""
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.label = QLabel("Today: 0", self)
        self.label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.label.setStyleSheet("color: white;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.setFixedSize(300, 60)
        self.label.setGeometry(0, 0, 300, 60)

        # Position overlay on the right side of the screen, vertically centered
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 30
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        self.show()

    def update_count(self, count: int) -> None:
        """
        Update the displayed report count.
        
        Args:
            count: Number of reports to display
        """
        self.label.setText(f"{count}")
