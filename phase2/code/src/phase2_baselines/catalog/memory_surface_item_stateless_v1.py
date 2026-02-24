"""Memory surface: item-stateless memory."""

from .type_surface_spec import SurfaceSpec

MEMORY_SURFACE_ITEM_STATELESS_V1 = "memory_surface.item_stateless.v1"
MEMORY_SURFACE_ITEM_STATELESS_V1_SPEC = SurfaceSpec(
    surface_id=MEMORY_SURFACE_ITEM_STATELESS_V1,
    display_name="Item-Stateless Memory",
    description="No persistent memory is carried across benchmark items.",
)
