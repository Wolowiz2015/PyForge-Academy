"""
Interactive visualizer for PyForge Academy.

Renders abstract Python state into geometry on a QGraphicsScene so learners
can *see* what a list, dict, or call frame looks like.

Modes:
  - "memory"     : key/value cards for top-level variables
  - "list"       : indexed slots laid out horizontally
  - "dict"       : key boxes connected to value boxes
  - "object"     : class instance with attribute table
  - "call-stack" : labeled frames stacked vertically
  - "generator"  : token stream emerging from a function box (animated)
  - "loop"       : iterator with a moving highlight cursor (animated)

The visualizer is fed by `CodeRunner.run(...).scope` plus the lesson's `viz`
hint. It chooses what to draw heuristically when the hint is general
("memory" / "object" / "list" / "dict"), or uses the explicit hint to drive
the animated modes.

Animation is done with QTimer ticks updating a small state struct rather
than QPropertyAnimation per item — simpler and fits our discrete steps.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from PySide6.QtCore import Qt, QRectF, QTimer, QPointF
from PySide6.QtGui import QBrush, QColor, QFont, QPen, QPainter
from PySide6.QtWidgets import (
    QGraphicsScene, QGraphicsView, QGraphicsRectItem,
    QGraphicsSimpleTextItem, QGraphicsLineItem, QGraphicsItemGroup,
)

from pyforge import theme


def _box(scene: QGraphicsScene, x, y, w, h, color=theme.BG_PANEL,
         border=theme.BORDER_BRIGHT, radius=6) -> QGraphicsRectItem:
    rect = scene.addRect(QRectF(x, y, w, h),
                         QPen(QColor(border), 1.2),
                         QBrush(QColor(color)))
    return rect


def _text(scene: QGraphicsScene, x, y, s, color=theme.TEXT_PRIMARY,
          size=11, bold=False) -> QGraphicsSimpleTextItem:
    item = scene.addSimpleText(str(s))
    f = QFont("JetBrains Mono", size)
    if bold:
        f.setBold(True)
    item.setFont(f)
    item.setBrush(QBrush(QColor(color)))
    item.setPos(x, y)
    return item


def _truncate(value: Any, n: int = 28) -> str:
    s = repr(value)
    return s if len(s) <= n else s[: n - 1] + "…"


class VisualizerView(QGraphicsView):
    """Interactive canvas. Public entry point: `visualize(scope, hint)`."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform)
        self.setBackgroundBrush(QBrush(QColor(theme.BG_DEEP)))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._anim_state: Dict[str, Any] = {}

    # ------------------------------------------------------------------ public
    def clear(self):
        self._timer.stop()
        self._scene.clear()
        self._anim_state.clear()

    def visualize(self, scope: Dict[str, Any], hint: Optional[str] = None):
        """Render the appropriate diagram for the scope."""
        self.clear()

        if not scope and not hint:
            self._render_empty()
            return

        # Pick a default if no hint
        chosen = hint or self._infer_hint(scope)

        try:
            if chosen == "list":
                self._render_lists(scope)
            elif chosen == "dict":
                self._render_dicts(scope)
            elif chosen == "object":
                self._render_objects(scope)
            elif chosen == "call-stack":
                self._render_call_stack(scope)
            elif chosen == "loop":
                self._render_loop(scope)
            elif chosen == "generator":
                self._render_generator(scope)
            else:
                self._render_memory(scope)
        except Exception as e:  # never let visualization break the lesson
            self.clear()
            _text(self._scene, 20, 20, f"Visualization error: {e}",
                  color=theme.WARNING)

        self.setSceneRect(self._scene.itemsBoundingRect().adjusted(-20, -20, 20, 20))

    # ------------------------------------------------------------------ helpers
    def _infer_hint(self, scope: Dict[str, Any]) -> str:
        # Pick the most "interesting" structure present
        for v in scope.values():
            if isinstance(v, list) and v:
                return "list"
        for v in scope.values():
            if isinstance(v, dict) and v:
                return "dict"
        for v in scope.values():
            if hasattr(v, "__dict__") and not callable(v):
                return "object"
        return "memory"

    def _render_empty(self):
        _text(self._scene, 20, 20,
              "Run code to populate variables, then click Visualize.",
              color=theme.TEXT_MUTED, size=12)

    # ------------------------------------------------------------------ memory
    def _render_memory(self, scope: Dict[str, Any]):
        """Cards: name -> repr(value) with type tag."""
        _text(self._scene, 20, 14, "Memory frame", color=theme.TEXT_MUTED,
              size=11, bold=True)

        x0, y0 = 20, 40
        card_w, card_h, gap = 240, 64, 14

        for i, (name, value) in enumerate(scope.items()):
            row, col = divmod(i, 3)
            x = x0 + col * (card_w + gap)
            y = y0 + row * (card_h + gap)
            _box(self._scene, x, y, card_w, card_h, color=theme.BG_PANEL)
            _text(self._scene, x + 12, y + 8, name, color=theme.ACCENT_HOVER,
                  bold=True, size=12)
            _text(self._scene, x + 12, y + 28, _truncate(value),
                  color=theme.TEXT_PRIMARY)
            _text(self._scene, x + 12, y + 46,
                  f"{type(value).__name__}", color=theme.TEXT_MUTED, size=9)

    # ------------------------------------------------------------------ list
    def _render_lists(self, scope: Dict[str, Any]):
        y = 20
        for name, value in scope.items():
            if not isinstance(value, list):
                continue
            _text(self._scene, 20, y, f"{name}  list[{len(value)}]",
                  color=theme.ACCENT_HOVER, bold=True, size=12)
            y += 26
            cell_w, cell_h = 70, 50
            for i, item in enumerate(value[:20]):
                x = 20 + i * (cell_w + 4)
                _box(self._scene, x, y, cell_w, cell_h)
                _text(self._scene, x + 8, y + 10, _truncate(item, 8),
                      color=theme.TEXT_PRIMARY)
                _text(self._scene, x + 8, y + 32, f"[{i}]",
                      color=theme.TEXT_DIM, size=9)
            if len(value) > 20:
                _text(self._scene, 20 + 20 * (cell_w + 4), y + 18,
                      f"+{len(value)-20} more", color=theme.TEXT_MUTED)
            y += cell_h + 30

        if y == 20:
            _text(self._scene, 20, 20, "No lists in scope yet.",
                  color=theme.TEXT_MUTED)

    # ------------------------------------------------------------------ dict
    def _render_dicts(self, scope: Dict[str, Any]):
        y = 20
        for name, value in scope.items():
            if not isinstance(value, dict):
                continue
            _text(self._scene, 20, y, f"{name}  dict[{len(value)}]",
                  color=theme.ACCENT_HOVER, bold=True, size=12)
            y += 24

            row_h = 32
            kw, vw, gap = 140, 200, 10
            for i, (k, v) in enumerate(list(value.items())[:25]):
                yy = y + i * (row_h + 4)
                _box(self._scene, 20, yy, kw, row_h)
                _text(self._scene, 28, yy + 8, _truncate(k, 16),
                      color=theme.SYN_STRING)
                # arrow
                self._scene.addLine(20 + kw, yy + row_h/2, 20 + kw + gap, yy + row_h/2,
                                    QPen(QColor(theme.BORDER_BRIGHT), 1.2))
                _box(self._scene, 20 + kw + gap, yy, vw, row_h, color=theme.BG_ELEVATED)
                _text(self._scene, 28 + kw + gap, yy + 8, _truncate(v, 28),
                      color=theme.TEXT_PRIMARY)
            y += min(len(value), 25) * (row_h + 4) + 30

        if y == 20:
            _text(self._scene, 20, 20, "No dicts in scope yet.",
                  color=theme.TEXT_MUTED)

    # ------------------------------------------------------------------ object
    def _render_objects(self, scope: Dict[str, Any]):
        y = 20
        for name, value in scope.items():
            if callable(value) or not hasattr(value, "__dict__"):
                continue
            attrs = value.__dict__
            if not attrs:
                continue

            # Header
            _box(self._scene, 20, y, 360, 36, color=theme.ACCENT_SOFT,
                 border=theme.ACCENT)
            _text(self._scene, 32, y + 9,
                  f"{name} : {type(value).__name__}",
                  color=theme.TEXT_PRIMARY, bold=True, size=12)
            y += 42

            # Attribute rows
            for k, v in attrs.items():
                _box(self._scene, 20, y, 130, 28)
                _text(self._scene, 28, y + 7, k, color=theme.SYN_FUNCTION)
                _box(self._scene, 154, y, 226, 28, color=theme.BG_ELEVATED)
                _text(self._scene, 162, y + 7, _truncate(v, 30),
                      color=theme.TEXT_PRIMARY)
                y += 32
            y += 18

        if y == 20:
            _text(self._scene, 20, 20, "No objects with attributes yet.",
                  color=theme.TEXT_MUTED)

    # ------------------------------------------------------------------ call-stack
    def _render_call_stack(self, scope: Dict[str, Any]):
        # We can't introspect a finished call stack, so we synthesize a
        # didactic view: each top-level callable becomes a "frame".
        _text(self._scene, 20, 14, "Call stack (top is most recent)",
              color=theme.TEXT_MUTED, size=11, bold=True)

        callables = [(k, v) for k, v in scope.items() if callable(v)]
        if not callables:
            self._render_memory(scope)
            return

        y = 50
        for i, (name, fn) in enumerate(reversed(callables)):
            color = theme.ACCENT_SOFT if i == 0 else theme.BG_PANEL
            _box(self._scene, 20, y, 380, 50, color=color)
            _text(self._scene, 32, y + 8, f"frame: {name}",
                  color=theme.TEXT_PRIMARY, bold=True)
            try:
                argcount = fn.__code__.co_argcount
                args = fn.__code__.co_varnames[:argcount]
                _text(self._scene, 32, y + 28,
                      f"args: ({', '.join(args)})",
                      color=theme.TEXT_MUTED, size=10)
            except Exception:
                pass
            y += 60

    # ------------------------------------------------------------------ loop (animated)
    def _render_loop(self, scope: Dict[str, Any]):
        # Pick the longest sequence-like value as the iterable to walk.
        seq = None
        seq_name = None
        for k, v in scope.items():
            if isinstance(v, (list, tuple)) and v:
                if seq is None or len(v) > len(seq):
                    seq, seq_name = list(v), k
        if seq is None:
            seq = list(range(1, 9))
            seq_name = "range(1, 9)"

        _text(self._scene, 20, 14, f"Iterating over {seq_name}",
              color=theme.TEXT_MUTED, bold=True)

        cell_w, cell_h = 60, 50
        cells = []
        for i, item in enumerate(seq[:18]):
            x = 20 + i * (cell_w + 4)
            r = _box(self._scene, x, 50, cell_w, cell_h)
            _text(self._scene, x + 8, 60, _truncate(item, 6))
            cells.append(r)

        cursor = _box(self._scene, 20, 110, cell_w, 6,
                      color=theme.ACCENT, border=theme.ACCENT)

        # Animate cursor sliding through cells
        self._anim_state = {"mode": "loop", "i": 0, "cells": cells,
                            "cursor": cursor, "cell_w": cell_w}
        self._timer.start(420)

    # ------------------------------------------------------------------ generator (animated)
    def _render_generator(self, scope: Dict[str, Any]):
        _text(self._scene, 20, 14, "Generator: lazy values yield over time",
              color=theme.TEXT_MUTED, bold=True)

        # Source box on left
        _box(self._scene, 20, 60, 160, 60, color=theme.ACCENT_SOFT, border=theme.ACCENT)
        _text(self._scene, 36, 80, "yield ...", color=theme.TEXT_PRIMARY, bold=True)

        # Track for emitted values
        for x in range(200, 700, 80):
            self._scene.addLine(x, 90, x + 60, 90,
                                QPen(QColor(theme.BORDER), 1, Qt.DashLine))

        # Animated tokens
        tokens = []
        self._anim_state = {"mode": "gen", "i": 0, "tokens": tokens, "next_value": 0}
        self._timer.start(600)

    # ------------------------------------------------------------------ tick
    def _tick(self):
        st = self._anim_state
        if st.get("mode") == "loop":
            i = st["i"]
            cells = st["cells"]
            if i >= len(cells):
                st["i"] = 0
                i = 0
            cursor = st["cursor"]
            target_x = 20 + i * (st["cell_w"] + 4)
            cursor.setRect(QRectF(target_x, 110, st["cell_w"], 6))
            # subtle highlight on the active cell
            for j, cell in enumerate(cells):
                cell.setBrush(QBrush(QColor(theme.ACCENT_SOFT if j == i
                                            else theme.BG_PANEL)))
            st["i"] = i + 1

        elif st.get("mode") == "gen":
            i = st["i"]
            x = 200 + (i % 6) * 80
            tok = _box(self._scene, x, 70, 60, 40, color=theme.BG_ELEVATED,
                       border=theme.SUCCESS)
            _text(self._scene, x + 14, 78, str(st["next_value"]),
                  color=theme.SUCCESS, bold=True)
            st["tokens"].append(tok)
            st["next_value"] += 1
            st["i"] = i + 1
            # Trim oldest tokens if too many
            if len(st["tokens"]) > 14:
                old = st["tokens"].pop(0)
                self._scene.removeItem(old)
