"""Tests for atomic condition catalog identities and surfaces."""

from __future__ import annotations

import unittest

from phase2_baselines.catalog import (
    MATRIX_A_REASONING_ONLY_CANONICAL_KEYS,
    condition_names,
    get_condition_spec,
    resolve_conditions,
)


class ConditionCatalogTests(unittest.TestCase):
    def test_catalog_contains_expected_matrix_a_conditions(self) -> None:
        names = set(condition_names())
        required = set(MATRIX_A_REASONING_ONLY_CANONICAL_KEYS)
        self.assertTrue(required.issubset(names))

    def test_matrix_a_surfaces_are_reasoning_only(self) -> None:
        specs = resolve_conditions(list(MATRIX_A_REASONING_ONLY_CANONICAL_KEYS))
        for spec in specs:
            self.assertEqual(spec.execution_surface_id, "execution_surface.prompt_reasoning_loop.v1")
            self.assertEqual(spec.tool_surface_id, "tool_surface.no_tools.v1")
            self.assertEqual(spec.memory_surface_id, "memory_surface.item_stateless.v1")

    def test_atomic_ids_are_non_empty(self) -> None:
        for name in condition_names():
            spec = get_condition_spec(name)
            self.assertTrue(spec.algorithm_id)
            self.assertTrue(spec.algorithm_module_id)
            self.assertTrue(spec.condition_id)

    def test_legacy_aliases_resolve_to_canonical_condition_keys(self) -> None:
        alias_expected = {
            "single": "baseline_single_path_reasoning_only_v1",
            "cot": "baseline_chain_of_thought_reasoning_only_v1",
            "cot_sc": "baseline_chain_of_thought_self_consistency_reasoning_only_v1",
            "react_text": "baseline_react_reasoning_text_loop_only_v1",
            "tot": "baseline_tree_of_thoughts_search_reasoning_only_v1",
        }
        for alias, expected_canonical in alias_expected.items():
            self.assertEqual(get_condition_spec(alias).condition_key, expected_canonical)


if __name__ == "__main__":
    unittest.main()
