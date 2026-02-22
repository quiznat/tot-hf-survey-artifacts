"""Runnable prompt template helpers used in Section 2 examples."""


def build_generation_prompt(task: str, current_path: str, k: int) -> str:
    """Build a prompt for generating k candidate next steps."""
    return f"""
Given the task: {task}
And current progress: {current_path}

Generate {k} different possible next steps. Each step should represent
a concrete action toward solving the problem. Consider diverse approaches.

Steps:
1.
2.
3.
""".strip()


def build_evaluation_prompt(task: str, thought_path: str) -> str:
    """Build a prompt for scoring partial-solution promise on a 0-10 scale."""
    return f"""
Given the task: {task}
And current progress: {thought_path}

Rate how promising this approach is on a scale of 0-10:
- 0-3: Likely incorrect or counterproductive
- 4-6: Might help but uncertain
- 7-10: Clearly advances toward solution

Rating:
""".strip()
