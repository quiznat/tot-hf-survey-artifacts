"""Runnable strategy-pattern examples backing Sections 4.3 and 5.2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class CandidatePath:
    """High-level tool sequence proposal."""

    name: str
    steps: list[str]


def default_candidates() -> list[CandidatePath]:
    """Candidate sequences used in the tool-selection example."""
    return [
        CandidatePath(
            name="blog_post_first",
            steps=[
                "search comparative blog posts",
                "extract benchmark snippets",
                "summarize trade-offs",
            ],
        ),
        CandidatePath(
            name="docs_and_repo_evidence",
            steps=[
                "parse official docs for capabilities",
                "collect GitHub activity and release cadence",
                "build feature and reliability matrix",
            ],
        ),
        CandidatePath(
            name="community_sentiment",
            steps=[
                "collect forum discussions",
                "aggregate anecdotal impressions",
            ],
        ),
    ]


def evaluate_candidate(task: str, candidate: CandidatePath) -> float:
    """Simple deterministic heuristic used for runnable examples."""
    task_l = task.lower()
    score = 5.0
    if "production" in task_l or "rag" in task_l:
        if "docs" in candidate.name or "repo" in candidate.name:
            score += 3.0
        if "blog" in candidate.name:
            score -= 1.0
        if "sentiment" in candidate.name:
            score -= 2.0
    if "reproduc" in task_l and ("docs" in candidate.name or "repo" in candidate.name):
        score += 1.0
    return score


def execute_candidate(candidate: CandidatePath) -> str:
    """Execution stand-in used by traditional and ToT selectors."""
    return f"executed:{candidate.name}"


def traditional_agent(
    task: str,
    *,
    candidates: list[CandidatePath] | None = None,
    execute_fn: Callable[[CandidatePath], str] = execute_candidate,
) -> str:
    """
    Single-path selection baseline.

    Traditional baseline commits to the first parsed candidate and executes it.
    """
    choices = candidates or default_candidates()
    first_choice = choices[0]
    return execute_fn(first_choice)


def tot_agent(
    task: str,
    *,
    candidates: list[CandidatePath] | None = None,
    evaluate_fn: Callable[[str, CandidatePath], float] = evaluate_candidate,
    execute_fn: Callable[[CandidatePath], str] = execute_candidate,
) -> tuple[CandidatePath, list[tuple[str, float]], str]:
    """Evaluate multiple candidates, select the best path, and execute it."""
    choices = candidates or default_candidates()
    scored = [(candidate, evaluate_fn(task, candidate)) for candidate in choices]
    best_candidate, _ = max(scored, key=lambda pair: pair[1])
    ranked = [(candidate.name, score) for candidate, score in scored]
    return best_candidate, ranked, execute_fn(best_candidate)


def compare_tool_selection(task: str) -> dict[str, object]:
    """Convenience helper used directly in the paper snippet."""
    baseline_result = traditional_agent(task)
    best_candidate, ranked_scores, tot_result = tot_agent(task)
    return {
        "traditional_result": baseline_result,
        "tot_best_candidate": best_candidate.name,
        "tot_ranked_scores": ranked_scores,
        "tot_result": tot_result,
    }


@dataclass
class RecoveryReport:
    completed_actions: list[str]
    retry_count: int
    fallback_actions: list[str]
    replanned_from_step: int | None
    errors: list[str]


class RecoverableAgent:
    """Runnable recovery/backtracking stand-in for Section 4.3.2."""

    def __init__(self) -> None:
        self.errors: list[str] = []

    @staticmethod
    def execute_action(action: str) -> str:
        if "fail" in action:
            raise RuntimeError(f"simulated failure for action={action}")
        if "invalid" in action:
            return "INVALID_RESULT"
        return f"ok:{action}"

    @staticmethod
    def verify_result(result: str) -> bool:
        return not result.startswith("INVALID")

    @staticmethod
    def generate_alternatives(action: str, step_index: int) -> list[str]:
        del step_index
        normalized = action.replace("fail_", "").replace("invalid_", "")
        return [f"fallback_{normalized}", f"backup_{normalized}"]

    def log_error(self, action: str, err: Exception) -> None:
        self.errors.append(f"{action}: {err}")

    def execute_with_recovery(self, action_plan: list[str]) -> RecoveryReport:
        completed: list[str] = []
        retry_count = 0
        fallback_actions: list[str] = []
        replanned_from_step: int | None = None

        for index, action in enumerate(action_plan):
            try:
                result = self.execute_action(action)
                if self.verify_result(result):
                    completed.append(action)
                    continue
            except Exception as err:
                self.log_error(action, err)

            recovered = False
            for alternative in self.generate_alternatives(action, index):
                retry_count += 1
                try:
                    alternative_result = self.execute_action(alternative)
                except Exception as err:
                    self.log_error(alternative, err)
                    continue

                if self.verify_result(alternative_result):
                    fallback_actions.append(alternative)
                    completed.append(alternative)
                    recovered = True
                    break

            if recovered:
                continue

            replanned_from_step = max(index - 1, 0)
            break

        return RecoveryReport(
            completed_actions=completed,
            retry_count=retry_count,
            fallback_actions=fallback_actions,
            replanned_from_step=replanned_from_step,
            errors=list(self.errors),
        )


class HybridReasoningAgent:
    """Switch between single-path and tree-style reasoning by complexity."""

    def __init__(self, complexity_threshold: int = 7) -> None:
        self.complexity_threshold = complexity_threshold

    @staticmethod
    def assess_complexity(task: str) -> int:
        task_l = task.lower()
        score = 2
        token_count = len(task.split())
        if token_count >= 10:
            score += 2
        if any(k in task_l for k in ("compare", "trade-off", "ambigu", "multi-step", "plan")):
            score += 3
        if any(k in task_l for k in ("and", "or", "while")):
            score += 1
        return max(1, min(score, 10))

    @staticmethod
    def run_cot(task: str) -> str:
        return f"cot:{task}"

    @staticmethod
    def run_tot(task: str) -> str:
        return f"tot:{task}"

    def run(self, task: str) -> dict[str, object]:
        complexity = self.assess_complexity(task)
        if complexity < self.complexity_threshold:
            mode = "cot"
            output = self.run_cot(task)
        else:
            mode = "tot"
            output = self.run_tot(task)
        return {"mode": mode, "complexity": complexity, "output": output}


class AdaptiveToTAgent:
    """Adaptive beam/depth configuration using bounded heuristics."""

    def __init__(self, default_beam_width: int = 3, default_max_depth: int = 4) -> None:
        self.default_beam_width = default_beam_width
        self.default_max_depth = default_max_depth

    @staticmethod
    def _clamp(value: int, low: int, high: int) -> int:
        return max(low, min(value, high))

    @staticmethod
    def _complexity_score(task: str) -> int:
        task_l = task.lower()
        score = 2
        if len(task.split()) >= 12:
            score += 2
        if any(k in task_l for k in ("compare", "optimize", "trade-off", "design", "evaluate")):
            score += 3
        if "uncertain" in task_l or "ambiguous" in task_l:
            score += 1
        return max(1, min(score, 10))

    def estimate_config(self, task: str) -> dict[str, int]:
        complexity = self._complexity_score(task)
        beam_width = self._clamp(self.default_beam_width + (complexity - 5) // 2, 2, 5)
        max_depth = self._clamp(self.default_max_depth + (complexity - 5) // 2, 2, 6)
        return {"beam_width": beam_width, "max_depth": max_depth}

    @staticmethod
    def solve_with_tot(task: str, *, beam_width: int, max_depth: int) -> str:
        return f"tot(task={task}, beam={beam_width}, depth={max_depth})"

    def adaptive_solve(self, task: str) -> dict[str, object]:
        config = self.estimate_config(task)
        solution = self.solve_with_tot(
            task,
            beam_width=config["beam_width"],
            max_depth=config["max_depth"],
        )
        return {"config": config, "solution": solution}
