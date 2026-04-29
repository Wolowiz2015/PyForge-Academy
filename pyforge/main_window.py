"""
Main window for PyForge Academy.

Layout (left → right):
   ┌────────────┬───────────────────────────────────┬──────────────┐
   │  Sidebar   │  Lesson view (theory / editor /   │   AI Tutor   │
   │ Curriculum │  output / visualizer tabs)        │   (Mistral)  │
   │   tree     │                                   │              │
   └────────────┴───────────────────────────────────┴──────────────┘

The sidebar is a QTreeWidget grouping lessons by level. Selecting a lesson
loads:
  - theory text into the markdown-flavored top pane
  - example code into the editor
  - exercise prompt + check button below
"""

from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont, QKeySequence, QPixmap, QColor
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QMainWindow, QPlainTextEdit,
    QProgressBar, QPushButton, QSplitter, QStatusBar, QTabWidget,
    QTextBrowser, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget,
    QMessageBox, QGraphicsDropShadowEffect, QSizePolicy
)
import datetime as dt

from pyforge import theme
from pyforge.ai_tutor import AITutorPanel, DEFAULT_MODEL
from pyforge.code_runner import CodeRunner
from pyforge.curriculum import CURRICULUM, all_levels, by_level, find_lesson
from pyforge.progress_db import LessonProgress, ProgressStore
from pyforge.visualizer import VisualizerView
from pyforge.code_editor import CodeEditor

ASSETS_DIR = Path(__file__).parent / "assets"
LOGO_PATH = str(ASSETS_DIR / "logo.png")

def add_shadow(widget: QWidget, blur=24, alpha=40, color=None):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    c = QColor(color) if color else QColor(0, 0, 0)
    c.setAlpha(alpha)
    shadow.setColor(c)
    shadow.setOffset(0, 4)
    widget.setGraphicsEffect(shadow)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyForge Academy")
        self.resize(1360, 850)
        self.setMinimumSize(1000, 700)

        self._runner   = CodeRunner(timeout_seconds=8.0)
        self._progress = ProgressStore()
        self._current_lesson_id: str | None = None

        self._build_ui()
        self._wire_shortcuts()

        # Open the first lesson on launch
        last = self._progress.get_meta("last_lesson_id")
        try:
            self._open_lesson(last) if last else self._open_lesson(CURRICULUM[0]["id"])
        except (KeyError, IndexError):
            if CURRICULUM:
                self._open_lesson(CURRICULUM[0]["id"])

        self._refresh_progress_bar()

    # ------------------------------------------------------------------ ui
    def _build_ui(self):
        # ---------- Left: Sidebar
        left = QFrame()
        left.setObjectName("SidebarCard")
        left_v = QVBoxLayout(left)
        left_v.setContentsMargins(12, 20, 12, 20)
        left_v.setSpacing(20)

        # Logo & Brand
        brand_container = QWidget()
        brand_h = QHBoxLayout(brand_container)
        brand_h.setContentsMargins(12, 0, 12, 0)
        brand_h.setSpacing(12)
        
        logo_lbl = QLabel()
        pix = QPixmap(LOGO_PATH)
        if not pix.isNull():
            logo_lbl.setPixmap(pix.scaled(42, 42, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        brand_h.addWidget(logo_lbl)
        
        brand_text = QLabel("PYFORGE")
        brand_text.setObjectName("Brand")
        brand_text.setContentsMargins(0, 0, 0, 0)
        brand_h.addWidget(brand_text)
        brand_h.addStretch()
        left_v.addWidget(brand_container)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(20)
        self.tree.itemClicked.connect(self._on_tree_click)

        for level in all_levels():
            top = QTreeWidgetItem([level])
            top.setFont(0, QFont("Inter", 11, QFont.Bold))
            for lesson in by_level(level):
                child = QTreeWidgetItem([f"{lesson['title']}"])
                child.setData(0, Qt.UserRole, lesson["id"])
                top.addChild(child)
            top.setExpanded(level in ("Onboarding", "Foundations"))
            self.tree.addTopLevelItem(top)
        left_v.addWidget(self.tree, 1)

        # Sidebar Footer
        foot = QFrame()
        foot.setObjectName("Card")
        foot.setStyleSheet(f"background-color: {theme.BG_ELEVATED}; border: none;")
        foot_v = QVBoxLayout(foot)
        foot_v.setContentsMargins(16, 16, 16, 16)
        foot_v.setSpacing(8)
        l1 = QLabel("TUTOR ACTIVE")
        l1.setObjectName("H3")
        l1.setStyleSheet(f"color: {theme.SUCCESS}; font-size: 10px;")
        l2 = QLabel(f"{DEFAULT_MODEL} model")
        l2.setObjectName("Muted")
        foot_v.addWidget(l1)
        foot_v.addWidget(l2)
        left_v.addWidget(foot)

        # ---------- Center: Lesson Workspace
        center = QWidget()
        center_v = QVBoxLayout(center)
        center_v.setContentsMargins(40, 30, 40, 30)
        center_v.setSpacing(24)

        # Header
        hdr = QHBoxLayout()
        hdr.setSpacing(16)
        self.lesson_title = QLabel("…")
        self.lesson_title.setObjectName("H1")
        hdr.addWidget(self.lesson_title)
        self.level_chip = QLabel("")
        self.level_chip.setObjectName("Tag")
        hdr.addWidget(self.level_chip)
        hdr.addStretch(1)
        
        self.btn_check = QPushButton("Check Exercise")
        self.btn_check.setObjectName("PrimaryButton")
        self.btn_check.setCursor(Qt.PointingHandCursor)
        self.btn_check.clicked.connect(self._check_exercise)
        hdr.addWidget(self.btn_check)
        center_v.addLayout(hdr)

        # Content Splitter (Theory vs Editor/Output)
        main_split = QSplitter(Qt.Vertical)
        main_split.setHandleWidth(1)

        # Theory Area
        theory_container = QFrame()
        theory_container.setObjectName("Card")
        theory_v = QVBoxLayout(theory_container)
        theory_v.setContentsMargins(0, 0, 0, 0)
        
        self.theory = QTextBrowser()
        self.theory.setOpenExternalLinks(True)
        self.theory.setFrameShape(QFrame.NoFrame)
        self.theory.setStyleSheet(f"background-color: transparent; padding: 24px;")
        theory_v.addWidget(self.theory)
        main_split.addWidget(theory_container)

        # Editor + Tabs
        workspace_split = QSplitter(Qt.Horizontal)
        workspace_split.setHandleWidth(1)

        # Editor Pane
        ed_card = QFrame()
        ed_card.setObjectName("Card")
        ed_v = QVBoxLayout(ed_card)
        ed_v.setContentsMargins(0, 0, 0, 0)
        ed_v.setSpacing(0)

        ed_toolbar = QHBoxLayout()
        ed_toolbar.setContentsMargins(16, 12, 16, 12)
        ed_label = QLabel("EDITOR")
        ed_label.setObjectName("H3")
        ed_toolbar.addWidget(ed_label)
        ed_toolbar.addStretch(1)
        
        self.btn_run = QPushButton("Run")
        self.btn_run.setObjectName("PrimaryButton")
        self.btn_run.setCursor(Qt.PointingHandCursor)
        self.btn_run.clicked.connect(self._run_code)
        
        self.btn_viz = QPushButton("Visualize")
        self.btn_viz.setCursor(Qt.PointingHandCursor)
        self.btn_viz.clicked.connect(self._visualize)
        
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setObjectName("GhostButton")
        self.btn_reset.setCursor(Qt.PointingHandCursor)
        self.btn_reset.clicked.connect(self._reset_editor)
        
        for b in (self.btn_reset, self.btn_viz, self.btn_run):
            ed_toolbar.addWidget(b)
        ed_v.addLayout(ed_toolbar)

        self.editor = CodeEditor()
        self.editor.setFrameShape(QFrame.NoFrame)
        ed_v.addWidget(self.editor, 1)
        workspace_split.addWidget(ed_card)

        # Tabs Pane
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFrameShape(QFrame.NoFrame)
        self.output.setStyleSheet("background-color: transparent; padding: 12px;")
        self.tabs.addTab(self.output, "Output")

        self.viz = VisualizerView()
        self.tabs.addTab(self.viz, "Visualizer")

        self.exercise_view = QTextBrowser()
        self.exercise_view.setFrameShape(QFrame.NoFrame)
        self.exercise_view.setStyleSheet("background-color: transparent; padding: 24px;")
        self.tabs.addTab(self.exercise_view, "Exercise")

        workspace_split.addWidget(self.tabs)
        workspace_split.setSizes([600, 400])
        main_split.addWidget(workspace_split)
        
        main_split.setSizes([280, 500])
        center_v.addWidget(main_split, 1)

        # ---------- Right: AI Tutor
        self.ai_panel = AITutorPanel()
        self.ai_panel.setFixedWidth(340)

        # ---------- Master Layout
        master = QSplitter(Qt.Horizontal)
        master.addWidget(left)
        master.addWidget(center)
        master.addWidget(self.ai_panel)
        master.setStretchFactor(1, 1)
        master.setSizes([280, 800, 340])
        master.setHandleWidth(1)
        self.setCentralWidget(master)

        # ---------- Status Bar
        sb = QStatusBar()
        self.status_label = QLabel("Ready")
        sb.addWidget(self.status_label, 1)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        sb.addPermanentWidget(self.progress_bar)
        
        self.completion_label = QLabel("0 / 0")
        self.completion_label.setObjectName("Muted")
        self.completion_label.setContentsMargins(10, 0, 0, 0)
        sb.addPermanentWidget(self.completion_label)
        self.setStatusBar(sb)

    # ------------------------------------------------------------------ shortcuts
    def _wire_shortcuts(self):
        run_action = QAction("Run", self)
        run_action.setShortcut(QKeySequence("Ctrl+Return"))
        run_action.triggered.connect(self._run_code)
        self.addAction(run_action)

        check_action = QAction("Check", self)
        check_action.setShortcut(QKeySequence("Ctrl+Shift+Return"))
        check_action.triggered.connect(self._check_exercise)
        self.addAction(check_action)

        fullscreen_action = QAction("Toggle Fullscreen", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.triggered.connect(self._toggle_fullscreen)
        self.addAction(fullscreen_action)

    def _toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    # ------------------------------------------------------------------ tree
    def _on_tree_click(self, item: QTreeWidgetItem, _col: int):
        lesson_id = item.data(0, Qt.UserRole)
        if lesson_id:
            self._open_lesson(lesson_id)

    def _open_lesson(self, lesson_id: str):
        lesson = find_lesson(lesson_id)
        self._current_lesson_id = lesson_id

        self.lesson_title.setText(lesson["title"])
        self.level_chip.setText(lesson["level"].upper())
        self.theory.setMarkdown(lesson["theory"])
        self.editor.setPlainText(lesson["example"])
        self.output.setPlainText("")
        self.viz.clear()

        # Exercise tab
        ex_html = (
            f"<h2 style='color:{theme.TEXT_PRIMARY}; margin-bottom: 12px;'>Exercise Challenge</h2>"
            f"<div style='color:{theme.TEXT_MUTED}; font-size: 14px; line-height: 1.6;'>"
            f"{lesson['exercise'] or 'No exercise for this lesson.'}</div>"
            f"<div style='margin-top: 24px; padding: 12px; background:{theme.BG_ELEVATED}; border-radius: 8px; color:{theme.INFO};'>"
            f"<b>Tip:</b> Edit the code and click <b>Check Exercise</b> to verify."
            f"</div>"
        )
        self.exercise_view.setHtml(ex_html)

        # AI lesson context
        self.ai_panel.set_lesson_context(lesson["title"], lesson["theory"])

        # Persist progress
        existing = self._progress.get_lesson(lesson_id) or LessonProgress(lesson_id=lesson_id)
        if existing.status == "new":
            existing.status = "viewed"
        existing.last_seen_iso = dt.datetime.utcnow().isoformat()
        self._progress.upsert_lesson(existing)
        self._progress.set_meta("last_lesson_id", lesson_id)

        self.status_label.setText(f"Lesson {lesson_id} loaded")
        self._refresh_progress_bar()

    # ------------------------------------------------------------------ run
    def _run_code(self):
        source = self.editor.toPlainText()
        result = self._runner.run(source)

        text = []
        if result.stdout:
            text.append(result.stdout)
        if result.stderr:
            text.append(f"\n[STDERR]\n{result.stderr}")
        if result.error:
            text.append(f"\n[ERROR]\n{result.error}")
        if not text:
            text.append("(no output)")
        self.output.setPlainText("".join(text))

        self.tabs.setCurrentIndex(0)
        self.status_label.setText(
            f"{'✓' if result.ok else '✗'} Ran in {result.duration_ms:.1f}ms"
        )
        self._progress.log_run(self._current_lesson_id or "?", source,
                                result.duration_ms, result.ok,
                                dt.datetime.utcnow().isoformat())
        self._last_scope = result.scope

    def _visualize(self):
        scope = getattr(self, "_last_scope", None)
        if scope is None:
            self._run_code()
            scope = getattr(self, "_last_scope", {})
        lesson = find_lesson(self._current_lesson_id) if self._current_lesson_id else {}
        self.viz.visualize(scope, lesson.get("viz"))
        self.tabs.setCurrentIndex(1)

    def _reset_editor(self):
        if self._current_lesson_id is None:
            return
        lesson = find_lesson(self._current_lesson_id)
        self.editor.setPlainText(lesson["example"])
        self.output.clear()
        self.viz.clear()
        self.status_label.setText("Editor reset")

    # ------------------------------------------------------------------ check
    def _check_exercise(self):
        if self._current_lesson_id is None:
            return
        lesson = find_lesson(self._current_lesson_id)
        if not lesson["assert_code"]:
            QMessageBox.information(self, "No Exercise", "This lesson has no auto-checked exercise.")
            return
        source = self.editor.toPlainText()
        check = self._runner.check_exercise(source, lesson["assert_code"])

        prog = self._progress.get_lesson(self._current_lesson_id) or LessonProgress(
            lesson_id=self._current_lesson_id)
        prog.attempts += 1
        prog.last_seen_iso = dt.datetime.utcnow().isoformat()
        if check.passed:
            prog.exercise_passed = True
            prog.status = "completed"
        self._progress.upsert_lesson(prog)
        self._refresh_progress_bar()

        if check.passed:
            QMessageBox.information(self, "Success", "Correct! Exercise passed.")
            self.status_label.setText("✓ Exercise passed")
        else:
            QMessageBox.warning(self, "Try Again", check.detail)
            self.status_label.setText("✗ Exercise failed")

    # ------------------------------------------------------------------ progress
    def _refresh_progress_bar(self):
        summary = self._progress.completion_summary(len(CURRICULUM))
        self.progress_bar.setMaximum(summary["total"])
        self.progress_bar.setValue(summary["completed"])
        self.completion_label.setText(
            f'{summary["completed"]} / {summary["total"]} Completed'
        )
