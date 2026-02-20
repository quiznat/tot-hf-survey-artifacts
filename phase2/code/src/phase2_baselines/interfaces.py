"""Interface contracts for baseline runners, tasks, and model adapters."""

from __future__ import annotations

from typing import Any, Callable, Mapping, Protocol


class ModelAdapter(Protocol):
    """Minimal model adapter contract used by runners."""

    def generate(self, prompt: str) -> str:
        """Return model output text for a prompt."""


class BenchmarkTask(Protocol):
    """Minimal benchmark task contract used by runners."""

    @property
    def task_id(self) -> str:
        """Stable task identifier."""

    def build_prompt(self, input_data: Any, scratchpad: str = "") -> str:
        """Build prompt text for a given input and optional scratchpad."""

    def extract_final_answer(self, raw_output: str) -> str:
        """Extract the final answer string from raw model output."""

    def evaluate(self, final_answer: str, input_data: Any) -> bool:
        """Evaluate final answer correctness."""

    def available_tools(self) -> Mapping[str, Callable[[str, Any], str]]:
        """Return available tool functions by name for ReAct-style runners."""
