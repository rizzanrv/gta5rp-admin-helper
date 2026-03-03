import asyncio
import datetime
import psutil
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QHBoxLayout, QSpinBox, QComboBox, QApplication
)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import QTimer, Qt

from database.manager import DatabaseManager
from ocr.processor import OCRProcessor
from ui.overlay import OverlayWindow
from input.key_listener import GlobalKeyListener, SignalEmitter


class ReportCounterApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("GTA5RP Admin Tool")
        self.setGeometry(100, 100, 550, 500)
        self._apply_dark_theme()

        self.db = DatabaseManager()
        asyncio.run(self.db.initialize())

        self.emitter = SignalEmitter()
        self.key_listener = GlobalKeyListener(self.emitter)
        self.key_listener.start()

        self.ocr = OCRProcessor(on_new_report_callback=self._on_new_report)
        self.ocr.signals.log_message.connect(self._log)
        self.ocr.signals.status_update.connect(self._set_status)

        self.overlay = OverlayWindow()

        self._setup_ui()
        self._setup_timers()

        self.NORM_SECONDS = 4 * 3600
        self.elapsed_seconds = 0
        self.is_game_running = False
        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self._check_game_and_update_timer)
        self.game_timer.start(1000)
        self.norm_paused = False

        self._update_statistics_display()
        self._update_overlay()

        self.emitter.enter_pressed.connect(self._on_enter_pressed)
        self.emitter.log_message.connect(self._log)
        self.emitter.status_update.connect(self._set_status)

    def _apply_dark_theme(self) -> None:
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(60, 60, 60))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(70, 130, 180))
        QApplication.setPalette(palette)

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()

        self.status_label = QLabel("Готово. Нажмите Enter")
        self.status_label.setFont(QFont("Arial", 11))
        layout.addWidget(self.status_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(self.log_text)

        self.stats_label = QLabel("Статистика: ...")
        layout.addWidget(self.stats_label)

        self.norm_timer_label = QLabel("Норма: 0:00:00 / 4:00:00")
        self.norm_timer_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.norm_timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.norm_timer_label.setStyleSheet("color: #ffcc00;")
        layout.addWidget(self.norm_timer_label)

        self.overtime_label = QLabel("")
        self.overtime_label.setFont(QFont("Arial", 11))
        self.overtime_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.overtime_label.setStyleSheet("color: #00ff00;")
        layout.addWidget(self.overtime_label)
        self.pause_norm_btn = QPushButton("⏸ Пауза нормы")
        self.pause_norm_btn.clicked.connect(self._toggle_norm_pause)
        layout.addWidget(self.pause_norm_btn)

        res_layout = QHBoxLayout()
        res_layout.addWidget(QLabel("Разрешение экрана:"))
        self.res_combo = QComboBox()
        self.res_combo.addItems(["Full HD (1920x1080)", "4K (3840x2160)"])
        self.res_combo.currentIndexChanged.connect(self._change_resolution)
        res_layout.addWidget(self.res_combo)
        layout.addLayout(res_layout)

        control_layout = QHBoxLayout()
        self.plus_btn = QPushButton("+1")
        self.plus_btn.clicked.connect(self._manual_add)
        control_layout.addWidget(self.plus_btn)

        self.minus_btn = QPushButton("-1")
        self.minus_btn.clicked.connect(self._manual_sub)
        control_layout.addWidget(self.minus_btn)
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Сегодня", "Неделя", "Месяц"])
        control_layout.addWidget(self.period_combo)

        self.set_spin = QSpinBox()
        self.set_spin.setRange(0, 9999)
        control_layout.addWidget(self.set_spin)

        self.set_btn = QPushButton("Установить сегодня")
        self.set_btn.clicked.connect(self._manual_set)
        control_layout.addWidget(self.set_btn)
        layout.addLayout(control_layout)

        reset_btn = QPushButton("Сбросить ВСЁ (осторожно!)")
        reset_btn.setStyleSheet("color: red;")
        reset_btn.clicked.connect(self._reset_all)
        layout.addWidget(reset_btn)

        author_label = QLabel(
            "Разработчик: игрок La Puerta — Zatru Swearvyan (#10717)<br>"
            "Telegram: <a href='https://t.me/unbrokenflex' style='color: #70a1ff;'>https://t.me/unbrokenflex</a>"
        )
        author_label.setOpenExternalLinks(True)
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        author_label.setFont(QFont("Arial", 9))
        author_label.setStyleSheet("color: #aaaaaa;")
        layout.addWidget(author_label)

        central.setLayout(layout)

    def _setup_timers(self) -> None:
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self._update_statistics_display)
        self.stats_timer.start(2000)

        self.overlay_timer = QTimer()
        self.overlay_timer.timeout.connect(self._update_overlay)
        self.overlay_timer.start(2000)

    def _check_game_and_update_timer(self) -> None:
        current_running = any(
            proc.info["name"].lower() in {"gta5.exe", "ragemp.exe", "rage-multiplayer.exe"}
            for proc in psutil.process_iter(['name'])
        )

        if current_running and not self.is_game_running:
            self.is_game_running = True
            self.emitter.log_message.emit("Игра запущена — таймер нормы стартовал")
        elif not current_running and self.is_game_running:
            self.is_game_running = False
            self.emitter.log_message.emit("Игра закрыта — таймер нормы приостановлен")

        if self.is_game_running and not self.norm_paused:
            self.elapsed_seconds += 1

        self._update_norm_timer_display()

    def _update_norm_timer_display(self) -> None:
        if self.elapsed_seconds < self.NORM_SECONDS:
            hours_elapsed = self.elapsed_seconds // 3600
            minutes_elapsed = (self.elapsed_seconds % 3600) // 60
            seconds_elapsed = self.elapsed_seconds % 60
            self.norm_timer_label.setText(
                f"Норма: {hours_elapsed:01d}:{minutes_elapsed:02d}:{seconds_elapsed:02d} / 4:00:00"
            )
            self.norm_timer_label.setStyleSheet("color: #ffcc00;")
            self.overtime_label.setText("")
        else:
            overtime = self.elapsed_seconds - self.NORM_SECONDS
            hours = overtime // 3600
            minutes = (overtime % 3600) // 60
            seconds = overtime % 60
            self.norm_timer_label.setText("Норма: 4:00:00 / 4:00:00")
            self.norm_timer_label.setStyleSheet("color: #00ff00;")
            self.overtime_label.setText(f"Сверх нормы: +{hours:01d}:{minutes:02d}:{seconds:02d}")

    def _change_resolution(self, index: int) -> None:
        resolutions = ["Full HD", "4K"]
        self.ocr.set_resolution(resolutions[index])
        self.emitter.log_message.emit(f"Разрешение установлено: {resolutions[index]}")

    def _log(self, message: str) -> None:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

    def _toggle_norm_pause(self) -> None:
        self.norm_paused = not self.norm_paused

        if self.norm_paused:
            self.pause_norm_btn.setText("▶ Продолжить норму")
            self.emitter.log_message.emit("⏸ Таймер нормы поставлен на паузу")
        else:
            self.pause_norm_btn.setText("⏸ Пауза нормы")
            self.emitter.log_message.emit("▶ Таймер нормы продолжен")

    def _set_status(self, text: str) -> None:
        self.status_label.setText(text)

    def _on_enter_pressed(self) -> None:
        self.ocr.process_screenshot()

    def _on_new_report(self) -> None:
        asyncio.run(self._handle_new_report_async())

    async def _handle_new_report_async(self) -> None:
        await self.db.increment()
        stats = await self.db.get_statistics()
        self.stats_label.setText(f"📊 Сегодня: {stats['day']} | Неделя: {stats['week']} | Месяц: {stats['month']}")
        self.overlay.update_count(stats["day"])
        self.emitter.log_message.emit("Новый репорт обнаружен и учтён")

    def _manual_add(self) -> None:
        asyncio.run(self.db.increment())
        self._update_statistics_display()
        self._update_overlay()
        self.emitter.log_message.emit("➕ Ручное +1")

    def _manual_sub(self) -> None:
        asyncio.run(self.db.decrement())
        self._update_statistics_display()
        self._update_overlay()
        self.emitter.log_message.emit("➖ Ручное -1")

    def _manual_set(self) -> None:
        value = self.set_spin.value()
        asyncio.run(self.db.set_today_to(value))
        self._update_statistics_display()
        self._update_overlay()
        self.emitter.log_message.emit(f"🔢 Установлено вручную: {value}")

    def _reset_all(self) -> None:
        asyncio.run(self.db.reset_all())
        self._update_statistics_display()
        self._update_overlay()
        self.emitter.log_message.emit("🗑️ Вся статистика сброшена!")

    def _update_statistics_display(self) -> None:
        stats = asyncio.run(self.db.get_statistics())
        self.stats_label.setText(f"📊 Сегодня: {stats['day']} | Неделя: {stats['week']} | Месяц: {stats['month']}")

    def _update_overlay(self) -> None:
        stats = asyncio.run(self.db.get_statistics())
        self.overlay.update_count(stats["day"])

    def closeEvent(self, event) -> None:
        self.key_listener.stop()
        self.game_timer.stop()
        self.overlay.close()
        event.accept()