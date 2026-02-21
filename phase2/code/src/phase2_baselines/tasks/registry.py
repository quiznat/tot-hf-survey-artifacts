"""Task registry for multi-task benchmark execution."""

from __future__ import annotations

from .arithmetic24 import Arithmetic24Task
from .digit_permutation import DigitPermutationTask
from .linear2 import LinearSystem2Task
from .subset_sum import SubsetSumTask


TASK_ALIASES = {
    "game24": Arithmetic24Task.task_id,
    "game24-demo": Arithmetic24Task.task_id,
    "subset-sum": SubsetSumTask.task_id,
    "subset-sum-demo": SubsetSumTask.task_id,
    "linear2": LinearSystem2Task.task_id,
    "linear2-demo": LinearSystem2Task.task_id,
    "digit-permutation": DigitPermutationTask.task_id,
    "digit-permutation-demo": DigitPermutationTask.task_id,
}


def resolve_task_id(task_name: str) -> str:
    key = task_name.strip().lower()
    return TASK_ALIASES.get(key, key)


def create_task(task_name: str):
    task_id = resolve_task_id(task_name)
    if task_id == Arithmetic24Task.task_id:
        return Arithmetic24Task()
    if task_id == SubsetSumTask.task_id:
        return SubsetSumTask()
    if task_id == LinearSystem2Task.task_id:
        return LinearSystem2Task()
    if task_id == DigitPermutationTask.task_id:
        return DigitPermutationTask()
    raise RuntimeError(f"Unsupported task: {task_name}")


def supported_tasks() -> list[str]:
    return sorted(
        {
            Arithmetic24Task.task_id,
            SubsetSumTask.task_id,
            LinearSystem2Task.task_id,
            DigitPermutationTask.task_id,
        }
    )
