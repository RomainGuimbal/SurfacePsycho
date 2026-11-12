from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPVirtualCPCount(CustomGeometryGroup):
    _name = "SP - Virtual CP Count"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_virtual_cp_count", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        cp_count = tree.inputs.integer("CP Count", 0, structure_type="SINGLE", force_non_field=True)
        degree = tree.inputs.integer("Degree", 0, structure_type="SINGLE", force_non_field=True)
        clamped = tree.inputs.boolean("Clamped", False, structure_type="SINGLE", force_non_field=True)
        cyclic = tree.inputs.boolean("Cyclic", False, structure_type="SINGLE", force_non_field=True)
        virtual_cp_count = tree.outputs.integer("Virtual CP Count")

        with g.Frame("Knot mode"):
            with g.Frame():
                with g.Frame():
                    _reroute = g.Reroute().props(label="Cyclic", width=19.0)
                    _reroute_1 = g.Reroute().props(label="3", width=19.0)
                    _reroute_2 = g.Reroute().props(label="2", width=19.0)
                with g.Frame():
                    _reroute_3 = g.Reroute().props(label="Clamped", width=19.0)
                    _reroute_4 = g.Reroute().props(label="3", width=19.0)
                    _reroute_5 = g.Reroute().props(label="1", width=19.0)
                _reroute_6 = g.Reroute().props(label="0", width=19.0)
            reroute_7 = g.Reroute(input=cyclic).props(width=19.0)
            integer_math = g.IntegerMath(value=g.Reroute(input=clamped).props(width=19.0), value_001=g.IntegerMath(value=reroute_7, value_001=reroute_7).props(width=100.0, hide=True)).props(hide=True)
        with g.Frame("Virtual CP Count"):
            reroute_8 = g.Reroute(input=cp_count).props(width=19.0)
            index_switch = g.IndexSwitch.integer(integer_math, (reroute_8, reroute_8, (reroute_8.o.output + degree).props(label="+p", width=100.0, hide=True), (reroute_8.o.output + 1).props(width=100.0, hide=True)))
            (
                g.Reroute(input=index_switch.o.output).props(label="virtual count", width=19.0)
                >> virtual_cp_count
            )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Frame.005": ("NodeFrame", (-24.67, -103.2), None, ()),
            "Frame.006": ("NodeFrame", (30.18, -137.43), "Frame.008", ()),
            "Frame.007": ("NodeFrame", (175.49, -30.18), "Frame.008", ()),
            "Frame.008": ("NodeFrame", (35.11, -36.04), "Frame.013", ()),
            "Frame.013": ("NodeFrame", (-284.92, 278.88), None, ()),
            "Group Input": ("NodeGroupInput", (-492.61, -5.22), None, ()),
            "Group Output": ("NodeGroupOutput", (457.9, -131.1), None, (("Virtual CP Count", "Reroute.022", "Output"), )),
            "Index Switch": ("GeometryNodeIndexSwitch", (189.71, -35.79), "Frame.005", (("0", "Reroute.001", "Output"), ("1", "Reroute.001", "Output"), ("2", "Integer Math.003", "Value"), ("3", "Integer Math.004", "Value"), ("Index", "Integer Math.007", "Value"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (54.03, -176.4), "Frame.005", (("Value", "Reroute.001", "Output"), ("Value#1", "Group Input", "Degree"), )),
            "Integer Math.004": ("FunctionNodeIntegerMath", (52.68, -211.78), "Frame.005", (("Value", "Reroute.001", "Output"), )),
            "Integer Math.005": ("FunctionNodeIntegerMath", (54.09, -314.76), "Frame.013", (("Value", "Reroute.038", "Output"), ("Value#1", "Reroute.038", "Output"), )),
            "Integer Math.007": ("FunctionNodeIntegerMath", (185.81, -297.32), "Frame.013", (("Value", "Reroute.047", "Output"), ("Value#1", "Integer Math.005", "Value"), )),
            "Reroute.001": ("NodeReroute", (35.21, -147.42), "Frame.005", (("Input", "Group Input", "CP Count"), )),
            "Reroute.022": ("NodeReroute", (385.69, -69.36), "Frame.005", (("Input", "Index Switch", "Output"), )),
            "Reroute.028": ("NodeReroute", (35.21, -35.72), "Frame.006", ()),
            "Reroute.029": ("NodeReroute", (39.48, -35.21), "Frame.007", ()),
            "Reroute.033": ("NodeReroute", (180.0, -35.21), "Frame.006", ()),
            "Reroute.034": ("NodeReroute", (112.74, -35.72), "Frame.006", ()),
            "Reroute.035": ("NodeReroute", (35.21, -142.46), "Frame.007", ()),
            "Reroute.036": ("NodeReroute", (148.55, -108.48), "Frame.008", ()),
            "Reroute.037": ("NodeReroute", (39.98, -76.42), "Frame.007", ()),
            "Reroute.038": ("NodeReroute", (37.04, -322.61), "Frame.013", (("Input", "Group Input", "Cyclic"), )),
            "Reroute.047": ("NodeReroute", (35.21, -301.96), "Frame.013", (("Input", "Group Input", "Clamped"), )),
        }