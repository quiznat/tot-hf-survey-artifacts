"""Runnable optimization helpers for caching and early termination."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Callable


@dataclass
class ThoughtNode:
    score: float


class CachedToTSupport:
    """Cache wrappers for evaluation and generation stages."""

    def __init__(self) -> None:
        self.evaluation_cache: dict[str, float] = {}
        self.generation_cache: dict[str, list[str]] = {}

    @staticmethod
    def _key(prompt: str) -> str:
        return hashlib.md5(prompt.encode("utf-8")).hexdigest()

    def cached_evaluate(self, prompt: str, evaluate_fn: Callable[[str], float]) -> float:
        key = self._key(prompt)
        if key not in self.evaluation_cache:
            self.evaluation_cache[key] = evaluate_fn(prompt)
        return self.evaluation_cache[key]

    def cached_generate(
        self,
        prompt: str,
        k: int,
        generate_fn: Callable[[str, int], list[str]],
    ) -> list[str]:
        key = f"{self._key(prompt)}::{k}"
        if key not in self.generation_cache:
            self.generation_cache[key] = generate_fn(prompt, k)
        return self.generation_cache[key]


class EarlyTerminationPolicy:
    """Threshold-based early termination check."""

    def __init__(self, confidence_threshold: float = 0.9) -> None:
        self.confidence_threshold = confidence_threshold

    def should_terminate(self, beams: list[ThoughtNode]) -> bool:
        if not beams:
            return False
        best = max(beams, key=lambda n: n.score)
        heuristic_confidence = best.score / 10.0
        return heuristic_confidence >= self.confidence_threshold
