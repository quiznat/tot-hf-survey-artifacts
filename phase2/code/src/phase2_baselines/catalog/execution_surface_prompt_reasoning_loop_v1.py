"""Execution surface: prompt reasoning loop."""

from .type_surface_spec import SurfaceSpec

EXECUTION_SURFACE_PROMPT_REASONING_LOOP_V1 = "execution_surface.prompt_reasoning_loop.v1"
EXECUTION_SURFACE_PROMPT_REASONING_LOOP_V1_SPEC = SurfaceSpec(
    surface_id=EXECUTION_SURFACE_PROMPT_REASONING_LOOP_V1,
    display_name="Prompt Reasoning Loop",
    description="Direct prompt-response loop with no external code execution runtime.",
)
