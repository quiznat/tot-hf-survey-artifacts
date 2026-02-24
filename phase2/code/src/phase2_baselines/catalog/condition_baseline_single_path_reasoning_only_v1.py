"""Atomic condition spec: baseline single-path reasoning-only."""

from .algorithm_baseline_single_path_direct_answer_v1 import ALGORITHM_ID, ALGORITHM_MODULE_ID
from .condition_family_baseline_single_path_reasoning import CONDITION_FAMILY_BASELINE_SINGLE_PATH_REASONING
from .condition_key_baseline_single_path_reasoning_only_v1 import CONDITION_KEY_BASELINE_SINGLE_PATH_REASONING_ONLY_V1
from .execution_surface_prompt_reasoning_loop_v1 import EXECUTION_SURFACE_PROMPT_REASONING_LOOP_V1
from .memory_surface_item_stateless_v1 import MEMORY_SURFACE_ITEM_STATELESS_V1
from .runner_adapter_single_path_reasoning_v1 import RUNNER_ADAPTER_SINGLE_PATH_REASONING_V1
from .tool_surface_no_tools_v1 import TOOL_SURFACE_NO_TOOLS_V1
from .type_condition_spec import ConditionSpec


CONDITION_SPEC_BASELINE_SINGLE_PATH_REASONING_ONLY_V1 = ConditionSpec(
    condition_key=CONDITION_KEY_BASELINE_SINGLE_PATH_REASONING_ONLY_V1,
    condition_id="baseline-single-path",
    condition_display_name="Baseline Single-Path (Reasoning-Only)",
    condition_family_id=CONDITION_FAMILY_BASELINE_SINGLE_PATH_REASONING,
    algorithm_id=ALGORITHM_ID,
    algorithm_module_id=ALGORITHM_MODULE_ID,
    runner_adapter_id=RUNNER_ADAPTER_SINGLE_PATH_REASONING_V1,
    execution_surface_id=EXECUTION_SURFACE_PROMPT_REASONING_LOOP_V1,
    tool_surface_id=TOOL_SURFACE_NO_TOOLS_V1,
    memory_surface_id=MEMORY_SURFACE_ITEM_STATELESS_V1,
    legacy_aliases=("single", "baseline-single-path"),
    default_temperature=0.0,
)
