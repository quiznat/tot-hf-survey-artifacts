"""Single-path baseline runner implementation."""

from __future__ import annotations

from typing import Any

from ..metrics import estimate_tokens
from ..models import RunnerExecution
from .base import BaseRunner


class SinglePathRunner(BaseRunner):
    """Baseline that performs one reasoning/action trajectory."""

    runner_id = "baseline-single-path"

    def _execute(self, input_data: Any) -> RunnerExecution:
        assert self.task is not None

        prompt = self.task.build_prompt(input_data)
        raw_output = self.model.generate(prompt)
        final_answer = self.task.extract_final_answer(raw_output)

        success = self.task.evaluate(final_answer, input_data)
        outcome = "success" if success else "failure"

        trace = [
            f"PROMPT: {prompt}",
            f"OUTPUT: {raw_output}",
            f"FINAL: {final_answer}",
        ]

        return RunnerExecution(
            outcome=outcome,
            final_answer=final_answer,
            notes="single-path baseline execution",
            trace=trace,
            tokens_in=estimate_tokens(prompt),
            tokens_out=estimate_tokens(raw_output),
        )
