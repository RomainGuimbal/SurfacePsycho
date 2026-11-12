from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPGridCoordinates(CustomGeometryGroup):
    _name = "SP - Grid Coordinates"
    _color_tag = "CONVERTER"
    _tree_properties = {"default_group_node_width": 160, "node_tool_idname": "geometry.sp_grid_coordinates", "show_modifier_manage_panel": False, "is_modifier": True}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.collapse = True

        u_count = tree.inputs.integer("U Count", 4, min_value=0)
        index = tree.inputs.integer("Index", 0, min_value=0, default_input="INDEX")
        index_u = tree.outputs.integer("Index U", description="Column of vertex (0,1,2,0,1,2...)")
        index_v = tree.outputs.integer("Index V", description="Row of vertex (0,0,0,1,1,1...)")

        index % u_count >> index_u
        index // u_count >> index_v


with TreeBuilder("SP - Evaluate Interpolated Patch [Single Direction]", clear=True) as tree:
    sample_grid = tree.inputs.geometry("Sample Grid")
    position = tree.inputs.vector("Position", (0.0, 0.0, 0.0), hide_value=True)
    value = tree.inputs.float("Value", 0.0, hide_value=True)
    interpolation_direction_count = tree.inputs.integer("Interpolation Direction Count", 0, structure_type="SINGLE", force_non_field=True)
    other_direction_count = tree.inputs.integer("Other Direction Count", 4, min_value=0, structure_type="SINGLE", force_non_field=True)
    value_1 = tree.outputs.vector("Value")

    sp_grid_coordinates = SPGridCoordinates(**{"U Count": interpolation_direction_count})
    integer_math = ((interpolation_direction_count * other_direction_count).props(hide=True) * interpolation_direction_count).props(width=100.0, hide=True)
    integer_math_1 = (interpolation_direction_count * interpolation_direction_count).props(width=100.0, hide=True)
    sp_grid_coordinates_1 = SPGridCoordinates(**{"U Count": integer_math_1})
    integer_math_2 = (sp_grid_coordinates.o.index_u + (interpolation_direction_count * sp_grid_coordinates_1.o.index_v).props(hide=True)).props(hide=True)
    points = g.Points(count=integer_math, radius=0.0).props(width=100.0, hide=True)
    sample_index = g.SampleIndex.point.vector(sample_grid, position, integer_math_2).props(label="Q", hide=True)
    vector_math = sample_index.o.value * g.SampleIndex.point.float(points, value, sp_grid_coordinates_1.o.index_u)
    accumulate_field = vector_math.point.total(sp_grid_coordinates.o.index_v).props(hide_outputs=["Leading", "Trailing"])
    sample_index_1 = g.SampleIndex.point.vector(points, accumulate_field, (interpolation_direction_count * g.Index()).props(hide=True)).props(hide=True)

    sample_index_1 >> value_1