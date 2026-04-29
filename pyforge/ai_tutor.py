"""
AI Tutor — Ollama (Mistral by default) chat panel.

Talks to a local Ollama instance over its REST API at http://localhost:11434.
The streaming endpoint returns one JSON object per line, each with a
`response` chunk; we emit those chunks into the UI as they arrive so the
chat feels responsive.

Design choices:
  - Networking happens on a worker QThread, never on the GUI thread.
  - Chat history is sent every turn (Ollama is stateless on /api/generate).
  - System prompt frames Mistral as a Python tutor and constrains scope.
  - Lesson-aware: when the user is on a lesson, we inject the lesson's
    title + theory as context so answers stay relevant.
  - Resilient: connection errors surface a friendly message with the exact
    command to run (`ollama pull mistral`) instead of a stack trace.

If you swap Mistral for another model, just change DEFAULT_MODEL.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import List, Optional

from PySide6.QtCore import QObject, QThread, Signal, Qt
from PySide6.QtGui import QFont, QTextCursor
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTextEdit, QVBoxLayout, QWidget,
)

# Use stdlib HTTP so we don't force `requests`/`httpx` on the user.
import urllib.request
import urllib.error

from pyforge import theme


OLLAMA_URL    = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "mistral"

SYSTEM_PROMPT = (
    "You are PyForge Tutor, a senior Python engineer and patient teacher. "
    "Answer ONLY questions related to learning Python, computer science "
    "fundamentals, debugging the user's code, or the lesson they are on. "
    "Be concise. When useful, give short runnable examples in fenced code "
    "blocks. If asked something off-topic, gently steer back to Python."
)


@dataclass
class ChatTurn:
    role: str            # "user" | "assistant"
    content: str = ""


# ---------------------------------------------------------------- worker
class _OllamaWorker(QObject):
    chunk    = Signal(str)
    finished = Signal()
    failed   = Signal(str)

    def __init__(self, model: str, prompt: str):
        super().__init__()
        self.model = model
        self.prompt = prompt
        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        body = json.dumps({
            "model":  self.model,
            "prompt": self.prompt,
            "stream": True,
            "options": {"temperature": 0.4, "num_ctx": 4096},
        }).encode("utf-8")

        req = urllib.request.Request(
            OLLAMA_URL,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                for raw in resp:
                    if self._stop:
                        break
                    line = raw.decode("utf-8", errors="ignore").strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    chunk = obj.get("response", "")
                    if chunk:
                        self.chunk.emit(chunk)
                    if obj.get("done"):
                        break
        except urllib.error.URLError as e:
            self.failed.emit(
                f"Could not reach Ollama at {OLLAMA_URL}.\n"
                f"Reason: {e.reason}\n\n"
                f"Make sure Ollama is running and you've pulled the model:\n"
                f"  ollama pull {self.model}\n"
                f"  ollama serve"
            )
            return
        except Exception as e:
            self.failed.emit(f"Unexpected error talking to Ollama: {e}")
            return
        finally:
            self.finished.emit()


# ---------------------------------------------------------------- chat panel
class AITutorPanel(QFrame):
    """Right-hand chat panel with streaming Mistral responses."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self._history: List[ChatTurn] = []
        self._worker: Optional[_OllamaWorker] = None
        self._thread: Optional[QThread] = None
        self._lesson_context = ""
        self._streaming = False
        self._current_assistant_turn: Optional[ChatTurn] = None

        self._build_ui()
        self._render_intro()

    # --------------------------------------------------------------- public api
    def set_lesson_context(self, title: str, theory: str):
        self._lesson_context = (
            f"Current lesson: {title}\n"
            f"Lesson notes:\n{theory}\n"
        )
        self._render_lesson_chip(title)

    def append_user_question(self, text: str):
        """External entry point — used when the editor 'Ask Tutor' button fires."""
        self.input.setText(text)
        self._send()

    # --------------------------------------------------------------- ui scaffold
    def _build_ui(self):
        v = QVBoxLayout(self)
        v.setContentsMargins(14, 14, 14, 14)
        v.setSpacing(10)

        # Header
        hdr = QHBoxLayout()
        title = QLabel("AI TUTOR")
        title.setObjectName("H3")
        hdr.addWidget(title)
        hdr.addStretch(1)
        self.lesson_chip = QLabel("")
        self.lesson_chip.setObjectName("Tag")
        self.lesson_chip.setVisible(False)
        hdr.addWidget(self.lesson_chip)
        v.addLayout(hdr)

        # Transcript
        self.transcript = QTextEdit()
        self.transcript.setReadOnly(True)
        self.transcript.setFont(QFont("Inter", 11))
        v.addWidget(self.transcript, 1)

        # Quick prompts
        quick = QHBoxLayout()
        quick.setSpacing(6)
        for label, text in [
            ("Explain this lesson", "Explain the current lesson in your own words."),
            ("Debug my code",        "Look at my latest code in the editor and explain what's wrong."),
            ("Give me a harder challenge", "Give me a harder version of the current exercise."),
        ]:
            b = QPushButton(label)
            b.setObjectName("GhostButton")
            b.clicked.connect(lambda _, t=text: self._set_input(t))
            quick.addWidget(b)
        quick.addStretch(1)
        v.addLayout(quick)

        # Input row
        row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask anything Python — e.g. 'why does my list mutate?'")
        self.input.returnPressed.connect(self._send)
        row.addWidget(self.input, 1)
        self.send_btn = QPushButton("Send")
        self.send_btn.setObjectName("PrimaryButton")
        self.send_btn.clicked.connect(self._send)
        row.addWidget(self.send_btn)
        v.addLayout(row)

    def _render_intro(self):
        self._append_html(
            f"<div style='color:{theme.TEXT_MUTED}; padding:6px 0;'>"
            f"<b style='color:{theme.ACCENT_HOVER}'>PyForge Tutor</b> is connected via "
            f"local Ollama. Default model: <code>{DEFAULT_MODEL}</code>. "
            f"Ask about syntax, errors, design patterns, or the current lesson."
            f"</div>"
        )

    def _render_lesson_chip(self, title: str):
        self.lesson_chip.setText(title[:40])
        self.lesson_chip.setVisible(True)

    def _set_input(self, text: str):
        self.input.setText(text)
        self.input.setFocus()

    # --------------------------------------------------------------- send / stream
    def _send(self):
        if self._streaming:
            return
        question = self.input.text().strip()
        if not question:
            return

        self.input.clear()
        self._history.append(ChatTurn(role="user", content=question))
        self._append_html(self._format_turn("user", question))

        # Start a fresh assistant turn that we'll mutate as chunks arrive
        self._current_assistant_turn = ChatTurn(role="assistant", content="")
        self._history.append(self._current_assistant_turn)
        self._append_html(self._format_turn("assistant", "▌"))  # caret-y placeholder

        prompt = self._build_prompt()

        self._thread = QThread(self)
        self._worker = _OllamaWorker(DEFAULT_MODEL, prompt)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.chunk.connect(self._on_chunk)
        self._worker.finished.connect(self._on_finished)
        self._worker.failed.connect(self._on_failed)

        self._streaming = True
        self.send_btn.setEnabled(False)
        self.send_btn.setText("…")
        self._thread.start()

    def _build_prompt(self) -> str:
        # Stitch together: system + lesson context + recent history
        parts = [SYSTEM_PROMPT]
        if self._lesson_context:
            parts.append(self._lesson_context)
        for turn in self._history[-12:]:  # cap context
            tag = "User" if turn.role == "user" else "Tutor"
            parts.append(f"{tag}: {turn.content}")
        parts.append("Tutor:")
        return "\n\n".join(parts)

    # --------------------------------------------------------------- slots
    def _on_chunk(self, chunk: str):
        if self._current_assistant_turn is None:
            return
        self._current_assistant_turn.content += chunk
        self._rerender_last_turn()

    def _on_finished(self):
        self._streaming = False
        self.send_btn.setEnabled(True)
        self.send_btn.setText("Send")
        if self._thread:
            self._thread.quit()
            self._thread.wait(500)

    def _on_failed(self, message: str):
        self._streaming = False
        self.send_btn.setEnabled(True)
        self.send_btn.setText("Send")
        if self._current_assistant_turn is not None:
            self._current_assistant_turn.content = message
            self._rerender_last_turn(error=True)
        if self._thread:
            self._thread.quit()
            self._thread.wait(500)

    # --------------------------------------------------------------- rendering
    def _rerender_last_turn(self, error: bool = False):
        # Rewrite the entire transcript — simple, always correct, fast enough
        self.transcript.clear()
        self._render_intro()
        if self._lesson_context:
            self.transcript.append("")
        for turn in self._history:
            self._append_html(self._format_turn(turn.role, turn.content,
                                                error=error and turn is self._current_assistant_turn))
        self._scroll_to_bottom()

    def _format_turn(self, role: str, content: str, error: bool = False) -> str:
        if role == "user":
            return (
                f"<div style='margin: 16px 0;'>"
                f"<div style='background:{theme.BG_ELEVATED}; padding:12px 16px; "
                f"border-radius: 12px 12px 0 12px; margin-left: 20%;'>"
                f"<b style='color:{theme.ACCENT_HOVER}; font-size:11px; text-transform:uppercase;'>You</b><br>"
                f"<div style='color:{theme.TEXT_PRIMARY}; margin-top:4px;'>{self._html_escape(content)}</div>"
                f"</div>"
                f"</div>"
            )
        color = theme.DANGER if error else theme.ACCENT
        body = self._format_assistant_body(content)
        return (
            f"<div style='margin: 16px 0;'>"
            f"<div style='background:{theme.BG_PANEL}; padding:12px 16px; "
            f"border: 1px solid {theme.BORDER}; border-radius: 12px 12px 12px 0; margin-right: 10%;'>"
            f"<b style='color:{color}; font-size:11px; text-transform:uppercase;'>PyForge Tutor</b><br>"
            f"<div style='color:{theme.TEXT_PRIMARY}; margin-top:4px; line-height:1.6;'>{body}</div>"
            f"</div>"
            f"</div>"
        )

    def _format_assistant_body(self, text: str) -> str:
        # Very lightweight Markdown-ish: code fences + inline backticks
        out = []
        in_code = False
        for line in text.splitlines():
            if line.strip().startswith("```"):
                if in_code:
                    out.append("</code></pre>")
                    in_code = False
                else:
                    out.append(
                        f"<pre style='background:{theme.BG_DEEP}; padding:12px; "
                        f"border-radius:8px; border: 1px solid {theme.BORDER}; "
                        f"margin: 8px 0;'>"
                        f"<code style='color:{theme.SYN_STRING}; font-family: JetBrains Mono, monospace; font-size: 12px;'>"
                    )
                    in_code = True
                continue
            if in_code:
                out.append(self._html_escape(line))
            else:
                # inline `code`
                escaped = self._html_escape(line)
                escaped = escaped.replace(
                    "`", f"<span style='color:{theme.SYN_FUNCTION}; font-family:monospace;'>")
                # Close the span (naive)
                if "<span" in escaped:
                    escaped = escaped.replace(" ", "</span> ", 1) # simple hack for one word
                out.append(escaped)
        if in_code:
            out.append("</code></pre>")
        return "<br>".join(out) or "<i>(no response)</i>"

    @staticmethod
    def _html_escape(s: str) -> str:
        return (s.replace("&", "&amp;")
                 .replace("<", "&lt;")
                 .replace(">", "&gt;"))

    def _append_html(self, html: str):
        self.transcript.moveCursor(QTextCursor.End)
        self.transcript.insertHtml(html)
        self._scroll_to_bottom()

    def _scroll_to_bottom(self):
        sb = self.transcript.verticalScrollBar()
        sb.setValue(sb.maximum())
