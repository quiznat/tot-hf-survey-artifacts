"""Runnable ToT runtime stand-ins for integration/template listings."""

from __future__ import annotations

import ast
import heapq
import operator as op
import re
from dataclasses import dataclass

from examples.paper_snippets.agent_runtime_examples import CodeAgent, InferenceClientModel


class HeuristicToTPlanner:
    """Planner stand-in with deterministic propose/evaluate/select behavior."""

    def propose(self, task: str) -> list[str]:
        task_l = task.lower()
        if "vector database" in task_l:
            return [
                "Gather official docs and release notes",
                "Search comparative blog posts",
                "Collect community sentiment",
            ]
        return [
            "Clarify objective and constraints",
            "Generate two alternative plans",
            "Choose highest-confidence plan",
        ]

    @staticmethod
    def evaluate(task: str, candidates: list[str]) -> list[float]:
        task_l = task.lower()
        scores: list[float] = []
        for candidate in candidates:
            score = 5.0
            c = candidate.lower()
            if "docs" in c or "official" in c:
                score += 2.5
            if "blog" in c:
                score -= 0.5
            if "sentiment" in c:
                score -= 1.0
            if "constraint" in c:
                score += 1.0
            if "vector database" in task_l and ("docs" in c or "release" in c):
                score += 1.0
            scores.append(score)
        return scores

    @staticmethod
    def select(candidates: list[str], scores: list[float]) -> str:
        if not candidates:
            return "No candidate plan available"
        best_idx = max(range(len(candidates)), key=lambda idx: scores[idx])
        return candidates[best_idx]


class ToTEnabledCodeAgent(CodeAgent):
    """CodeAgent stand-in with planner pre-step."""

    def __init__(self, *args, planner: HeuristicToTPlanner, **kwargs):
        super().__init__(*args, **kwargs)
        self.planner = planner

    def run(self, task: str, **kwargs) -> str:  # noqa: ARG002
        candidates = self.planner.propose(task)
        scores = self.planner.evaluate(task, candidates)
        high_level_plan = self.planner.select(candidates, scores)
        planned_task = (
            f"Task: {task}\n"
            f"Use this vetted high-level plan:\n{high_level_plan}"
        )
        return super().run(planned_task)


@dataclass
class ThoughtNode:
    thought: str
    parent: "ThoughtNode | None" = None
    score: float = 0.0
    depth: int = 0

    def path(self) -> list[str]:
        if self.parent is None:
            return [self.thought]
        return self.parent.path() + [self.thought]


class SimpleToTAgent:
    """Minimal runnable ToT agent template."""

    def __init__(self, model: InferenceClientModel, beam_width: int = 3, max_depth: int = 4):
        self.model = model
        self.beam_width = beam_width
        self.max_depth = max_depth

    @staticmethod
    def _generate_candidates(problem: str, path: list[str], k: int) -> list[str]:
        del problem
        depth = len(path)
        if depth == 1:
            candidates = ["identify constraints", "draft direct answer", "collect known facts"]
        elif depth == 2:
            candidates = ["derive intermediate values", "check assumptions", "search alternatives"]
        else:
            candidates = ["form final response", "verify consistency", "stop"]
        return candidates[:k]

    @staticmethod
    def _evaluate(path: list[str]) -> float:
        joined = " ".join(path).lower()
        score = 5.0
        if "identify constraints" in joined:
            score += 1.0
        if "derive intermediate values" in joined:
            score += 2.0
        if "verify consistency" in joined:
            score += 1.0
        if "draft direct answer" in joined:
            score -= 0.5
        return score

    @staticmethod
    def _is_solution(path: list[str]) -> bool:
        return "form final response" in " ".join(path).lower()

    @staticmethod
    def _format_solution(path: list[str]) -> str:
        return "\n".join(f"Step {idx + 1}: {step}" for idx, step in enumerate(path))

    def solve_with_tot(self, problem: str) -> str:
        root = ThoughtNode(thought=f"Start: {problem[:30]}...")
        beams = [root]

        for depth in range(self.max_depth):
            candidates: list[ThoughtNode] = []
            for node in beams:
                thoughts = self._generate_candidates(problem, node.path(), self.beam_width)
                for thought in thoughts:
                    child = ThoughtNode(thought=thought, parent=node, depth=depth + 1)
                    child.score = self._evaluate(child.path())
                    candidates.append(child)

            if not candidates:
                break

            beams = heapq.nlargest(self.beam_width, candidates, key=lambda n: n.score)
            for node in beams:
                if self._is_solution(node.path()):
                    return self._format_solution(node.path())

        best = max(beams, key=lambda n: n.score)
        return self._format_solution(best.path())


def evaluate_math(expression: str) -> float:
    """Safely evaluate restricted arithmetic expressions."""
    operators = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.USub: op.neg,
        ast.UAdd: op.pos,
    }

    def _eval(node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp):
            if type(node.op) not in operators:
                raise ValueError("Unsupported operator")
            return float(operators[type(node.op)](_eval(node.left), _eval(node.right)))
        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in operators:
                raise ValueError("Unsupported unary operator")
            return float(operators[type(node.op)](_eval(node.operand)))
        raise ValueError("Unsupported expression")

    parsed = ast.parse(expression, mode="eval")
    return _eval(parsed.body)


class MinimalToTAgent:
    """Reference runnable ToT variant inspired by Appendix B sketch."""

    def __init__(self, model: InferenceClientModel):
        self.model = model

    @staticmethod
    def _parse_score(raw: str, default: float = 5.0) -> float:
        match = re.search(r"-?\d+(?:\.\d+)?", raw)
        return float(match.group(0)) if match else default

    @staticmethod
    def _tool_signal(thought: str) -> float:
        cleaned = thought.strip()
        if not any(ch.isdigit() for ch in cleaned):
            return 0.0
        if not any(op_symbol in cleaned for op_symbol in "+-*/()"):
            return 0.0
        try:
            evaluate_math(cleaned)
            return 0.5
        except Exception:
            return -0.5

    @staticmethod
    def _generate_thoughts(task: str, path: list[str], beam_width: int) -> list[str]:
        del task
        if not path:
            options = ["1000 * (1 + 0.05)", "1000 + 1000*0.05", "estimate quickly"]
        elif len(path) == 1:
            options = ["* (1 + 0.05)", "repeat growth for year 2", "expand formula"]
        else:
            options = ["repeat growth for year 3", "compute final numeric value", "final answer"]
        return options[:beam_width]

    def tot_solve(self, task: str, beam_width: int = 3, max_depth: int = 4) -> list[str]:
        beams: list[tuple[float, list[str]]] = [(0.0, [])]

        for _depth in range(max_depth):
            candidates: list[tuple[float, list[str]]] = []
            for score, path in beams:
                thoughts = self._generate_thoughts(task, path, beam_width)
                for thought in thoughts:
                    new_path = path + [thought]
                    score_text = self.model.generate(f"Rate quality 0-10: {new_path}")
                    new_score = score + self._parse_score(score_text) + self._tool_signal(thought)
                    candidates.append((new_score, new_path))

            if not candidates:
                break
            beams = heapq.nlargest(beam_width, candidates, key=lambda pair: pair[0])

        return beams[0][1] if beams else []


class CollaborativeToT:
    """Multiple local agents exploring and sharing candidate thoughts."""

    def __init__(self, agents: list[CodeAgent]):
        self.agents = agents
        self.shared_memory: dict[str, str] = {}

    def collaborative_solve(self, task: str) -> dict[str, object]:
        contributions: list[dict[str, str]] = []
        for idx, agent in enumerate(self.agents, start=1):
            thought = agent.run(f"{task} | agent_{idx} perspective")
            key = f"agent_{idx}"
            self.shared_memory[key] = thought
            contributions.append({"agent": key, "thought": thought})

        selected = max(contributions, key=lambda row: len(row["thought"])) if contributions else None
        return {
            "task": task,
            "contributions": contributions,
            "selected": selected,
            "shared_memory": dict(self.shared_memory),
        }
