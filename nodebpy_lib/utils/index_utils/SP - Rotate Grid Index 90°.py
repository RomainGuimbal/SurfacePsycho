from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPRotateGridIndex90(CustomGeometryGroup):
    _name = "SP - Rotate Grid Index 90°"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_rotate_grid_index_90_", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        index = tree.inputs.integer("Index", -1, default_input="INDEX")
        u_count = tree.inputs.integer("U Count", -1)
        v_count = tree.inputs.integer("V Count", -1)
        index_1 = tree.outputs.integer("Index")

        reroute = g.Reroute(input=u_count).props(width=19.0)
        integer_math = (((u_count * v_count).props(hide=True) - (index + 1).props(hide=True)) % reroute).props(label="U")
        (
            integer_math * g.Reroute(input=v_count).props(width=19.0) + index // reroute
            >> index_1
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-961.62, -65.06), None, ()),
            "Group Output": ("NodeGroupOutput", (346.57, -46.69), None, (("Index", "Integer Math.006", "Value"), )),
            "Integer Math": ("FunctionNodeIntegerMath", (-321.63, 15.89), None, (("Value", "Integer Math.003", "Value"), ("Value#1", "Reroute", "Output"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (-102.79, -155.61), None, (("Value", "Group Input", "Index"), ("Value#1", "Reroute", "Output"), )),
            "Integer Math.002": ("FunctionNodeIntegerMath", (-676.36, -36.96), None, (("Value", "Group Input", "U Count"), ("Value#1", "Group Input", "V Count"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (-502.35, 9.04), None, (("Value", "Integer Math.002", "Value"), ("Value#1", "Integer Math.005", "Value"), )),
            "Integer Math.004": ("FunctionNodeIntegerMath", (-95.73, 10.04), None, (("Value", "Integer Math", "Value"), ("Value#1", "Reroute.002", "Output"), )),
            "Integer Math.005": ("FunctionNodeIntegerMath", (-684.06, -73.79), None, (("Value", "Group Input", "Index"), )),
            "Integer Math.006": ("FunctionNodeIntegerMath", (147.75, -47.42), None, (("Value", "Integer Math.004", "Value"), ("Value#1", "Integer Math.001", "Value"), )),
            "Reroute": ("NodeReroute", (-367.68, -147.4), None, (("Input", "Group Input", "U Count"), )),
            "Reroute.002": ("NodeReroute", (-363.87, -169.47), None, (("Input", "Group Input", "V Count"), )),
        }