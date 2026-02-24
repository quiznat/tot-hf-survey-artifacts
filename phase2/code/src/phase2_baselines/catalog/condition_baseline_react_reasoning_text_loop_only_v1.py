"""Atomic condition spec: baseline ReAct reasoning text-loop only."""

from .algorithm_baseline_react_text_loop_reasoning_only_no_tools_v1 import ALGORITHM_ID, ALGORITHM_MODULE_ID
from .condition_family_baseline_react_reasoning_text_loop_no_tools import (
    CONDITION_FAMILY_BASELINE_REACT_REASONING_TEXT_LOOP_NO_TOOLS,
)
from .condition_key_baseline_react_reasoning_text_loop_only_v1 import (
    CONDITION_KEY_BASELINE_REACT_REASONING_TEXT_LOOP_ONLY_V1,
)
from .execution_surface_prompt_reasoning_loop_v1 import EXECUTION_SURFACE_PROMPT_REASONING_LOOP_V1
from .memory_surface_item_stateless_v1 import MEMORY_SURFACE_ITEM_STATELESS_V1
from .react_execution_mode_reasoning_text_loop_no_tools_v1 import (
    REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1,
)
from .runner_adapter_react_reasoning_text_loop_no_tools_v1 import (
    RUNNER_ADAPTER_REACT_REASONING_TEXT_LOOP_NO_TOOLS_V1,
)
from .tool_surface_no_tools_v1 import TOOL_SURFACE_NO_TOOLS_V1
from .type_condition_spec import ConditionSpec


CONDITION_SPEC_BASELINE_REACT_REASONING_TEXT_LOOP_ONLY_V1 = ConditionSpec(
    condition_key=CONDITION_KEY_BASELINE_REACT_REASONING_TEXT_LOOP_ONLY_V1,
    condition_id="baseline-react-text",
    condition_display_name="Baseline ReAct Reasoning Text Loop (No Tools)",
    condition_family_id=CONDITION_FAMILY_BASELINE_REACT_REASONING_TEXT_LOOP_NO_TOOLS,
    algorithm_id=ALGORITHM_ID,
    algorithm_module_id=ALGORITHM_MODULE_ID,
    runner_adapter_id=RUNNER_ADAPTER_REACT_REASONING_TEXT_LOOP_NO_TOOLS_V1,
    execution_surface_id=EXECUTION_SURFACE_PROMPT_REASONING_LOOP_V1,
    tool_surface_id=TOOL_SURFACE_NO_TOOLS_V1,
    memory_surface_id=MEMORY_SURFACE_ITEM_STATELESS_V1,
    legacy_aliases=("react_text", "baseline-react-text"),
    react_execution_mode=REACT_EXECUTION_MODE_REASONING_TEXT_LOOP_NO_TOOLS_V1,
    default_temperature=0.0,
)
