# PyForge Academy

> An interactive desktop IDE that teaches Python from first variables to
> production-grade async APIs and local LLM pipelines — with a built-in
> AI tutor running fully offline via Ollama.

PyForge is a single-application learning platform: curated curriculum,
syntax-highlighted editor, sandboxed runner, animated visualizer, and a
streaming Mistral chat tutor — all in one PySide6 window.

---

## Quick start

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/PyForge-Academy.git
cd PyForge-Academy

# 2. Create and activate a virtual environment
# Windows:
python -m venv venv
.\venv\Scripts\activate
# macOS/Linux:
# python3 -m venv venv
# source venv/bin/activate

# 3. Install Python deps
pip install -r requirements.txt

# 4. Install Ollama and pull the tutor model
#    (https://ollama.com/download)
ollama pull mistral
ollama serve     # in a separate shell, if not auto-started

# 5. Run the app
python main.py
```

The app will create `~/.pyforge/progress.db` on first launch to track
completed lessons. Delete that file to fully reset progress.

---

## Architecture

```
┌─────────────── PySide6 Main Window ─────────────────────────────┐
│                                                                 │
│  Curriculum Tree    Lesson View                  AI Tutor       │
│  ─────────────      ─────────────                ────────       │
│   • Foundations      ┌──────────────────┐        ┌───────────┐  │
│   • Core             │  Theory (md)     │        │ stream    │  │
│   • Data Struct.     ├──────────────────┤        │  chunks   │  │
│   • OOP              │  Code editor     │◀──────▶│  via      │  │
│   • Async            │  (highlighter)   │        │  Ollama   │  │
│   • AI & LLMs        ├──────────────────┤        │  /api/    │  │
│   • …                │  Output │ Viz │  │        │  generate │  │
│                      └──────────────────┘        └───────────┘  │
│                                                                 │
└──────┬──────────────────────────┬──────────────────────────┬────┘
       │                          │                          │
   curriculum.py             code_runner.py              ai_tutor.py
   (lesson DB)               (exec sandbox)              (QThread → REST)
                                  │
                            visualizer.py
                            (QGraphicsScene
                             memory diagrams)
                                  │
                            progress_db.py
                            (SQLite, ~/.pyforge)
```

### Module map

| Module | Responsibility |
|---|---|
| `main.py` | Boots the `QApplication`, applies theme, opens the main window. |
| `pyforge/theme.py` | Color tokens + global QSS stylesheet. |
| `pyforge/curriculum.py` | All lesson content (theory, examples, exercises, auto-checks). |
| `pyforge/main_window.py` | Layout & orchestration (sidebar / center / right panel). |
| `pyforge/code_editor.py` | Custom `QPlainTextEdit` with syntax highlighter, line numbers, smart indent. |
| `pyforge/code_runner.py` | Timed `exec()` sandbox + exercise checker. |
| `pyforge/visualizer.py` | `QGraphicsScene` renderer for memory / list / dict / loop / generator views. |
| `pyforge/ai_tutor.py` | Ollama `/api/generate` streaming client on a `QThread` + chat UI. |
| `pyforge/progress_db.py` | SQLite-backed lesson + run history store. |
| `pyforge/assets/` | Static assets like the app logo. |

### Data flow on a typical lesson interaction

1. User clicks a lesson in the tree → `MainWindow._open_lesson(id)` loads
   theory, example, exercise, and pushes the lesson context into the AI
   panel.
2. User edits code, clicks ▶ Run → `CodeRunner.run(source)` execs in a
   dict scope with stdout captured and a watchdog timer.
3. Output panel updates; the result's `scope` dict is stashed for
   visualization.
4. User clicks 🧠 Visualize → `VisualizerView.visualize(scope, hint)`
   renders a `QGraphicsScene` view appropriate to the data shape.
5. User asks a question in the AI panel → an `_OllamaWorker` runs on a
   `QThread`, streams response chunks back via Qt signals; UI re-renders
   the latest assistant turn each tick.
6. User clicks ✓ Check exercise → `CodeRunner.check_exercise()` re-runs
   the source then evaluates the lesson's `assert_code` against the
   resulting scope; pass/fail flows into `ProgressStore`.

---

## Curriculum coverage

- **Foundations** — variables, types, strings, numbers, control flow, loops
- **Core** — functions, lambdas, comprehensions
- **Data Structures** — lists, dicts, tuples, sets
- **OOP** — classes, inheritance, dunder methods, dataclasses
- **Functional & Iterators** — generators, itertools, decorators
- **Async & Concurrency** — threads, processes, GIL, asyncio
- **Stdlib Power Tools** — pathlib, json/csv/sqlite3, regex
- **Errors & Logging** — exceptions, logging
- **Data Science** — NumPy, pandas, matplotlib
- **Web & APIs** — httpx, FastAPI
- **Testing & Tooling** — pytest essentials
- **Performance** — profiling, caching
- **AI & LLMs** — calling Ollama, mini RAG concepts

Lessons live in `app/curriculum.py` as a Python list of dicts; this is
intentionally easy to extend or migrate to a CMS later.

---

## Customization

- **Switch models**: edit `DEFAULT_MODEL` in `pyforge/ai_tutor.py`. Any model
  you've pulled with `ollama pull <name>` works.
- **Add a lesson**: append a dict to `CURRICULUM` in `pyforge/curriculum.py`. The
  sidebar groups by `level` automatically.
- **Theme**: tweak tokens in `pyforge/theme.py`. The QSS in
  `global_stylesheet()` rebuilds from those tokens.
- **Sandbox**: `pyforge/code_runner.py` runs user code in-process. For a
  multi-tenant or paid version, swap `exec()` for a subprocess + seccomp
  / nsjail / a WASM runtime (Pyodide).

---

## What this is *not* (yet)

- Not a competitive programming judge — no hidden test cases or scoring.
- Not multi-user / cloud-synced — progress is local SQLite.
- Not internet-sandbox safe — `exec()` runs in the same process.
- Not a video course — text + interactive code instead.

These are addressable in v1 without redesigning anything; see the roadmap
in the project notes.
