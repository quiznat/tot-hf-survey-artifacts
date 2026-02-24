"""Atomic data type for one experiment condition specification."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConditionSpec:
    """One atomic, uniquely identified condition definition."""

    condition_key: str
    condition_id: str
    condition_display_name: str
    condition_family_id: str
    algorithm_id: str
    algorithm_module_id: str
    runner_adapter_id: str
    execution_surface_id: str
    tool_surface_id: str
    memory_surface_id: str
    legacy_aliases: tuple[str, ...] = ()
    react_execution_mode: str | None = None
    tot_variant: str | None = None
    default_temperature: float | None = None

    @property
    def key(self) -> str:
        """Backward-compatible accessor for existing call sites."""
        return self.condition_key

    @property
    def runner_name(self) -> str:
        """Backward-compatible accessor for existing call sites."""
        return self.runner_adapter_id
