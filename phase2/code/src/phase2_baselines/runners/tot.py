"""Tree-of-Thought-style runner prototype."""

from __future__ import annotations

from dataclasses import asdict
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
                    score = self._evaluate_candidate(candidate, input_data, evaluator=candidate_evaluator)
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
            + f"\n\nGenerate up to {branch_factor} candidate final answers. One per line."
        )
        output = self.model.generate(prompt)

        candidates: List[str] = []
        for raw_line in output.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            upper = line.upper()
            if upper.startswith("CANDIDATE:"):
                line = line.split(":", 1)[1].strip()
            elif upper.startswith("FINAL:"):
                line = line.split(":", 1)[1].strip()
            candidates.append(line)

        if not candidates:
            fallback = self.task.extract_final_answer(output)
            if fallback:
                candidates = [fallback]

        return candidates[:branch_factor], estimate_tokens(prompt), estimate_tokens(output)

    def _evaluate_candidate(
        self,
        candidate: str,
        input_data: Any,
        evaluator: CandidateEvaluator | None,
    ) -> float:
        if callable(evaluator):
            return float(evaluator(candidate, input_data))
        assert self.task is not None
        return 1.0 if self.task.evaluate(candidate, input_data) else 0.0
