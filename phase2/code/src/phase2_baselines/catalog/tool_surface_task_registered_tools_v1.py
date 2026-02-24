"""Tool surface: task-registered tools."""

from .type_surface_spec import SurfaceSpec

TOOL_SURFACE_TASK_REGISTERED_TOOLS_V1 = "tool_surface.task_registered_tools.v1"
TOOL_SURFACE_TASK_REGISTERED_TOOLS_V1_SPEC = SurfaceSpec(
    surface_id=TOOL_SURFACE_TASK_REGISTERED_TOOLS_V1,
    display_name="Task-Registered Tools",
    description="Condition can call tools explicitly registered by the benchmark task.",
)
