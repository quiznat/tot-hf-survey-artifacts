"""Tool surface: no tools."""

from .type_surface_spec import SurfaceSpec

TOOL_SURFACE_NO_TOOLS_V1 = "tool_surface.no_tools.v1"
TOOL_SURFACE_NO_TOOLS_V1_SPEC = SurfaceSpec(
    surface_id=TOOL_SURFACE_NO_TOOLS_V1,
    display_name="No Tools",
    description="Condition cannot call external tools.",
)
