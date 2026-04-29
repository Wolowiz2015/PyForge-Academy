"""
Custom Python code editor for PyForge Academy.

Features:
  - Syntax highlighting (keywords, strings, numbers, comments, builtins,
    decorators, function/class names)
  - Line number gutter
  - Current-line highlight
  - Smart auto-indent on newline
  - Tab inserts 4 spaces
  - Monospace font with sane defaults

Kept self-contained — no QScintilla dependency, just QPlainTextEdit + a
QSyntaxHighlighter. Good enough for a learning app, fast to start.
"""

from __future__ import annotations

import builtins
import keyword
import re

from PySide6.QtCore import Qt, QRect, QSize, QRegularExpression
from PySide6.QtGui import (
    QColor, QFont, QPainter, QSyntaxHighlighter,
    QTextCharFormat, QTextCursor, QTextFormat, QPalette,
)
from PySide6.QtWidgets import (
    QPlainTextEdit, QTextEdit, QWidget,
)

from pyforge import theme


# ---------------------------------------------------------------- Highlighter
class PythonHighlighter(QSyntaxHighlighter):
    """Token-level syntax highlighting tuned for the dark theme."""

    def __init__(self, document):
        super().__init__(document)
        self.rules: list[tuple[QRegularExpression, QTextCharFormat]] = []

        def fmt(color: str, bold=False, italic=False) -> QTextCharFormat:
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if bold:
                f.setFontWeight(QFont.Bold)
            f.setFontItalic(italic)
            return f

        # Keywords
        kw_fmt = fmt(theme.SYN_KEYWORD, bold=True)
        for kw in keyword.kwlist:
            self.rules.append((QRegularExpression(rf"\b{kw}\b"), kw_fmt))

        # Builtins
        bi_fmt = fmt(theme.SYN_BUILTIN)
        for bi in dir(builtins):
            if bi.startswith("_"):
                continue
            self.rules.append((QRegularExpression(rf"\b{bi}\b"), bi_fmt))

        # `self` / `cls`
        self.rules.append((
            QRegularExpression(r"\b(self|cls)\b"),
            fmt(theme.INFO, italic=True),
        ))

        # Decorators @something
        self.rules.append((
            QRegularExpression(r"@\w+"),
            fmt(theme.SYN_DECORATOR, bold=True),
        ))

        # Class names: `class Name`
        self.rules.append((
            QRegularExpression(r"\bclass\s+(\w+)"),
            fmt(theme.SYN_CLASS, bold=True),
        ))

        # Function defs: `def name`
        self.rules.append((
            QRegularExpression(r"\bdef\s+(\w+)"),
            fmt(theme.SYN_FUNCTION, bold=True),
        ))

        # Function calls: `name(`
        self.rules.append((
            QRegularExpression(r"\b([A-Za-z_]\w*)(?=\()"),
            fmt(theme.SYN_FUNCTION),
        ))

        # Numbers (int, float, hex, scientific)
        self.rules.append((
            QRegularExpression(r"\b(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?\b|\b0x[\dA-Fa-f]+\b"),
            fmt(theme.SYN_NUMBER),
        ))

        # Strings — single & double quoted (single-line; multiline handled below)
        str_fmt = fmt(theme.SYN_STRING)
        self.rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), str_fmt))
        self.rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), str_fmt))

        # Comments
        self.rules.append((
            QRegularExpression(r"#[^\n]*"),
            fmt(theme.SYN_COMMENT, italic=True),
        ))

        # Multi-line triple-quoted strings handled in highlightBlock state
        self._tri_double = QRegularExpression(r'"""')
        self._tri_single = QRegularExpression(r"'''")
        self._tri_format = str_fmt

    def highlightBlock(self, text: str):
        # Single-line rules first
        for pattern, char_format in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), char_format)

        # Multi-line triple strings (state machine: 0=none, 1=in """, 2=in ''')
        self.setCurrentBlockState(0)
        for state, pat in [(1, self._tri_double), (2, self._tri_single)]:
            start = 0
            if self.previousBlockState() != state:
                m = pat.match(text)
                if not m.hasMatch():
                    continue
                start = m.capturedStart()
                start_after = m.capturedEnd()
            else:
                start_after = 0

            while start_after >= 0:
                m_end = pat.match(text, start_after)
                if m_end.hasMatch():
                    length = m_end.capturedEnd() - start
                    self.setFormat(start, length, self._tri_format)
                    start_after = m_end.capturedEnd()
                    # Look for next opener after this close
                    m_next = pat.match(text, start_after)
                    if not m_next.hasMatch():
                        break
                    start = m_next.capturedStart()
                    start_after = m_next.capturedEnd()
                else:
                    self.setCurrentBlockState(state)
                    self.setFormat(start, len(text) - start, self._tri_format)
                    break


# ---------------------------------------------------------------- Line numbers
class _LineNumberArea(QWidget):
    def __init__(self, editor: "CodeEditor"):
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self) -> QSize:
        return QSize(self._editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self._editor.line_number_area_paint(event)


# ---------------------------------------------------------------- Editor
class CodeEditor(QPlainTextEdit):
    """QPlainTextEdit subclass with line numbers, current line highlight,
    and Python-friendly indent behavior.
    """

    INDENT = "    "

    def __init__(self, parent=None):
        super().__init__(parent)
        self._line_area = _LineNumberArea(self)

        font = QFont("JetBrains Mono", 11)
        font.setStyleHint(QFont.Monospace)
        font.setFixedPitch(True)
        self.setFont(font)
        self.setTabStopDistance(4 * self.fontMetrics().horizontalAdvance(" "))

        self._highlighter = PythonHighlighter(self.document())

        self.blockCountChanged.connect(self._update_line_area_width)
        self.updateRequest.connect(self._update_line_area)
        self.cursorPositionChanged.connect(self._highlight_current_line)

        self._update_line_area_width(0)
        self._highlight_current_line()

        # Editor surface tweaks
        pal = self.palette()
        pal.setColor(QPalette.Base, QColor(theme.BG_ELEVATED))
        pal.setColor(QPalette.Text, QColor(theme.TEXT_PRIMARY))
        self.setPalette(pal)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

    # ---- line number area sizing & painting
    def line_number_area_width(self) -> int:
        digits = max(2, len(str(max(1, self.blockCount()))))
        return 12 + self.fontMetrics().horizontalAdvance("9") * digits

    def _update_line_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def _update_line_area(self, rect: QRect, dy: int):
        if dy:
            self._line_area.scroll(0, dy)
        else:
            self._line_area.update(0, rect.y(), self._line_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self._update_line_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self._line_area.setGeometry(QRect(cr.left(), cr.top(),
                                          self.line_number_area_width(),
                                          cr.height()))

    def line_number_area_paint(self, event):
        painter = QPainter(self._line_area)
        painter.fillRect(event.rect(), QColor(theme.BG_PANEL))

        block = self.firstVisibleBlock()
        block_num = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        cur_line = self.textCursor().blockNumber()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                num = str(block_num + 1)
                color = theme.ACCENT if block_num == cur_line else theme.TEXT_DIM
                painter.setPen(QColor(color))
                painter.drawText(0, top,
                                 self._line_area.width() - 6,
                                 self.fontMetrics().height(),
                                 Qt.AlignRight, num)
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_num += 1

    # ---- current line
    def _highlight_current_line(self):
        extra: list[QTextEdit.ExtraSelection] = []
        if not self.isReadOnly():
            sel = QTextEdit.ExtraSelection()
            color = QColor(theme.BG_HOVER)
            sel.format.setBackground(color)
            sel.format.setProperty(QTextFormat.FullWidthSelection, True)
            sel.cursor = self.textCursor()
            sel.cursor.clearSelection()
            extra.append(sel)
        self.setExtraSelections(extra)

    # ---- key handling: smart indent / tab
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab and not event.modifiers():
            self.insertPlainText(self.INDENT)
            return

        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            cursor = self.textCursor()
            block = cursor.block().text()
            indent = re.match(r"\s*", block).group(0)
            extra = self.INDENT if block.rstrip().endswith(":") else ""
            super().keyPressEvent(event)
            self.insertPlainText(indent + extra)
            return

        super().keyPressEvent(event)
