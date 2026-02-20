"""Tree-of-Thought-style runner prototype."""

from __future__ import annotations

from dataclasses import asdict
import re
from typing import Any, Callable, List, Tuple

from ..metrics import estimate_tokens
from ..models import RunnerExecution, SearchSummary, ThoughtNode
from .base import BaseRunner

CandidateGenerator = Callable[[ThoughtNode, Any, int], List[str]]
CandidateEvaluator = Callable[[str, Any], float]


class ToTRunner(BaseRunner):
    """Prototype ToT runner with configurable search depth/breadth/pruning."""

    runner_id = "tot-prototype"

    def _execute(self, input_data: Any) -> RunnerExecution:
        assert self.task is not None

        max_depth = int(self.config.get("max_depth", 3))
        branch_factor = int(self.config.get("branch_factor", 3))
        frontier_width = int(self.config.get("frontier_width", 3))
        evaluator_mode = str(self.config.get("evaluator_mode", "task_binary"))

        root = ThoughtNode(
            node_id="root",
            parent_id=None,
            depth=0,
            candidate="",
            score=0.0,
            cumulative_score=0.0,
            is_terminal=False,
        )

        frontier: List[ThoughtNode] = [root]
        trace: List[str] = []
        tokens_in = 0
        tokens_out = 0

        summary = SearchSummary(
            max_depth=max_depth,
            branch_factor=branch_factor,
            frontier_width=frontier_width,
            expanded_nodes=0,
            generated_nodes=0,
            terminal_nodes=0,
            peak_frontier_size=1,
        )

        next_index = 1
        candidate_generator = self.config.get("candidate_generator")
        candidate_evaluator = self.config.get("candidate_evaluator")

        for depth in range(1, max_depth + 1):
            trace.append(f"DEPTH {depth} frontier={len(frontier)}")
            next_frontier: List[ThoughtNode] = []

            for node in frontier:
                summary.expanded_nodes += 1
                candidates, in_tokens, out_tokens = self._generate_candidates(
                    node=node,
                    input_data=input_data,
                    branch_factor=branch_factor,
                    generator=candidate_generator,
                )
                tokens_in += in_tokens
                tokens_out += out_tokens

                if not candidates:
                    trace.append(f"NODE {node.node_id} generated no candidates")
                    continue

                for candidate in candidates[:branch_factor]:
                    score, eval_in_tokens, eval_out_tokens = self._evaluate_candidate(
                        candidate,
                        input_data,
                        evaluator=candidate_evaluator,
                        evaluator_mode=evaluator_mode,
                    )
                    tokens_in += eval_in_tokens
                    tokens_out += eval_out_tokens
                    terminal = self.task.evaluate(candidate, input_data)
                    child = ThoughtNode(
                        node_id=f"n{next_index:04d}",
                        parent_id=node.node_id,
                        depth=depth,
                        candidate=candidate,
                        score=score,
                        cumulative_score=node.cumulative_score + score,
                        is_terminal=terminal,
                    )
                    next_index += 1
                    summary.generated_nodes += 1

                    trace.append(
                        f"NODE {child.node_id} parent={child.parent_id} score={child.score:.4f} "
                        f"cum={child.cumulative_score:.4f} terminal={child.is_terminal} candidate={child.candidate}"
                    )

                    if child.is_terminal:
                        summary.terminal_nodes += 1
                        summary.stop_reason = "terminal_solution"
                        return RunnerExecution(
                            outcome="success",
                            final_answer=child.candidate,
                            notes="tot prototype found terminal candidate",
                            trace=trace,
                            tokens_in=tokens_in,
                            tokens_out=tokens_out,
                            extra={"search_summary": asdict(summary)},
                        )

                    next_frontier.append(child)

            if not next_frontier:
                summary.stop_reason = "empty_frontier"
                return RunnerExecution(
                    outcome="failure",
                    final_answer="",
                    notes="tot prototype frontier exhausted without candidates",
                    trace=trace,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                    error_type="empty_frontier",
                    extra={"search_summary": asdict(summary)},
                )

            # Prune to top frontier_width using cumulative score.
            next_frontier.sort(key=lambda item: item.cumulative_score, reverse=True)
            frontier = next_frontier[:frontier_width]
            summary.peak_frontier_size = max(summary.peak_frontier_size, len(frontier))

        summary.stop_reason = "depth_limit"
        best = frontier[0] if frontier else root
        return RunnerExecution(
            outcome="failure",
            final_answer=best.candidate,
            notes="tot prototype reached depth limit without terminal candidate",
            trace=trace,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            error_type="depth_limit",
            extra={"search_summary": asdict(summary)},
        )

    def _generate_candidates(
        self,
        node: ThoughtNode,
        input_data: Any,
        branch_factor: int,
        generator: CandidateGenerator | None,
    ) -> Tuple[List[str], int, int]:
        if callable(generator):
            candidates = [candidate.strip() for candidate in generator(node, input_data, branch_factor) if candidate.strip()]
            return candidates[:branch_factor], 0, 0

        assert self.task is not None
        prompt = (
            self.task.build_prompt(input_data, scratchpad=node.candidate)
            + "\n\nGenerate candidate arithmetic expressions that use each provided number exactly once."
            + f"\nReturn up to {branch_factor} candidates, one per line."
            + "\nOutput only raw expressions using + - * / and parentheses."
            + "\nDo not include '=', explanations, or words."
        )
        output = self.model.generate(prompt)

        candidates: List[str] = []
        for raw_line in output.splitlines():
            line = _clean_candidate_line(raw_line)
            if not line:
                continue
            upper = line.upper()
            if upper.startswith("CANDIDATE:"):
                line = _clean_candidate_line(line.split(":", 1)[1])
            elif upper.startswith("FINAL:"):
                line = _clean_candidate_line(line.split(":", 1)[1])
            if line:
                candidates.append(line)

        if not candidates:
            fallback = self.task.extract_final_answer(output)
            if fallback:
                candidates = [_clean_candidate_line(fallback)]

        return [candidate for candidate in candidates[:branch_factor] if candidate], estimate_tokens(prompt), estimate_tokens(output)

    def _evaluate_candidate(
        self,
        candidate: str,
        input_data: Any,
        evaluator: CandidateEvaluator | None,
        evaluator_mode: str,
    ) -> Tuple[float, int, int]:
        if callable(evaluator):
            return _clamp_score(float(evaluator(candidate, input_data))), 0, 0

        mode = evaluator_mode.strip().lower()
        if mode == "rule_based":
            return self._rule_based_score(candidate, input_data), 0, 0
        if mode == "model_self_eval":
            return self._model_self_eval_score(candidate, input_data)
        if mode == "hybrid":
            rule_score = self._rule_based_score(candidate, input_data)
            model_score, in_tokens, out_tokens = self._model_self_eval_score(candidate, input_data)
            return _clamp_score(0.6 * rule_score + 0.4 * model_score), in_tokens, out_tokens

        assert self.task is not None
        return (1.0, 0, 0) if self.task.evaluate(candidate, input_data) else (0.0, 0, 0)

    def _rule_based_score(self, candidate: str, input_data: Any) -> float:
        assert self.task is not None
        scorer = getattr(self.task, "score_candidate", None)
        if callable(scorer):
            return _clamp_score(float(scorer(candidate, input_data)))
        return 1.0 if self.task.evaluate(candidate, input_data) else 0.0

    def _model_self_eval_score(self, candidate: str, input_data: Any) -> Tuple[float, int, int]:
        assert self.task is not None
        prompt = (
            "Score the following candidate solution for the task on a scale from 0 to 1.\n"
            "0 means invalid/wrong; 1 means fully correct and compliant.\n"
            "Return only one numeric value between 0 and 1.\n\n"
            f"Task input: {input_data}\n"
            f"Candidate: {candidate}\n"
            "Score:"
        )
        output = self.model.generate(prompt).strip()
        match = re.search(r"[-+]?\d*\.?\d+", output)
        if not match:
            return 0.0, estimate_tokens(prompt), estimate_tokens(output)
        return _clamp_score(float(match.group(0))), estimate_tokens(prompt), estimate_tokens(output)


def _clean_candidate_line(raw_line: str) -> str:
    line = raw_line.strip()
    line = line.strip("`")
    line = re.sub(r"^\d+\s*[\)\.\-:]\s*", "", line)
    line = re.sub(r"^[\-\*\•]\s*", "", line)
    return line.strip()


def _clamp_score(score: float) -> float:
    if score < 0.0:
        return 0.0
    if score > 1.0:
        return 1.0
    return score
