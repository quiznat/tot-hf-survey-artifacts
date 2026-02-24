"""Atomic condition spec: baseline tree-of-thoughts search reasoning-only."""

from .algorithm_tree_of_thoughts_search_reasoning_only_v1 import ALGORITHM_ID, ALGORITHM_MODULE_ID
from .condition_family_baseline_tree_of_thoughts_search_reasoning import (
    CONDITION_FAMILY_BASELINE_TREE_OF_THOUGHTS_SEARCH_REASONING,
)
from .condition_key_baseline_tree_of_thoughts_search_reasoning_only_v1 import (
    CONDITION_KEY_BASELINE_TREE_OF_THOUGHTS_SEARCH_REASONING_ONLY_V1,
)
from .execution_surface_prompt_reasoning_loop_v1 import EXECUTION_SURFACE_PROMPT_REASONING_LOOP_V1
from .memory_surface_item_stateless_v1 import MEMORY_SURFACE_ITEM_STATELESS_V1
from .runner_adapter_tree_of_thoughts_search_reasoning_v1 import (
    RUNNER_ADAPTER_TREE_OF_THOUGHTS_SEARCH_REASONING_V1,
)
from .tool_surface_no_tools_v1 import TOOL_SURFACE_NO_TOOLS_V1
from .tot_variant_tree_of_thoughts_search_baseline_v1 import TOT_VARIANT_TREE_OF_THOUGHTS_SEARCH_BASELINE_V1
from .type_condition_spec import ConditionSpec


CONDITION_SPEC_BASELINE_TREE_OF_THOUGHTS_SEARCH_REASONING_ONLY_V1 = ConditionSpec(
    condition_key=CONDITION_KEY_BASELINE_TREE_OF_THOUGHTS_SEARCH_REASONING_ONLY_V1,
    condition_id="tot-prototype",
    condition_display_name="Baseline Tree-of-Thoughts Search (Reasoning-Only)",
    condition_family_id=CONDITION_FAMILY_BASELINE_TREE_OF_THOUGHTS_SEARCH_REASONING,
    algorithm_id=ALGORITHM_ID,
    algorithm_module_id=ALGORITHM_MODULE_ID,
    runner_adapter_id=RUNNER_ADAPTER_TREE_OF_THOUGHTS_SEARCH_REASONING_V1,
    execution_surface_id=EXECUTION_SURFACE_PROMPT_REASONING_LOOP_V1,
    tool_surface_id=TOOL_SURFACE_NO_TOOLS_V1,
    memory_surface_id=MEMORY_SURFACE_ITEM_STATELESS_V1,
    legacy_aliases=("tot", "tot-prototype"),
    tot_variant=TOT_VARIANT_TREE_OF_THOUGHTS_SEARCH_BASELINE_V1,
    default_temperature=0.0,
)
