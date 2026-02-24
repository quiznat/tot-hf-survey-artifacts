"""ReAct execution-mode normalization from legacy aliases to atomic IDs."""

from __future__ import annotations

from .react_execution_mode_reasoning_text_loop_no_tools_v1 import REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1
from .react_execution_mode_smolagents_code_agent_with_task_tools_v1 import REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1

_REACT_EXECUTION_MODE_ALIAS_TO_ATOMIC_ID = {
    REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1: REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1,
    REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1: REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1,
    "text_loop": REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1,
    "codeagent": REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1,
    "react_reasoning_text_loop_no_tools": REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1,
    "react_code_agent_with_tools": REACT_EXECUTION_MODE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1,
}


def normalize_react_execution_mode(value: str | None) -> str:
    """Normalize legacy alias into one atomic ReAct execution-mode ID."""
    key = str(value or "").strip()
    if not key:
        raise ValueError("react_execution_mode must be provided")
    if key not in _REACT_EXECUTION_MODE_ALIAS_TO_ATOMIC_ID:
        raise ValueError(f"Unsupported react_execution_mode: {value}")
    return _REACT_EXECUTION_MODE_ALIAS_TO_ATOMIC_ID[key]
