"""Tree-of-Thought runner implementations.

Active mode:
- model_decompose_search: generic model-driven decomposition + search (default)

Legacy candidate-search mode remains in this file only for historical reference and
is intentionally disabled at runtime.
"""

from __future__ import annotations

from dataclasses import asdict
import re
from typing import Any, Callable, List, Tuple

from ..metrics import estimate_tokens
from ..models import RunnerExecution, SearchSummary, ThoughtNode
from .base import BaseRunner

ThoughtGenerator = Callable[[ThoughtNode, Any, int], List[str]]
ThoughtEvaluator = Callable[[str, Any], float]


class ToTRunner(BaseRunner):
    """Tree-of-Thought runner with configurable search behavior."""

    runner_id = "tot-prototype"

    def _execute(self, input_data: Any) -> RunnerExecution:
        mode = str(self.config.get("tot_mode", "model_decompose_search")).strip().lower()
        if mode in {"legacy", "legacy_candidate_search", "candidate_search"}:
            raise RuntimeError(
                "Legacy ToT mode is disabled. Use tot_mode=model_decompose_search."
            )
        return self._execute_model_decompose_search(input_data)

    def _execute_model_decompose_search(self, input_data: Any) -> RunnerExecution:
        assert self.task is not None

        max_depth = int(self.config.get("max_depth", 3))
        branch_factor = int(self.config.get("branch_factor", 3))
        frontier_width = int(self.config.get("frontier_width", 3))
        decomposition_rounds = max(1, int(self.config.get("decomposition_rounds", 1)))
        evaluator_mode = str(self.config.get("evaluator_mode", "model_self_eval"))

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
        seen_states: set[str] = set()
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
        thought_generator = self.config.get("candidate_generator")
        thought_evaluator = self.config.get("candidate_evaluator")

        for round_index in range(1, decomposition_rounds + 1):
            trace.append(f"DECOMPOSE {round_index} frontier={len(frontier)}")
            next_frontier: List[ThoughtNode] = []

            for node in frontier:
                summary.expanded_nodes += 1
                thoughts, in_tokens, out_tokens = self._generate_thoughts(
                    node=node,
                    input_data=input_data,
                    branch_factor=branch_factor,
                    disallowed=seen_states,
                    generator=thought_generator,
                    phase="decompose",
                )
                tokens_in += in_tokens
                tokens_out += out_tokens

                if not thoughts:
                    trace.append(f"NODE {node.node_id} generated no thoughts")
                    continue

                for thought in thoughts[:branch_factor]:
                    state = _append_state(node.candidate, thought)
                    if state in seen_states:
                        trace.append(f"NODE {node.node_id} duplicate_skipped state={_trace_preview(state)}")
                        continue
                    seen_states.add(state)

                    score, eval_in_tokens, eval_out_tokens = self._evaluate_thought_state(
                        thought_state=state,
                        input_data=input_data,
                        evaluator=thought_evaluator,
                        evaluator_mode=evaluator_mode,
                    )
                    tokens_in += eval_in_tokens
                    tokens_out += eval_out_tokens

                    terminal_answer = self._extract_valid_terminal_answer(state, input_data)
                    child = ThoughtNode(
                        node_id=f"n{next_index:04d}",
                        parent_id=node.node_id,
                        depth=node.depth + 1,
                        candidate=state,
                        score=score,
                        cumulative_score=node.cumulative_score + score,
                        is_terminal=terminal_answer is not None,
                    )
                    next_index += 1
                    summary.generated_nodes += 1

                    trace.append(
                        f"NODE {child.node_id} parent={child.parent_id} score={child.score:.4f} "
                        f"cum={child.cumulative_score:.4f} terminal={child.is_terminal} thought={_trace_preview(thought)}"
                    )

                    if terminal_answer is not None:
                        summary.terminal_nodes += 1
                        summary.stop_reason = "terminal_solution"
                        search_summary = asdict(summary)
                        search_summary["tot_mode"] = "model_decompose_search"
                        search_summary["decomposition_rounds"] = decomposition_rounds
                        return RunnerExecution(
                            outcome="success",
                            final_answer=terminal_answer,
                            notes="tot model-decompose search found terminal candidate",
                            trace=trace,
                            tokens_in=tokens_in,
                            tokens_out=tokens_out,
                            extra={"search_summary": search_summary},
                        )

                    next_frontier.append(child)

            if not next_frontier:
                summary.stop_reason = "decomposition_exhausted"
                search_summary = asdict(summary)
                search_summary["tot_mode"] = "model_decompose_search"
                search_summary["decomposition_rounds"] = decomposition_rounds
                return RunnerExecution(
                    outcome="failure",
                    final_answer="",
                    notes="tot model-decompose search exhausted during decomposition",
                    trace=trace,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                    error_type="empty_frontier",
                    extra={"search_summary": search_summary},
                )

            next_frontier.sort(key=lambda item: item.cumulative_score, reverse=True)
            frontier = next_frontier[:frontier_width]
            summary.peak_frontier_size = max(summary.peak_frontier_size, len(frontier))

        for depth in range(1, max_depth + 1):
            trace.append(f"DEPTH {depth} frontier={len(frontier)}")
            next_frontier = []

            for node in frontier:
                summary.expanded_nodes += 1
                thoughts, in_tokens, out_tokens = self._generate_thoughts(
                    node=node,
                    input_data=input_data,
                    branch_factor=branch_factor,
                    disallowed=seen_states,
                    generator=thought_generator,
                    phase="expand",
                )
                tokens_in += in_tokens
                tokens_out += out_tokens

                if not thoughts:
                    trace.append(f"NODE {node.node_id} generated no thoughts")
                    continue

                for thought in thoughts[:branch_factor]:
                    state = _append_state(node.candidate, thought)
                    if state in seen_states:
                        trace.append(f"NODE {node.node_id} duplicate_skipped state={_trace_preview(state)}")
                        continue
                    seen_states.add(state)

                    score, eval_in_tokens, eval_out_tokens = self._evaluate_thought_state(
                        thought_state=state,
                        input_data=input_data,
                        evaluator=thought_evaluator,
                        evaluator_mode=evaluator_mode,
                    )
                    tokens_in += eval_in_tokens
                    tokens_out += eval_out_tokens

                    terminal_answer = self._extract_valid_terminal_answer(state, input_data)
                    child = ThoughtNode(
                        node_id=f"n{next_index:04d}",
                        parent_id=node.node_id,
                        depth=node.depth + 1,
                        candidate=state,
                        score=score,
                        cumulative_score=node.cumulative_score + score,
                        is_terminal=terminal_answer is not None,
                    )
                    next_index += 1
                    summary.generated_nodes += 1

                    trace.append(
                        f"NODE {child.node_id} parent={child.parent_id} score={child.score:.4f} "
                        f"cum={child.cumulative_score:.4f} terminal={child.is_terminal} thought={_trace_preview(thought)}"
                    )

                    if terminal_answer is not None:
                        summary.terminal_nodes += 1
                        summary.stop_reason = "terminal_solution"
                        search_summary = asdict(summary)
                        search_summary["tot_mode"] = "model_decompose_search"
                        search_summary["decomposition_rounds"] = decomposition_rounds
                        return RunnerExecution(
                            outcome="success",
                            final_answer=terminal_answer,
                            notes="tot model-decompose search found terminal candidate",
                            trace=trace,
                            tokens_in=tokens_in,
                            tokens_out=tokens_out,
                            extra={"search_summary": search_summary},
                        )

                    next_frontier.append(child)

            if not next_frontier:
                summary.stop_reason = "empty_frontier"
                search_summary = asdict(summary)
                search_summary["tot_mode"] = "model_decompose_search"
                search_summary["decomposition_rounds"] = decomposition_rounds
                return RunnerExecution(
                    outcome="failure",
                    final_answer="",
                    notes="tot model-decompose search frontier exhausted without candidates",
                    trace=trace,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                    error_type="empty_frontier",
                    extra={"search_summary": search_summary},
                )

            next_frontier.sort(key=lambda item: item.cumulative_score, reverse=True)
            frontier = next_frontier[:frontier_width]
            summary.peak_frontier_size = max(summary.peak_frontier_size, len(frontier))

        summary.stop_reason = "depth_limit"
        best = frontier[0] if frontier else root
        fallback = self._extract_guess_answer(best.candidate)
        search_summary = asdict(summary)
        search_summary["tot_mode"] = "model_decompose_search"
        search_summary["decomposition_rounds"] = decomposition_rounds
        return RunnerExecution(
            outcome="failure",
            final_answer=fallback,
            notes="tot model-decompose search reached depth limit without terminal answer",
            trace=trace,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            error_type="depth_limit",
            extra={"search_summary": search_summary},
        )

    def _execute_legacy(self, input_data: Any) -> RunnerExecution:
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
        seen_candidates: set[str] = set()
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
                candidates, in_tokens, out_tokens = self._generate_candidates_legacy(
                    node=node,
                    input_data=input_data,
                    branch_factor=branch_factor,
                    generator=candidate_generator,
                    disallowed=seen_candidates,
                )
                tokens_in += in_tokens
                tokens_out += out_tokens

                if not candidates:
                    trace.append(f"NODE {node.node_id} generated no candidates")
                    continue

                for candidate in candidates[:branch_factor]:
                    if candidate in seen_candidates:
                        trace.append(f"NODE {node.node_id} duplicate_skipped candidate={candidate}")
                        continue
                    seen_candidates.add(candidate)

                    score, eval_in_tokens, eval_out_tokens = self._evaluate_candidate_legacy(
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
                        search_summary = asdict(summary)
                        search_summary["tot_mode"] = "legacy_candidate_search"
                        return RunnerExecution(
                            outcome="success",
                            final_answer=child.candidate,
                            notes="tot legacy candidate search found terminal candidate",
                            trace=trace,
                            tokens_in=tokens_in,
                            tokens_out=tokens_out,
                            extra={"search_summary": search_summary},
                        )

                    next_frontier.append(child)

            if not next_frontier:
                summary.stop_reason = "empty_frontier"
                search_summary = asdict(summary)
                search_summary["tot_mode"] = "legacy_candidate_search"
                return RunnerExecution(
                    outcome="failure",
                    final_answer="",
                    notes="tot legacy candidate search frontier exhausted without candidates",
                    trace=trace,
                    tokens_in=tokens_in,
                    tokens_out=tokens_out,
                    error_type="empty_frontier",
                    extra={"search_summary": search_summary},
                )

            next_frontier.sort(key=lambda item: item.cumulative_score, reverse=True)
            frontier = next_frontier[:frontier_width]
            summary.peak_frontier_size = max(summary.peak_frontier_size, len(frontier))

        summary.stop_reason = "depth_limit"
        best = frontier[0] if frontier else root
        search_summary = asdict(summary)
        search_summary["tot_mode"] = "legacy_candidate_search"
        return RunnerExecution(
            outcome="failure",
            final_answer=best.candidate,
            notes="tot legacy candidate search reached depth limit without terminal candidate",
            trace=trace,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            error_type="depth_limit",
            extra={"search_summary": search_summary},
        )

    def _generate_thoughts(
        self,
        node: ThoughtNode,
        input_data: Any,
        branch_factor: int,
        disallowed: set[str],
        generator: ThoughtGenerator | None,
        phase: str,
    ) -> Tuple[List[str], int, int]:
        if callable(generator):
            raw = [line.strip() for line in generator(node, input_data, branch_factor) if line.strip()]
            normalized = [self._normalize_thought_line(line, input_data) for line in raw]
            return _unique_local(normalized)[:branch_factor], 0, 0

        assert self.task is not None
        total_tokens_in = 0
        total_tokens_out = 0
        collected: List[str] = []

        for attempt in range(2):
            disallowed_preview = sorted(disallowed)[:20]
            prompt = self._build_thought_prompt(
                phase=phase,
                input_data=input_data,
                current_path=node.candidate,
                branch_factor=branch_factor,
                disallowed_candidates=disallowed_preview,
                attempt=attempt,
            )
            output = self.model.generate(prompt)
            total_tokens_in += estimate_tokens(prompt)
            total_tokens_out += estimate_tokens(output)

            parsed = _parse_thought_lines(output, self.task.extract_final_answer)
            for thought in parsed:
                collected.append(self._normalize_thought_line(thought, input_data))

            unique = _unique_local(collected)
            if len(unique) >= branch_factor:
                return unique[:branch_factor], total_tokens_in, total_tokens_out

        return _unique_local(collected)[:branch_factor], total_tokens_in, total_tokens_out

    def _build_thought_prompt(
        self,
        phase: str,
        input_data: Any,
        current_path: str,
        branch_factor: int,
        disallowed_candidates: list[str],
        attempt: int,
    ) -> str:
        assert self.task is not None

        if phase == "decompose":
            prompt_builder = getattr(self.task, "build_tot_decomposition_prompt", None)
            if callable(prompt_builder):
                return prompt_builder(
                    input_data=input_data,
                    current_path=current_path,
                    branch_factor=branch_factor,
                    disallowed_candidates=disallowed_candidates,
                    attempt=attempt,
                )

        prompt_builder = getattr(self.task, "build_tot_step_prompt", None)
        if callable(prompt_builder):
            return prompt_builder(
                input_data=input_data,
                current_path=current_path,
                branch_factor=branch_factor,
                disallowed_candidates=disallowed_candidates,
                attempt=attempt,
            )

        legacy_prompt = getattr(self.task, "build_tot_candidate_prompt")
        return legacy_prompt(
            input_data=input_data,
            scratchpad=current_path,
            branch_factor=branch_factor,
            disallowed_candidates=disallowed_candidates,
            attempt=attempt,
        )

    def _normalize_thought_line(self, line: str, input_data: Any) -> str:
        cleaned = _clean_candidate_line(line)
        if not cleaned:
            return ""
        upper = cleaned.upper()
        if upper.startswith("DECOMP:"):
            return f"DECOMP: {cleaned.split(':', 1)[1].strip()}"
        if upper.startswith("STEP:"):
            return f"STEP: {cleaned.split(':', 1)[1].strip()}"
        if upper.startswith("FINAL:"):
            return f"FINAL: {cleaned.split(':', 1)[1].strip()}"
        if upper.startswith("ANSWER:"):
            return f"FINAL: {cleaned.split(':', 1)[1].strip()}"
        if upper.startswith("SOLUTION:"):
            return f"FINAL: {cleaned.split(':', 1)[1].strip()}"
        if upper.startswith("CANDIDATE:"):
            return f"FINAL: {cleaned.split(':', 1)[1].strip()}"

        assert self.task is not None
        # Treat raw valid answers as terminal thoughts when possible.
        if self.task.evaluate(cleaned, input_data):
            return f"FINAL: {cleaned}"
        return f"STEP: {cleaned}"

    def _evaluate_thought_state(
        self,
        thought_state: str,
        input_data: Any,
        evaluator: ThoughtEvaluator | None,
        evaluator_mode: str,
    ) -> Tuple[float, int, int]:
        if callable(evaluator):
            return _clamp_score(float(evaluator(thought_state, input_data))), 0, 0

        mode = evaluator_mode.strip().lower()
        if mode == "rule_based":
            return self._rule_based_state_score(thought_state, input_data), 0, 0
        if mode == "model_self_eval":
            return self._model_self_eval_state_score(thought_state, input_data)
        if mode == "hybrid":
            rule_score = self._rule_based_state_score(thought_state, input_data)
            model_score, in_tokens, out_tokens = self._model_self_eval_state_score(thought_state, input_data)
            return _clamp_score(0.6 * rule_score + 0.4 * model_score), in_tokens, out_tokens

        return self._task_binary_state_score(thought_state, input_data), 0, 0

    def _task_binary_state_score(self, thought_state: str, input_data: Any) -> float:
        answer = self._extract_marked_answer(thought_state)
        if not answer:
            return 0.0
        assert self.task is not None
        return 1.0 if self.task.evaluate(answer, input_data) else 0.0

    def _rule_based_state_score(self, thought_state: str, input_data: Any) -> float:
        assert self.task is not None

        scorer = getattr(self.task, "score_thought_state", None)
        if callable(scorer):
            try:
                return _clamp_score(float(scorer(thought_state, input_data)))
            except Exception:
                pass

        answer = self._extract_marked_answer(thought_state)
        if answer:
            if self.task.evaluate(answer, input_data):
                return 1.0
            score_candidate = getattr(self.task, "score_candidate", None)
            if callable(score_candidate):
                try:
                    return _clamp_score(float(score_candidate(answer, input_data)))
                except Exception:
                    return 0.2
            return 0.2

        return 0.5

    def _model_self_eval_state_score(self, thought_state: str, input_data: Any) -> Tuple[float, int, int]:
        assert self.task is not None
        prompt = (
            "Score this Tree-of-Thought state on a 0 to 1 scale.\n"
            "0 means the state is incorrect or unhelpful.\n"
            "1 means the state is highly promising and likely to produce a correct final answer.\n"
            "Return only one number in [0, 1].\n\n"
            f"Task prompt:\n{self.task.build_prompt(input_data)}\n\n"
            f"Thought state:\n{thought_state or '(empty)'}\n\n"
            "Score:"
        )
        output = self.model.generate(prompt).strip()
        match = re.search(r"[-+]?\d*\.?\d+", output)
        if not match:
            return 0.0, estimate_tokens(prompt), estimate_tokens(output)
        return _clamp_score(float(match.group(0))), estimate_tokens(prompt), estimate_tokens(output)

    def _extract_valid_terminal_answer(self, thought_state: str, input_data: Any) -> str | None:
        assert self.task is not None

        extractor = getattr(self.task, "extract_tot_final_answer", None)
        candidate = ""
        if callable(extractor):
            try:
                candidate = str(extractor(thought_state, input_data) or "").strip()
            except TypeError:
                candidate = str(extractor(thought_state) or "").strip()
        if not candidate:
            candidate = self._extract_marked_answer(thought_state)
        if not candidate:
            stripped = thought_state.strip()
            if "\n" not in stripped and not stripped.upper().startswith(("DECOMP:", "STEP:")):
                candidate = stripped
        if not candidate:
            return None
        if self.task.evaluate(candidate, input_data):
            return candidate
        return None

    def _extract_marked_answer(self, thought_state: str) -> str:
        lines = [line.strip() for line in thought_state.splitlines() if line.strip()]
        for line in reversed(lines):
            upper = line.upper()
            if upper.startswith("FINAL:"):
                return line.split(":", 1)[1].strip()
            if upper.startswith("ANSWER:"):
                return line.split(":", 1)[1].strip()
            if upper.startswith("SOLUTION:"):
                return line.split(":", 1)[1].strip()
        return ""

    def _extract_guess_answer(self, thought_state: str) -> str:
        answer = self._extract_marked_answer(thought_state)
        if answer:
            return answer
        stripped = thought_state.strip()
        if not stripped:
            return ""
        lines = [line.strip() for line in stripped.splitlines() if line.strip()]
        if not lines:
            return ""
        last = lines[-1]
        upper = last.upper()
        if upper.startswith("STEP:") or upper.startswith("DECOMP:"):
            return last.split(":", 1)[1].strip()
        return last

    def _generate_candidates_legacy(
        self,
        node: ThoughtNode,
        input_data: Any,
        branch_factor: int,
        generator: ThoughtGenerator | None,
        disallowed: set[str],
    ) -> Tuple[List[str], int, int]:
        if callable(generator):
            candidates = [candidate.strip() for candidate in generator(node, input_data, branch_factor) if candidate.strip()]
            return _unique_candidates(candidates, disallowed)[:branch_factor], 0, 0

        assert self.task is not None
        total_tokens_in = 0
        total_tokens_out = 0
        collected: List[str] = []
        prompt_builder = getattr(self.task, "build_tot_candidate_prompt")

        for attempt in range(2):
            disallowed_preview = sorted(disallowed)[:20]
            prompt = prompt_builder(
                input_data=input_data,
                scratchpad=node.candidate,
                branch_factor=branch_factor,
                disallowed_candidates=disallowed_preview,
                attempt=attempt,
            )

            output = self.model.generate(prompt)
            total_tokens_in += estimate_tokens(prompt)
            total_tokens_out += estimate_tokens(output)

            parsed = _parse_candidates(output, self.task.extract_final_answer)
            for candidate in parsed:
                if candidate:
                    collected.append(candidate)

            unique = _unique_candidates(collected, disallowed)
            if len(unique) >= branch_factor:
                return unique[:branch_factor], total_tokens_in, total_tokens_out

        return _unique_candidates(collected, disallowed)[:branch_factor], total_tokens_in, total_tokens_out

    def _evaluate_candidate_legacy(
        self,
        candidate: str,
        input_data: Any,
        evaluator: ThoughtEvaluator | None,
        evaluator_mode: str,
    ) -> Tuple[float, int, int]:
        if callable(evaluator):
            return _clamp_score(float(evaluator(candidate, input_data))), 0, 0

        mode = evaluator_mode.strip().lower()
        if mode == "rule_based":
            return self._rule_based_score_legacy(candidate, input_data), 0, 0
        if mode == "model_self_eval":
            return self._model_self_eval_score_legacy(candidate, input_data)
        if mode == "hybrid":
            rule_score = self._rule_based_score_legacy(candidate, input_data)
            model_score, in_tokens, out_tokens = self._model_self_eval_score_legacy(candidate, input_data)
            return _clamp_score(0.6 * rule_score + 0.4 * model_score), in_tokens, out_tokens

        assert self.task is not None
        return (1.0, 0, 0) if self.task.evaluate(candidate, input_data) else (0.0, 0, 0)

    def _rule_based_score_legacy(self, candidate: str, input_data: Any) -> float:
        assert self.task is not None
        scorer = getattr(self.task, "score_candidate", None)
        if callable(scorer):
            return _clamp_score(float(scorer(candidate, input_data)))
        return 1.0 if self.task.evaluate(candidate, input_data) else 0.0

    def _model_self_eval_score_legacy(self, candidate: str, input_data: Any) -> Tuple[float, int, int]:
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


def _parse_candidates(output: str, extract_final_answer: Callable[[str], str]) -> List[str]:
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
        fallback = extract_final_answer(output)
        if fallback:
            fallback_line = _clean_candidate_line(fallback)
            if fallback_line:
                candidates.append(fallback_line)
    return candidates


def _parse_thought_lines(output: str, extract_final_answer: Callable[[str], str]) -> List[str]:
    thoughts: List[str] = []
    for raw_line in output.splitlines():
        line = _clean_candidate_line(raw_line)
        if not line:
            continue
        upper = line.upper()
        if upper.startswith("THOUGHT:"):
            line = f"STEP: {line.split(':', 1)[1].strip()}"
        elif upper.startswith("ANSWER:"):
            line = f"FINAL: {line.split(':', 1)[1].strip()}"
        elif upper.startswith("SOLUTION:"):
            line = f"FINAL: {line.split(':', 1)[1].strip()}"
        elif upper.startswith("CANDIDATE:"):
            line = f"FINAL: {line.split(':', 1)[1].strip()}"
        elif upper.startswith("DECOMP:") or upper.startswith("STEP:") or upper.startswith("FINAL:"):
            line = line
        else:
            line = f"STEP: {line}"
        thoughts.append(line)

    if not thoughts:
        fallback = extract_final_answer(output)
        if fallback:
            fallback_line = _clean_candidate_line(fallback)
            if fallback_line:
                thoughts.append(f"FINAL: {fallback_line}")
    return thoughts


def _unique_candidates(candidates: List[str], disallowed: set[str]) -> List[str]:
    unique: List[str] = []
    seen_local: set[str] = set()
    for candidate in candidates:
        if candidate in disallowed:
            continue
        if candidate in seen_local:
            continue
        seen_local.add(candidate)
        unique.append(candidate)
    return unique


def _unique_local(values: List[str]) -> List[str]:
    unique: List[str] = []
    seen: set[str] = set()
    for value in values:
        if not value:
            continue
        if value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique


def _append_state(current_path: str, thought: str) -> str:
    line = thought.strip()
    if not current_path:
        return line
    return f"{current_path}\n{line}"


def _trace_preview(text: str, limit: int = 160) -> str:
    flattened = re.sub(r"\s+", " ", text).strip()
    if len(flattened) <= limit:
        return flattened
    return f"{flattened[: limit - 3]}..."


def _clamp_score(score: float) -> float:
    if score < 0.0:
        return 0.0
    if score > 1.0:
        return 1.0
    return score
