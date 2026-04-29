"""
PyForge Academy — entry point.

Run:
    python main.py

Prerequisites:
    pip install PySide6
    # For the AI tutor:
    # 1. Install Ollama:  https://ollama.com/download
    # 2. Pull the model:  ollama pull mistral
    # 3. Start the daemon if it's not already running: ollama serve
"""

from __future__ import annotations

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPalette, QColor
from PySide6.QtWidgets import QApplication

from pyforge import theme
from pyforge.main_window import MainWindow


def _enable_high_dpi():
    # PySide6 ≥ 6.0 enables High-DPI by default on most platforms.
    os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")


def main() -> int:
    _enable_high_dpi()
    app = QApplication(sys.argv)
    app.setApplicationName("PyForge Academy")
    app.setOrganizationName("PyForge")
    app.setApplicationDisplayName("PyForge Academy")
    app.setStyle("Fusion")

    # Dark Fusion palette — better than the default on Windows/Linux
    pal = QPalette()
    pal.setColor(QPalette.Window,           QColor(theme.BG_DEEP))
    pal.setColor(QPalette.WindowText,       QColor(theme.TEXT_PRIMARY))
    pal.setColor(QPalette.Base,             QColor(theme.BG_ELEVATED))
    pal.setColor(QPalette.AlternateBase,    QColor(theme.BG_PANEL))
    pal.setColor(QPalette.Text,             QColor(theme.TEXT_PRIMARY))
    pal.setColor(QPalette.Button,           QColor(theme.BG_ELEVATED))
    pal.setColor(QPalette.ButtonText,       QColor(theme.TEXT_PRIMARY))
    pal.setColor(QPalette.Highlight,        QColor(theme.ACCENT))
    pal.setColor(QPalette.HighlightedText,  QColor("white"))
    pal.setColor(QPalette.ToolTipBase,      QColor(theme.BG_PANEL))
    pal.setColor(QPalette.ToolTipText,      QColor(theme.TEXT_PRIMARY))
    app.setPalette(pal)

    app.setStyleSheet(theme.global_stylesheet())

    win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
