"""Runnable walkthrough fixtures for previously illustrative manuscript listings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


def tennis_ball_cot_trace() -> str:
    """Return a deterministic CoT-style solution trace for the tennis-ball example."""
    lines = [
        "Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls.",
        "Each can has 3 tennis balls. How many tennis balls does he have now?",
        "",
        "A: Roger started with 5 balls.",
        "He buys 2 cans, each with 3 balls, so that's 2 * 3 = 6 balls.",
        "5 + 6 = 11.",
        "The answer is 11.",
    ]
    return "\n".join(lines)


def math_thought_decomposition() -> list[str]:
    """Thought decomposition for a simple arithmetic expression."""
    return [
        "T1: Calculate first parentheses: 15 + 27 = 42",
        "T2: Calculate second parentheses: 42 - 18 = 24",
        "T3: Multiply results from T1 and T2: 42 * 24 = 1008",
    ]


def creative_thought_decomposition() -> list[str]:
    """Thought decomposition for a creative writing task."""
    return [
        "T1: Choose setting (modern city, historical period, future)",
        "T2: Select detective archetype (hardboiled, amateur, professional)",
        "T3: Determine mystery type (murder, theft, disappearance)",
        "T4: Plan plot structure (clues, red herrings, resolution)",
    ]


@dataclass(frozen=True)
class ToTState:
    """State object for the runnable ToT loop demo."""

    steps: tuple[str, ...]
    score: float


def _default_generate(problem: str, state: ToTState) -> list[str]:
    del problem
    if not state.steps:
        return ["collect constraints", "guess answer", "identify goal"]
    if len(state.steps) == 1:
        return ["derive intermediate values", "verify assumptions", "estimate quickly"]
    return ["produce final answer", "double-check arithmetic", "stop early"]


def _default_evaluate(problem: str, candidate_steps: tuple[str, ...]) -> float:
    problem_l = problem.lower()
    joined = " ".join(candidate_steps).lower()
    score = 5.0
    if "identify goal" in joined:
        score += 1.0
    if "derive intermediate values" in joined:
        score += 2.0
    if "double-check arithmetic" in joined:
        score += 1.5
    if "guess answer" in joined:
        score -= 1.5
    if "stop early" in joined:
        score -= 1.0
    if "math" in problem_l or "calculate" in problem_l:
        if "derive intermediate values" in joined:
            score += 0.5
    return score


def run_tot_algorithm(
    problem: str,
    *,
    beam_width: int = 2,
    max_depth: int = 3,
    generate_fn: Callable[[str, ToTState], list[str]] = _default_generate,
    evaluate_fn: Callable[[str, tuple[str, ...]], float] = _default_evaluate,
) -> dict[str, object]:
    """Runnable ToT loop for section-level algorithm demonstration."""
    beams = [ToTState(steps=tuple(), score=0.0)]
    explored = 0

    for _depth in range(max_depth):
        candidates: list[ToTState] = []
        for state in beams:
            for thought in generate_fn(problem, state):
                new_steps = state.steps + (thought,)
                score = evaluate_fn(problem, new_steps)
                explored += 1
                candidates.append(ToTState(steps=new_steps, score=score))

        if not candidates:
            break
        candidates.sort(key=lambda s: s.score, reverse=True)
        beams = candidates[:beam_width]

    best = max(beams, key=lambda s: s.score)
    return {
        "best_steps": list(best.steps),
        "best_score": best.score,
        "explored_states": explored,
        "beam_width": beam_width,
        "max_depth": max_depth,
    }


def build_traditional_tool_call(expression: str) -> dict[str, object]:
    """Return a JSON-serializable traditional tool-call payload."""
    return {"tool": "calculator", "parameters": {"expression": expression}}


def tool_selection_walkthrough() -> dict[str, object]:
    """Structured version of the section 4.3.1 exploration narrative."""
    paths = [
        {"name": "Path A", "summary": "Blog-post-first comparison", "rating": "medium"},
        {"name": "Path B", "summary": "Docs + repository evidence", "rating": "high"},
        {"name": "Path C", "summary": "Community sentiment sweep", "rating": "low"},
    ]
    return {
        "task": "Compare two open-source vector databases for a production RAG stack",
        "paths": paths,
        "selected": "Path B",
        "selection_reason": "source quality and reproducibility",
    }


def market_analysis_plan() -> dict[str, object]:
    """Structured rendering of the section 4.3.3 multi-step plan."""
    return {
        "task": "Prepare a market analysis report on electric vehicles",
        "selected_research": "Branch A",
        "selected_analysis": "Option 2",
        "selected_format": "Format C",
        "execution_plan": [
            "Week 1: Source acquisition (reports, filings, policy updates)",
            "Week 2: Data extraction and normalization",
            "Week 3: Comparative analysis across manufacturers and regions",
            "Week 4: Draft report with claim-level citations",
            "Week 5: Validation pass (fact checks + consistency review)",
            "Week 6: Final report and appendix packaging",
        ],
    }


def financial_case_study() -> dict[str, object]:
    """Runnable synthetic walkthrough for section 4.4.1."""
    return {
        "traditional_steps": [
            'Search for "Company Q3 2024 earnings"',
            "Extract revenue figure",
            "Calculate YoY growth",
        ],
        "selected_strategy": "Strategy B",
        "execution_steps": [
            "Retrieve 10-Q filing",
            "Extract key metrics",
            "Compare to analyst estimates",
            "Analyze segment performance",
            "Check cash position and debt",
            "Search for management commentary",
        ],
    }


def creative_case_study() -> dict[str, object]:
    """Runnable synthetic walkthrough for section 4.4.2."""
    return {
        "constraints": {
            "target": "Gen Z audience",
            "channels": ["TikTok", "Instagram"],
            "theme": "Sustainability",
            "budget": "$50K",
        },
        "selected_concept": "Concept B",
        "evaluation_weights": {
            "budget_fit": 0.25,
            "brand_alignment": 0.30,
            "engagement_potential": 0.30,
            "measurability": 0.15,
        },
        "execution_plan": [
            "Week 1: Filter development and testing",
            "Week 2-3: Soft launch with beta users",
            "Week 4: Full campaign launch",
            "Week 5-6: Monitor and optimize",
            "Week 7: Results analysis and report",
        ],
    }


def debugging_case_study() -> dict[str, object]:
    """Runnable synthetic walkthrough for section 4.4.3."""
    return {
        "error": "AttributeError: 'NoneType' object has no attribute 'strip'",
        "hypotheses": [
            ("H1", "Function returns None before .strip() is called", "High"),
            ("H2", "Variable overwritten with None somewhere", "Medium"),
            ("H3", "Conditional branch not handling None case", "High"),
            ("H4", "External API returning None unexpectedly", "Low"),
        ],
        "resolution": "Add null check before calling .strip()",
    }


def multimodal_tree_outline() -> dict[str, object]:
    """Structured outline for section 6.1.2."""
    return {
        "root": "Visual Thought Tree",
        "nodes": [
            "Image understanding nodes",
            "Visual reasoning branches",
            "Cross-modal integration points",
        ],
        "example_task": "Design a logo based on these brand values",
    }


def hierarchical_tree_outline() -> dict[str, object]:
    """Structured outline for section 6.1.3."""
    return {
        "high_level_phases": [
            {"phase": "Research", "subtree": "research strategies"},
            {"phase": "Analysis", "subtree": "analysis methods"},
            {"phase": "Synthesis", "subtree": "writing approaches"},
        ]
    }
