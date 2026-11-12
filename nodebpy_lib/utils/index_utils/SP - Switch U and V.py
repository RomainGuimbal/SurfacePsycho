from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPSwitchUAndV(CustomGeometryGroup):
    _name = "SP - Switch U and V"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_switch_u_and_v", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        enable = tree.inputs.boolean("Enable", True)
        u_count = tree.inputs.integer("U Count", -1)
        v_count = tree.inputs.integer("V Count", -1)
        index = tree.inputs.integer("Index", -1, default_input="INDEX")
        index_1 = tree.outputs.integer("Index")
        u_count_1 = tree.outputs.integer("U Count")
        v_count_1 = tree.outputs.integer("V Count")

        reroute = g.Reroute(input=v_count).props(width=19.0)
        reroute_1 = g.Reroute(input=u_count).props(width=19.0)
        (
            enable.switch.integer(index, (index % reroute_1).props(label="U") * reroute + index // reroute_1)
            >> index_1
        )
        enable.switch.integer(reroute, reroute_1) >> v_count_1
        enable.switch.integer(reroute_1, reroute) >> u_count_1

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-609.38, -61.58), None, ()),
            "Group Output": ("NodeGroupOutput", (708.7, -12.01), None, (("Index", "Switch", "Output"), ("U Count", "Switch.002", "Output"), ("V Count", "Switch.001", "Output"), )),
            "Integer Math": ("FunctionNodeIntegerMath", (-138.6, 227.97), None, (("Value", "Group Input", "Index"), ("Value#1", "Reroute.004", "Output"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (55.14, 204.69), None, (("Value", "Integer Math", "Value"), ("Value#1", "Reroute.003", "Output"), )),
            "Integer Math.002": ("FunctionNodeIntegerMath", (240.93, 166.33), None, (("Value", "Integer Math.001", "Value"), ("Value#1", "Integer Math.005", "Value"), )),
            "Integer Math.005": ("FunctionNodeIntegerMath", (55.66, 51.98), None, (("Value", "Group Input", "Index"), ("Value#1", "Reroute.004", "Output"), )),
            "Reroute.003": ("NodeReroute", (-282.18, -182.71), None, (("Input", "Group Input", "V Count"), )),
            "Reroute.004": ("NodeReroute", (-280.51, -163.67), None, (("Input", "Group Input", "U Count"), )),
            "Switch": ("GeometryNodeSwitch", (468.42, 102.07), None, (("False", "Group Input", "Index"), ("Switch", "Group Input", "Enable"), ("True", "Integer Math.002", "Value"), )),
            "Switch.001": ("GeometryNodeSwitch", (454.86, -215.03), None, (("False", "Reroute.003", "Output"), ("Switch", "Group Input", "Enable"), ("True", "Reroute.004", "Output"), )),
            "Switch.002": ("GeometryNodeSwitch", (461.09, -51.23), None, (("False", "Reroute.004", "Output"), ("Switch", "Group Input", "Enable"), ("True", "Reroute.003", "Output"), )),
        }