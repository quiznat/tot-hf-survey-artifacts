"""Simple model adapters for deterministic local scaffolding."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ScriptedModel:
    """Deterministic adapter returning pre-scripted responses in order."""

    responses: list[str] = field(default_factory=list)
    fallback: str = ""

    def generate(self, prompt: str) -> str:
        del prompt
        if self.responses:
            return self.responses.pop(0)
        return self.fallback
