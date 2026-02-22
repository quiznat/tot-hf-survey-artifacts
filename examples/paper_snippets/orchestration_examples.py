"""Runnable orchestration and recovery helpers for agent-like loops."""

from __future__ import annotations

from typing import Callable


def retry_with_recovery(
    task: str,
    run_fn: Callable[[str], str],
    add_recovery_context: Callable[[str, Exception], str],
    log_error: Callable[[Exception], None],
    max_attempts: int = 3,
) -> str:
    """Retry run_fn with recovery context injected after failures."""
    current_task = task
    last_err: Exception | None = None
    for _ in range(max_attempts):
        try:
            return run_fn(current_task)
        except Exception as err:  # pragma: no cover - branch checked in tests
            last_err = err
            log_error(err)
            current_task = add_recovery_context(current_task, err)
    if last_err is not None:
        raise last_err
    raise RuntimeError("retry_with_recovery reached invalid state")
