from bpy.types import GeometryNodeTree
from nodebpy import TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPFlipGridIndex(CustomGeometryGroup):
    _name = "SP - Flip Grid index"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_flip_grid_index", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        enable = tree.inputs.boolean("Enable", True)
        u_count = tree.inputs.integer("U Count", 0, min_value=0)
        index = tree.inputs.integer("Index", 0, min_value=0, default_input="INDEX")
        flipped_index = tree.outputs.integer("Flipped index")

        (
            enable.switch.integer(index, (0 - (index % u_count - (u_count - 1)) + index // u_count * u_count).props(hide=True))
            >> flipped_index
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-802.82, 64.74), None, ()),
            "Group Output": ("NodeGroupOutput", (543.59, 94.61), None, (("Flipped index", "Switch", "Output"), )),
            "Integer Math": ("FunctionNodeIntegerMath", (-418.08, 233.25), None, (("Value", "Group Input", "U Count"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (-413.89, 368.9), None, (("Value", "Group Input", "Index"), ("Value#1", "Group Input", "U Count"), )),
            "Integer Math.002": ("FunctionNodeIntegerMath", (-234.55, 339.88), None, (("Value", "Integer Math.001", "Value"), ("Value#1", "Integer Math", "Value"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (-345.88, 41.45), None, (("Value", "Group Input", "Index"), ("Value#1", "Group Input", "U Count"), )),
            "Integer Math.004": ("FunctionNodeIntegerMath", (-184.54, -17.77), None, (("Value", "Integer Math.003", "Value"), ("Value#1", "Group Input", "U Count"), )),
            "Integer Math.005": ("FunctionNodeIntegerMath", (111.26, 124.99), None, (("Value", "Integer Math.006", "Value"), ("Value#1", "Integer Math.004", "Value"), )),
            "Integer Math.006": ("FunctionNodeIntegerMath", (-68.48, 326.25), None, (("Value#1", "Integer Math.002", "Value"), )),
            "Switch": ("GeometryNodeSwitch", (350.43, 133.53), None, (("False", "Group Input", "Index"), ("Switch", "Group Input", "Enable"), ("True", "Integer Math.005", "Value"), )),
        }