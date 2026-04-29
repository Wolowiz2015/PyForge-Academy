"""
Code execution engine for PyForge Academy.

We run user code in an in-process exec sandbox with these guarantees:
  - stdout/stderr captured into a dict
  - a hard wall-clock timeout enforced by injecting a KeyboardInterrupt
    into the executing worker thread via PyThreadState_SetAsyncExc
  - locals/globals dict returned so the exercise checker can inspect them
  - results returned as a structured dict, not printed

This is *educational* sandboxing, not security sandboxing. For an
internet-facing version, swap exec() for a subprocess with seccomp / a
container / a WASM sandbox. See `notes/security.md`.

The exercise checker accepts an `assert_code` snippet authored alongside
each lesson; it executes against the merged scope from the user's run, so
the lesson author can write things like `assert square(3) == 9`.

About the timeout mechanism: a tight Python `while True: pass` will
*always* yield between bytecode dispatches (controlled by sys.setswitchinterval),
so an async exception injection from another thread reliably interrupts
it. Tight C loops that don't release the GIL (rare in user-level code)
are the one case this can't preempt — for those the duration_ms in the
result will exceed the configured timeout, and the worker thread is left
running but daemonized.
"""

from __future__ import annotations

import builtins
import ctypes
import io
import sys
import threading
import time
import traceback
import types
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass, field
from typing import Any, Dict

# Lessons sometimes use `@dataclass`, `pickle`, or other machinery that calls
# `sys.modules.get(cls.__module__)` to introspect the module a class was
# defined in. exec()'d code without a registered module fails that lookup.
# We pre-register a synthetic module under this name and run user code with
# `__name__` pointing at it.
_LESSON_MODULE_NAME = "__pyforge_lesson__"


@dataclass
class RunResult:
    ok: bool
    stdout: str = ""
    stderr: str = ""
    error: str = ""
    duration_ms: float = 0.0
    scope: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CheckResult:
    passed: bool
    detail: str = ""


def _async_raise(thread_ident: int, exctype: type) -> None:
    """Inject `exctype` into the thread identified by `thread_ident`."""
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_ulong(thread_ident),
        ctypes.py_object(exctype),
    )
    # If multiple threads were affected (shouldn't happen with a unique id),
    # roll back to be safe.
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_ulong(thread_ident), ctypes.c_long(0)
        )


class _LessonTimeout(KeyboardInterrupt):
    """Distinct exception so we can tell timeouts apart from real Ctrl+C."""


class CodeRunner:
    """Execute Python source with capture + a hard wall-clock timeout."""

    def __init__(self, timeout_seconds: float = 10.0):
        self.timeout = timeout_seconds

    # ----------------------------------------------------------- run user code
    def run(self, source: str) -> RunResult:
        # Build a synthetic module so dataclasses / pickle / inspect can
        # resolve cls.__module__ via sys.modules.
        lesson_module = types.ModuleType(_LESSON_MODULE_NAME)
        lesson_module.__dict__["__builtins__"] = builtins
        sys.modules[_LESSON_MODULE_NAME] = lesson_module
        scope: Dict[str, Any] = lesson_module.__dict__
        out, err = io.StringIO(), io.StringIO()
        result = RunResult(ok=False)
        runtime: Dict[str, Any] = {"exc": None, "out_str": "", "err_str": ""}

        def _target():
            try:
                with redirect_stdout(out), redirect_stderr(err):
                    code = compile(source, "<lesson>", "exec")
                    exec(code, scope)
            except BaseException as e:  # noqa: BLE001 — we want everything
                runtime["exc"] = e
            finally:
                runtime["out_str"] = out.getvalue()
                runtime["err_str"] = err.getvalue()

        worker = threading.Thread(target=_target, daemon=True, name="pyforge-runner")
        t0 = time.perf_counter()
        worker.start()
        worker.join(self.timeout)

        if worker.is_alive():
            # Inject a timeout exception; give it a short grace window to unwind.
            if worker.ident is not None:
                _async_raise(worker.ident, _LessonTimeout)
            worker.join(0.5)
            result.error = (
                f"Execution exceeded {self.timeout:.1f}s timeout — "
                f"check for infinite loops."
            )
        else:
            exc = runtime["exc"]
            if exc is None:
                result.ok = True
            elif isinstance(exc, _LessonTimeout):
                result.error = "Execution interrupted by timeout."
            elif isinstance(exc, SystemExit):
                result.error = "SystemExit"
            else:
                result.error = "".join(
                    traceback.format_exception(type(exc), exc, exc.__traceback__)
                )

        result.duration_ms = (time.perf_counter() - t0) * 1000
        result.stdout = runtime["out_str"]
        result.stderr = runtime["err_str"]
        result.scope = {
            k: v for k, v in scope.items()
            if not k.startswith("__")
        }
        # Remove the synthetic module so successive runs start clean.
        sys.modules.pop(_LESSON_MODULE_NAME, None)
        return result

    # ----------------------------------------------------------- check exercise
    def check_exercise(self, source: str, assert_code: str) -> CheckResult:
        """
        Run the user's source, then evaluate the lesson's `assert_code` against
        the resulting scope. The asserter sees:
            - every variable the user defined
            - `_stdout` and `_stderr` (strings)
            - `_vars` (dict mirror of the scope)
        """
        run = self.run(source)
        if not run.ok:
            return CheckResult(passed=False,
                               detail=run.error or "Code did not run successfully.")

        env = dict(run.scope)
        env["_stdout"] = run.stdout
        env["_stderr"] = run.stderr
        env["_vars"]   = run.scope

        try:
            exec(assert_code, env)
            return CheckResult(passed=True, detail="✓ Looks good!")
        except AssertionError as e:
            return CheckResult(passed=False, detail=f"Check failed: {e or 'assertion failed'}")
        except Exception:
            tb = traceback.format_exc(limit=2)
            return CheckResult(passed=False, detail=f"Checker error:\n{tb}")
