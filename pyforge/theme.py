"""
Theme tokens and global stylesheet for PyForge Academy.
Redesigned with a premium Midnight Indigo aesthetic.
"""

# ---------- Color tokens ----------
BG_DEEP        = "#020617"   # Slate 950 - Deepest navy
BG_PANEL       = "#0F172A"   # Slate 900 - Dark panel
BG_ELEVATED    = "#1E293B"   # Slate 800 - Elevated surface
BG_HOVER       = "#334155"   # Slate 700 - Hover state
BORDER         = "#1E293B"   # Subtle borders
BORDER_BRIGHT  = "#8B5CF6"   # Violet 500 accent

TEXT_PRIMARY   = "#F8FAFC"   # Slate 50 - High contrast text
TEXT_MUTED     = "#94A3B8"   # Slate 400 - Lower contrast
TEXT_DIM       = "#475569"   # Slate 600 - Dimmed text

ACCENT         = "#8B5CF6"   # Violet 500
ACCENT_HOVER   = "#A78BFA"   # Violet 400
ACCENT_SOFT    = "rgba(139, 92, 246, 0.12)"

SUCCESS        = "#10B981"   # Emerald 500
WARNING        = "#F59E0B"   # Amber 500
DANGER         = "#EF4444"   # Red 500
INFO           = "#0EA5E9"   # Sky 500

# Syntax-highlight palette (Modern Dark)
SYN_KEYWORD    = "#C084FC"  # Purple
SYN_STRING     = "#FDE047"  # Yellow
SYN_NUMBER     = "#FB7185"  # Rose
SYN_COMMENT    = "#64748B"  # Slate
SYN_FUNCTION   = "#38BDF8"  # Sky
SYN_BUILTIN    = "#818CF8"  # Indigo
SYN_DECORATOR  = "#F472B6"  # Pink
SYN_OPERATOR   = "#94A3B8"  # Slate
SYN_CLASS      = "#F8FAFC"  # White


def global_stylesheet() -> str:
    """Return the QSS stylesheet applied to the QApplication."""
    return f"""
    QWidget {{
        background-color: {BG_DEEP};
        color: {TEXT_PRIMARY};
        font-family: "Inter", "Segoe UI", system-ui, sans-serif;
        font-size: 13px;
        outline: none;
    }}

    QMainWindow, QDialog {{
        background-color: {BG_DEEP};
    }}

    /* Sidebar list / Tree */
    QListWidget, QTreeWidget {{
        background-color: transparent;
        border: none;
        outline: 0;
        padding: 4px;
    }}
    QListWidget::item, QTreeWidget::item {{
        padding: 10px 12px;
        border-radius: 8px;
        margin: 2px 4px;
        color: {TEXT_MUTED};
        border: 1px solid transparent;
    }}
    QListWidget::item:hover, QTreeWidget::item:hover {{
        background-color: {BG_PANEL};
        color: {TEXT_PRIMARY};
    }}
    QListWidget::item:selected, QTreeWidget::item:selected {{
        background-color: {ACCENT_SOFT};
        color: {ACCENT_HOVER};
        font-weight: bold;
        border: 1px solid {ACCENT};
    }}

    QHeaderView::section {{
        background-color: {BG_DEEP};
        color: {TEXT_MUTED};
        padding: 8px;
        border: none;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 11px;
    }}

    /* Buttons */
    QPushButton {{
        background-color: {BG_ELEVATED};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {BG_HOVER};
        border-color: {TEXT_MUTED};
    }}
    QPushButton:pressed {{
        background-color: {BG_PANEL};
    }}
    QPushButton#PrimaryButton {{
        background-color: {ACCENT};
        color: white;
        border: none;
    }}
    QPushButton#PrimaryButton:hover {{
        background-color: {ACCENT_HOVER};
    }}
    QPushButton#PrimaryButton:pressed {{
        background-color: {ACCENT};
    }}
    QPushButton#GhostButton {{
        background-color: transparent;
        border: 1px solid {BORDER};
        color: {TEXT_MUTED};
    }}
    QPushButton#GhostButton:hover {{
        color: {TEXT_PRIMARY};
        border-color: {TEXT_MUTED};
        background-color: {BG_PANEL};
    }}
    QPushButton:disabled {{
        color: {TEXT_DIM};
        background-color: {BG_DEEP};
        border: 1px solid {BG_PANEL};
    }}

    /* Inputs */
    QLineEdit, QTextEdit, QPlainTextEdit, QTextBrowser {{
        background-color: {BG_PANEL};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 8px;
        selection-background-color: {ACCENT};
        selection-color: white;
    }}
    QPlainTextEdit, QTextEdit {{
        font-family: "JetBrains Mono", "Consolas", monospace;
    }}
    QTextBrowser {{
        line-height: 1.6;
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QTextBrowser:focus {{
        border: 1px solid {ACCENT};
        background-color: {BG_DEEP};
    }}

    /* Splitter */
    QSplitter::handle {{
        background-color: transparent;
    }}
    QSplitter::handle:hover {{
        background-color: {ACCENT_SOFT};
    }}

    /* Tabs */
    QTabWidget::pane {{
        border: 1px solid {BORDER};
        background-color: {BG_PANEL};
        border-radius: 12px;
        top: -1px;
    }}
    QTabBar::tab {{
        background-color: transparent;
        color: {TEXT_MUTED};
        padding: 8px 20px;
        border: none;
        border-bottom: 2px solid transparent;
        font-weight: bold;
        margin-right: 4px;
    }}
    QTabBar::tab:hover {{
        color: {TEXT_PRIMARY};
    }}
    QTabBar::tab:selected {{
        color: {ACCENT_HOVER};
        border-bottom: 2px solid {ACCENT};
    }}

    /* Scrollbars */
    QScrollBar:vertical {{
        background: transparent;
        width: 10px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {BG_ELEVATED};
        border-radius: 5px;
        min-height: 24px;
        margin: 2px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {TEXT_DIM};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 10px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background: {BG_ELEVATED};
        border-radius: 5px;
        min-width: 24px;
        margin: 2px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: {TEXT_DIM};
    }}

    /* Labels */
    QLabel#H1 {{ font-size: 24px; font-weight: 800; color: {TEXT_PRIMARY}; letter-spacing: -0.5px; }}
    QLabel#H2 {{ font-size: 18px; font-weight: 700; color: {TEXT_PRIMARY}; }}
    QLabel#H3 {{ font-size: 14px; font-weight: 600; color: {TEXT_MUTED}; text-transform: uppercase; letter-spacing: 1px; }}
    QLabel#Muted {{ color: {TEXT_MUTED}; font-size: 12px; }}
    QLabel#Tag {{
        background: {ACCENT_SOFT};
        color: {ACCENT_HOVER};
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
    }}
    QLabel#Brand {{
        font-size: 18px;
        font-weight: 900;
        color: {TEXT_PRIMARY};
        padding: 20px 24px;
        background: transparent;
        letter-spacing: -0.5px;
    }}

    /* Group / card */
    QFrame#Card {{
        background-color: {BG_PANEL};
        border: 1px solid {BORDER};
        border-radius: 12px;
    }}
    
    QFrame#SidebarCard {{
        background-color: {BG_DEEP};
        border-right: 1px solid {BORDER};
    }}

    /* Progress bar */
    QProgressBar {{
        background-color: {BG_ELEVATED};
        border: none;
        border-radius: 6px;
        height: 8px;
        text-align: center;
        color: transparent;
    }}
    QProgressBar::chunk {{
        background: {ACCENT};
        border-radius: 6px;
    }}

    /* Combo box */
    QComboBox {{
        background-color: {BG_PANEL};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 6px 12px;
    }}
    QComboBox:hover {{ border-color: {TEXT_MUTED}; }}
    QComboBox QAbstractItemView {{
        background-color: {BG_PANEL};
        border: 1px solid {BORDER};
        selection-background-color: {ACCENT_SOFT};
        selection-color: {ACCENT_HOVER};
        border-radius: 8px;
    }}

    /* Tooltip */
    QToolTip {{
        background-color: {BG_ELEVATED};
        color: {TEXT_PRIMARY};
        border: 1px solid {BORDER};
        padding: 6px 10px;
        border-radius: 6px;
    }}

    /* Status bar */
    QStatusBar {{
        background-color: {BG_DEEP};
        color: {TEXT_MUTED};
        border-top: 1px solid {BORDER};
        padding: 4px 12px;
        font-size: 12px;
    }}
    """
