"""Runnable monitoring/observability helpers used in Section 3.7.2."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class InMemorySpan:
    name: str
    attributes: dict[str, object] = field(default_factory=dict)

    def set_attribute(self, key: str, value: object) -> None:
        self.attributes[key] = value


class _SpanContext:
    def __init__(self, tracer: "InMemoryTracer", name: str):
        self.tracer = tracer
        self.span = InMemorySpan(name=name)

    def __enter__(self) -> InMemorySpan:
        self.tracer.last_span = self.span
        return self.span

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


class InMemoryTracer:
    def __init__(self) -> None:
        self.last_span: InMemorySpan | None = None

    def start_as_current_span(self, name: str) -> _SpanContext:
        return _SpanContext(self, name)


class InstrumentedRunner:
    """Simple runner wrapper that records task/runtime attributes."""

    def __init__(self, tracer: InMemoryTracer):
        self.tracer = tracer

    def run(
        self,
        task: str,
        run_fn: Callable[[str], str],
        steps: int,
        tools_used: list[str],
    ) -> str:
        with self.tracer.start_as_current_span("agent_run") as span:
            span.set_attribute("task", task)
            start_time = time.perf_counter()
            result = run_fn(task)
            span.set_attribute("duration", time.perf_counter() - start_time)
            span.set_attribute("steps", steps)
            span.set_attribute("tools_used", tools_used)
            return result
