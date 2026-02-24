"""Registry composer for atomic condition modules."""

from __future__ import annotations

from typing import Dict, Iterable, List

from .condition_baseline_chain_of_thought_reasoning_only_v1 import (
    CONDITION_SPEC_BASELINE_CHAIN_OF_THOUGHT_REASONING_ONLY_V1,
)
from .condition_baseline_chain_of_thought_self_consistency_reasoning_only_v1 import (
    CONDITION_SPEC_BASELINE_CHAIN_OF_THOUGHT_SELF_CONSISTENCY_REASONING_ONLY_V1,
)
from .condition_baseline_react_code_agent_with_task_tools_v1 import (
    CONDITION_SPEC_BASELINE_REACT_CODE_AGENT_WITH_TASK_TOOLS_V1,
)
from .condition_baseline_react_reasoning_text_loop_only_v1 import (
    CONDITION_SPEC_BASELINE_REACT_REASONING_TEXT_LOOP_ONLY_V1,
)
from .condition_baseline_single_path_reasoning_only_v1 import (
    CONDITION_SPEC_BASELINE_SINGLE_PATH_REASONING_ONLY_V1,
)
from .condition_baseline_tree_of_thoughts_generalized_recursive_reasoning_only_v1 import (
    CONDITION_SPEC_BASELINE_TREE_OF_THOUGHTS_GENERALIZED_RECURSIVE_REASONING_ONLY_V1,
)
from .condition_baseline_tree_of_thoughts_search_reasoning_only_v1 import (
    CONDITION_SPEC_BASELINE_TREE_OF_THOUGHTS_SEARCH_REASONING_ONLY_V1,
)
from .type_condition_spec import ConditionSpec


_CONDITION_SPEC_BY_KEY: Dict[str, ConditionSpec] = {
    CONDITION_SPEC_BASELINE_SINGLE_PATH_REASONING_ONLY_V1.condition_key: CONDITION_SPEC_BASELINE_SINGLE_PATH_REASONING_ONLY_V1,
    CONDITION_SPEC_BASELINE_CHAIN_OF_THOUGHT_REASONING_ONLY_V1.condition_key: CONDITION_SPEC_BASELINE_CHAIN_OF_THOUGHT_REASONING_ONLY_V1,
    CONDITION_SPEC_BASELINE_CHAIN_OF_THOUGHT_SELF_CONSISTENCY_REASONING_ONLY_V1.condition_key: CONDITION_SPEC_BASELINE_CHAIN_OF_THOUGHT_SELF_CONSISTENCY_REASONING_ONLY_V1,
    CONDITION_SPEC_BASELINE_REACT_CODE_AGENT_WITH_TASK_TOOLS_V1.condition_key: CONDITION_SPEC_BASELINE_REACT_CODE_AGENT_WITH_TASK_TOOLS_V1,
    CONDITION_SPEC_BASELINE_REACT_REASONING_TEXT_LOOP_ONLY_V1.condition_key: CONDITION_SPEC_BASELINE_REACT_REASONING_TEXT_LOOP_ONLY_V1,
    CONDITION_SPEC_BASELINE_TREE_OF_THOUGHTS_SEARCH_REASONING_ONLY_V1.condition_key: CONDITION_SPEC_BASELINE_TREE_OF_THOUGHTS_SEARCH_REASONING_ONLY_V1,
    CONDITION_SPEC_BASELINE_TREE_OF_THOUGHTS_GENERALIZED_RECURSIVE_REASONING_ONLY_V1.condition_key: CONDITION_SPEC_BASELINE_TREE_OF_THOUGHTS_GENERALIZED_RECURSIVE_REASONING_ONLY_V1,
}


_CONDITION_KEY_ALIAS_TO_CANONICAL_KEY: Dict[str, str] = {}
for _condition_key, _condition_spec in _CONDITION_SPEC_BY_KEY.items():
    _CONDITION_KEY_ALIAS_TO_CANONICAL_KEY[_condition_key] = _condition_key
    for _legacy_alias in _condition_spec.legacy_aliases:
        _CONDITION_KEY_ALIAS_TO_CANONICAL_KEY[_legacy_alias] = _condition_key


def canonical_condition_names() -> List[str]:
    """Return sorted canonical condition keys."""
    return sorted(_CONDITION_SPEC_BY_KEY.keys())


def condition_names(include_aliases: bool = True) -> List[str]:
    """Return sorted condition keys. Include aliases by default."""
    if include_aliases:
        return sorted(_CONDITION_KEY_ALIAS_TO_CANONICAL_KEY.keys())
    return canonical_condition_names()


def normalize_condition_key(condition_key: str) -> str:
    """Normalize alias to canonical condition key."""
    key = str(condition_key or "").strip()
    if key not in _CONDITION_KEY_ALIAS_TO_CANONICAL_KEY:
        raise KeyError(f"Unknown condition key: {condition_key}")
    return _CONDITION_KEY_ALIAS_TO_CANONICAL_KEY[key]


def get_condition_spec(condition_key: str) -> ConditionSpec:
    """Resolve one key/alias to exactly one atomic condition spec."""
    canonical_key = normalize_condition_key(condition_key)
    return _CONDITION_SPEC_BY_KEY[canonical_key]


def resolve_conditions(condition_keys: Iterable[str]) -> List[ConditionSpec]:
    """Resolve multiple keys/aliases to atomic condition specs."""
    resolved: List[ConditionSpec] = []
    for key in condition_keys:
        resolved.append(get_condition_spec(key))
    return resolved
