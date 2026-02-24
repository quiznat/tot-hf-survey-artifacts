"""Chain-of-thought baseline runner implementations."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
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
        tokens_in = estimate_tokens(prompt)
        tokens_out = estimate_tokens(raw_output)
        trace = [
            f"PROMPT: {prompt}",
            f"OUTPUT: {raw_output}",
            f"FINAL: {final_answer}",
        ]

        recovery_enabled = bool(self.config.get("cot_answer_recovery", False))
        if recovery_enabled and not success:
            recovered_answer, recovery_prompt, recovery_output = self._recover_answer(
                input_data=input_data,
                raw_output=raw_output,
            )
            tokens_in += estimate_tokens(recovery_prompt)
            tokens_out += estimate_tokens(recovery_output)
            trace.append(f"RECOVERY PROMPT: {recovery_prompt}")
            trace.append(f"RECOVERY OUTPUT: {recovery_output}")
            trace.append(f"RECOVERY FINAL: {recovered_answer}")
            if recovered_answer:
                final_answer = recovered_answer
                success = self.task.evaluate(final_answer, input_data)

        return RunnerExecution(
            outcome="success" if success else "failure",
            final_answer=final_answer,
            notes="cot baseline execution",
            trace=trace,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
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

    def _recover_answer(self, input_data: Any, raw_output: str) -> tuple[str, str, str]:
        assert self.task is not None
        recovery_prompt = (
            "You previously attempted this task but may have provided extra reasoning text.\n"
            "Return ONLY the final answer in task-required format.\n\n"
            f"Task:\n{self.task.build_prompt(input_data)}\n\n"
            f"Previous reasoning:\n{raw_output}\n\n"
            "Answer only:"
        )
        recovery_output = self.model.generate(recovery_prompt)
        recovered_answer = self._extract_answer(recovery_output)
        return recovered_answer, recovery_prompt, recovery_output


class CoTSelfConsistencyRunner(CoTRunner):
    """Self-consistency CoT baseline using majority vote over sampled trajectories."""

    runner_id = "baseline-cot-sc"

    def _execute(self, input_data: Any) -> RunnerExecution:
        assert self.task is not None

        samples = max(1, int(self.config.get("cot_sc_samples", 5)))
        parallel_workers = max(
            1,
            min(
                samples,
                int(self.config.get("cot_sc_parallel_workers", 1)),
            ),
        )
        vote_counts: Dict[str, int] = {}
        first_seen: Dict[str, int] = {}
        sample_outputs: List[Tuple[int, str, str, str]] = []
        tokens_in = 0
        tokens_out = 0

        def run_sample(sample_idx: int) -> Dict[str, Any]:
            prompt = self._build_prompt(
                input_data=input_data,
                sample_index=sample_idx,
                total_samples=samples,
            )
            raw_output = self.model.generate(prompt)
            answer = self._extract_answer(raw_output)
            recovery_prompt = ""
            recovery_output = ""
            sample_tokens_in = estimate_tokens(prompt)
            sample_tokens_out = estimate_tokens(raw_output)
            if bool(self.config.get("cot_answer_recovery", False)) and not self.task.evaluate(answer, input_data):
                answer, recovery_prompt, recovery_output = self._recover_answer(
                    input_data=input_data,
                    raw_output=raw_output,
                )
                sample_tokens_in += estimate_tokens(recovery_prompt)
                sample_tokens_out += estimate_tokens(recovery_output)
            return {
                "sample_idx": sample_idx,
                "prompt": prompt,
                "raw_output": raw_output,
                "answer": answer,
                "recovery_prompt": recovery_prompt,
                "recovery_output": recovery_output,
                "tokens_in": sample_tokens_in,
                "tokens_out": sample_tokens_out,
            }

        sample_results: List[Dict[str, Any]] = []
        if parallel_workers == 1:
            for sample_idx in range(1, samples + 1):
                sample_results.append(run_sample(sample_idx))
        else:
            with ThreadPoolExecutor(max_workers=parallel_workers) as executor:
                futures = {
                    executor.submit(run_sample, sample_idx): sample_idx
                    for sample_idx in range(1, samples + 1)
                }
                for future in as_completed(futures):
                    sample_results.append(future.result())

        sample_results.sort(key=lambda entry: int(entry["sample_idx"]))

        for result in sample_results:
            sample_idx = int(result["sample_idx"])
            answer = str(result["answer"])
            vote_key = answer if answer else "<empty>"
            vote_counts[vote_key] = vote_counts.get(vote_key, 0) + 1
            first_seen.setdefault(vote_key, sample_idx)
            sample_outputs.append((sample_idx, str(result["prompt"]), str(result["raw_output"]), answer))
            tokens_in += int(result["tokens_in"])
            tokens_out += int(result["tokens_out"])
            recovery_prompt = str(result["recovery_prompt"])
            recovery_output = str(result["recovery_output"])
            if recovery_prompt:
                sample_outputs.append(
                    (
                        sample_idx,
                        f"RECOVERY PROMPT: {recovery_prompt}",
                        f"RECOVERY OUTPUT: {recovery_output}",
                        answer,
                    )
                )

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
                "cot_sc_parallel_workers": parallel_workers,
                "cot_sc_vote_counts": ranked_votes,
                "cot_sc_winner_votes": winner_votes,
            },
        )
