"""Chain-of-thought baseline runner implementations."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..metrics import estimate_tokens
from ..models import RunnerExecution
from .base import BaseRunner


class CoTRunner(BaseRunner):
    """Single-path Chain-of-Thought baseline with tagged final output."""

    runner_id = "baseline-cot"

    def _execute(self, input_data: Any) -> RunnerExecution:
        assert self.task is not None

        prompt = self._build_prompt(input_data=input_data, sample_index=1, total_samples=1)
        raw_output = self.model.generate(prompt)
        final_answer = self._extract_answer(raw_output)
        success = self.task.evaluate(final_answer, input_data)

        return RunnerExecution(
            outcome="success" if success else "failure",
            final_answer=final_answer,
            notes="cot baseline execution",
            trace=[
                f"PROMPT: {prompt}",
                f"OUTPUT: {raw_output}",
                f"FINAL: {final_answer}",
            ],
            tokens_in=estimate_tokens(prompt),
            tokens_out=estimate_tokens(raw_output),
        )

    def _build_prompt(self, input_data: Any, sample_index: int, total_samples: int) -> str:
        assert self.task is not None
        builder = getattr(self.task, "build_cot_prompt", None)
        if callable(builder):
            try:
                return str(builder(input_data, sample_index, total_samples))
            except TypeError:
                # Backward-compat with older task helpers that only accept input_data.
                return str(builder(input_data))

        task_prompt = self.task.build_prompt(input_data)
        return (
            f"{task_prompt}\n\n"
            "Think step by step before answering.\n"
            "End with exactly one line in this format:\n"
            "FINAL: <answer>\n"
        )

    def _extract_answer(self, raw_output: str) -> str:
        assert self.task is not None
        answer = self.task.extract_final_answer(raw_output).strip()
        if answer:
            return answer
        return raw_output.strip()


class CoTSelfConsistencyRunner(CoTRunner):
    """Self-consistency CoT baseline using majority vote over sampled trajectories."""

    runner_id = "baseline-cot-sc"

    def _execute(self, input_data: Any) -> RunnerExecution:
        assert self.task is not None

        samples = max(1, int(self.config.get("cot_sc_samples", 5)))
        vote_counts: Dict[str, int] = {}
        first_seen: Dict[str, int] = {}
        sample_outputs: List[Tuple[int, str, str, str]] = []
        tokens_in = 0
        tokens_out = 0

        for sample_idx in range(1, samples + 1):
            prompt = self._build_prompt(
                input_data=input_data,
                sample_index=sample_idx,
                total_samples=samples,
            )
            raw_output = self.model.generate(prompt)
            answer = self._extract_answer(raw_output)
            vote_key = answer if answer else "<empty>"

            vote_counts[vote_key] = vote_counts.get(vote_key, 0) + 1
            first_seen.setdefault(vote_key, sample_idx)
            sample_outputs.append((sample_idx, prompt, raw_output, answer))
            tokens_in += estimate_tokens(prompt)
            tokens_out += estimate_tokens(raw_output)

        ranked_votes = sorted(
            vote_counts.items(),
            key=lambda item: (-item[1], first_seen.get(item[0], 10**9)),
        )
        winner_key, winner_votes = ranked_votes[0]
        final_answer = "" if winner_key == "<empty>" else winner_key
        success = self.task.evaluate(final_answer, input_data)

        trace: List[str] = []
        for sample_idx, prompt, raw_output, answer in sample_outputs:
            trace.append(f"SAMPLE {sample_idx} PROMPT: {prompt}")
            trace.append(f"SAMPLE {sample_idx} OUTPUT: {raw_output}")
            trace.append(f"SAMPLE {sample_idx} FINAL: {answer}")
        trace.append(
            "VOTE SUMMARY: "
            + ", ".join(f"{key} -> {count}" for key, count in ranked_votes[:10])
        )
        trace.append(
            f"VOTE WINNER: {final_answer} ({winner_votes}/{samples})"
        )

        return RunnerExecution(
            outcome="success" if success else "failure",
            final_answer=final_answer,
            notes=f"cot self-consistency baseline execution (samples={samples})",
            trace=trace,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            extra={
                "cot_sc_samples": samples,
                "cot_sc_vote_counts": ranked_votes,
                "cot_sc_winner_votes": winner_votes,
            },
        )
