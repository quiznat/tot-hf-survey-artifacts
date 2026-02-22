"""Runnable stand-ins for CodeAgent/MultiStepAgent runtime examples."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


class InferenceClientModel:
    """Minimal deterministic stand-in for an inference model client."""

    def __init__(self, model_id: str):
        self.model_id = model_id

    def generate(self, prompt: str) -> str:
        lowered = prompt.lower()
        if "15th fibonacci" in lowered:
            return "610"
        if "analyze" in lowered and "summarize" in lowered:
            return "search -> analyze -> summarize"
        return f"model[{self.model_id}]: {prompt[:80]}"


class CodeAgent:
    """Minimal CodeAgent-like runtime with configuration fields."""

    def __init__(
        self,
        *,
        tools: list[Any],
        model: InferenceClientModel,
        max_steps: int = 10,
        planning_interval: int | None = None,
        additional_authorized_imports: list[str] | None = None,
        executor_type: str = "local",
        executor_kwargs: dict[str, Any] | None = None,
    ):
        self.tools = tools
        self.model = model
        self.max_steps = max_steps
        self.planning_interval = planning_interval
        self.additional_authorized_imports = additional_authorized_imports or []
        self.executor_type = executor_type
        self.executor_kwargs = executor_kwargs

    def run(self, task: str) -> str:
        return self.model.generate(task)


class MultiStepAgent(CodeAgent):
    """Simplified multi-step runner that returns an explicit planned trace."""

    def run(self, task: str) -> str:
        plan = [
            "search news and regulation updates",
            "collect representative price signals",
            "summarize likely impacts",
        ]
        return " | ".join(plan) + f" | task={task[:40]}"


@dataclass
class ChatRequest:
    message: str


def handle_chat(agent: CodeAgent, request: ChatRequest) -> dict[str, str]:
    """Framework-agnostic local chat handler equivalent to a FastAPI route."""
    response = agent.run(request.message)
    return {"response": response}
