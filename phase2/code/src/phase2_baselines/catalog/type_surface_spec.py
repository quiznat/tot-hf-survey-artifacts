"""Atomic data type for one capability surface specification."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SurfaceSpec:
    """One atomic capability surface definition."""

    surface_id: str
    display_name: str
    description: str
