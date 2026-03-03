"""Global keyboard listener module for capturing key events."""

from pynput import keyboard
from PyQt6.QtCore import QObject, pyqtSignal


class SignalEmitter(QObject):
    """Qt signal emitter for keyboard events."""
    
    enter_pressed = pyqtSignal()
    log_message = pyqtSignal(str)
    status_update = pyqtSignal(str)


class GlobalKeyListener:
    """Listens for global keyboard events using pynput."""

    def __init__(self, emitter: SignalEmitter) -> None:
        """
        Initialize keyboard listener.
        
        Args:
            emitter: Signal emitter for Qt events
        """
        self.emitter = emitter
        self.listener = None

    def _on_press(self, key) -> None:
        """
        Handle key press events.
        
        Args:
            key: The key that was pressed
        """
        try:
            if key == keyboard.Key.enter:
                self.emitter.enter_pressed.emit()
        except AttributeError:
            pass

    def start(self) -> None:
        """Start listening for keyboard events."""
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def stop(self) -> None:
        """Stop listening for keyboard events."""
        if self.listener:
            self.listener.stop()