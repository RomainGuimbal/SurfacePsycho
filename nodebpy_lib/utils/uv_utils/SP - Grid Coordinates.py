from bpy.types import GeometryNodeTree
from nodebpy import TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPGridCoordinates(CustomGeometryGroup):
    _name = "SP - Grid Coordinates"
    _color_tag = "CONVERTER"
    _tree_properties = {"default_group_node_width": 160, "node_tool_idname": "geometry.sp_grid_coordinates", "show_modifier_manage_panel": False, "is_modifier": True}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        tree.collapse = True

        u_count = tree.inputs.integer("U Count", 4, min_value=0)
        index = tree.inputs.integer("Index", 0, min_value=0, default_input="INDEX")
        index_u = tree.outputs.integer("Index U", description="Column of vertex (0,1,2,0,1,2...)")
        index_v = tree.outputs.integer("Index V", description="Row of vertex (0,0,0,1,1,1...)")

        index % u_count >> index_u
        index // u_count >> index_v

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-605.63, 56.92), None, ()),
            "Group Output": ("NodeGroupOutput", (-251.38, 49.86), None, (("Index U", "Integer Math", "Value"), ("Index V", "Integer Math.001", "Value"), )),
            "Integer Math": ("FunctionNodeIntegerMath", (-424.27, 34.98), None, (("Value", "Group Input", "Index"), ("Value#1", "Group Input", "U Count"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (-424.27, -4.04), None, (("Value", "Group Input", "Index"), ("Value#1", "Group Input", "U Count"), )),
        }