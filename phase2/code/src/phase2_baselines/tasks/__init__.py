"""Benchmark task adapters."""

from .arithmetic24 import Arithmetic24Task
from .digit_permutation import DigitPermutationTask
from .linear2 import LinearSystem2Task
from .registry import create_task, resolve_task_id, supported_tasks
from .subset_sum import SubsetSumTask

__all__ = [
    "Arithmetic24Task",
    "SubsetSumTask",
    "LinearSystem2Task",
    "DigitPermutationTask",
    "create_task",
    "resolve_task_id",
    "supported_tasks",
]
