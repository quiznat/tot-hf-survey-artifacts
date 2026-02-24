"""Execution surface: smolagents code-agent with task tools."""

from .type_surface_spec import SurfaceSpec

EXECUTION_SURFACE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1 = (
    "execution_surface.smolagents_code_agent_with_task_tools.v1"
)
EXECUTION_SURFACE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1_SPEC = SurfaceSpec(
    surface_id=EXECUTION_SURFACE_SMOLAGENTS_CODE_AGENT_WITH_TASK_TOOLS_V1,
    display_name="smolagents CodeAgent Runtime",
    description="smolagents CodeAgent runtime with task-registered tool execution.",
)
