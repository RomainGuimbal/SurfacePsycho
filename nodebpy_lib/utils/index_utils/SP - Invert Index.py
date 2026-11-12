from bpy.types import GeometryNodeTree
from nodebpy import TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPInvertIndex(CustomGeometryGroup):
    _name = "SP - Invert Index"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_invert_index", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        enable = tree.inputs.boolean("Enable", False)
        point_count = tree.inputs.integer("Point Count", 0)
        index = tree.inputs.integer("Index", 0)
        index_1 = tree.outputs.integer("Index")

        enable.switch.integer(index, point_count - 1 - index) >> index_1

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-244.7, 79.34), None, ()),
            "Group Output": ("NodeGroupOutput", (501.75, 56.91), None, (("Index", "Switch.003", "Output"), )),
            "Integer Math": ("FunctionNodeIntegerMath", (-14.14, -26.31), None, (("Value", "Group Input", "Point Count"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (165.06, -30.0), None, (("Value", "Integer Math", "Value"), ("Value#1", "Group Input", "Index"), )),
            "Switch.003": ("GeometryNodeSwitch", (346.87, 95.48), None, (("False", "Group Input", "Index"), ("Switch", "Group Input", "Enable"), ("True", "Integer Math.001", "Value"), )),
        }