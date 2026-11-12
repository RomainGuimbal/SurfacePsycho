from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPAutoMult(CustomGeometryGroup):
    _name = "SP - Auto Mult"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.sp_auto_mult", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        count = tree.inputs.integer("Count", 0, structure_type="SINGLE", force_non_field=True)
        degree = tree.inputs.integer("Degree", 0, structure_type="SINGLE", force_non_field=True)
        clamped = tree.inputs.boolean("Clamped", False, structure_type="SINGLE", force_non_field=True)
        cyclic = tree.inputs.boolean("Cyclic", False, structure_type="SINGLE", force_non_field=True)
        mult = tree.outputs.integer("Mult")
        length = tree.outputs.integer("Length")

        integer_math = (count - degree).props(hide=True)
        with g.Frame("clamped non-periodic"):
            index = g.Index()
            boolean_math = (g.Compare.integer.equal(index, 0).props(label="=0", hide=True).o.result | g.Compare.integer.equal(index, integer_math).props(label="=last knot id", hide=True)).props(width=100.0, hide=True)
            switch = boolean_math.switch.integer(1, (degree + 1).props(label="degree +1", hide=True))
        with g.Frame("clamped periodic"):
            index_1 = g.Index()
            boolean_math_1 = (g.Compare.integer.equal(index_1, 1).props(label="=1", hide=True).o.result | g.Compare.integer.equal(index_1, integer_math + 1).props(label="=last knot -1")).props(width=100.0, hide=True)
            switch_1 = boolean_math_1.switch.integer(1, degree)
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
            integer_math_1 = g.IntegerMath(value=g.Reroute(input=clamped).props(width=19.0), value_001=g.IntegerMath(value=reroute_7, value_001=reroute_7).props(hide=True)).props(hide=True)
        index_switch = g.IndexSwitch.integer(integer_math_1, (count + degree + 1, integer_math + 1, count + 1, integer_math + 3))
        index_switch_1 = g.IndexSwitch.integer(integer_math_1, (1, switch, 1, switch_1))
        with g.Frame():
            switch_2 = (g.Index() >= index_switch).props(hide=True).switch.integer(index_switch_1).props(label="clear tail")
        viewer = g.Viewer()
        viewer.items.geometry(g.MeshLine(40), "Mesh")
        viewer.items.integer(switch_2, "Output")

        switch_2 >> mult
        index_switch >> length

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math.003": ("FunctionNodeBooleanMath", (360.99, -104.08), "Frame", (("Boolean", "Compare.004", "Result"), ("Boolean#1", "Compare.008", "Result"), )),
            "Boolean Math.004": ("FunctionNodeBooleanMath", (388.96, -104.1), "Frame.004", (("Boolean", "Compare.005", "Result"), ("Boolean#1", "Compare.009", "Result"), )),
            "Compare.002": ("FunctionNodeCompare", (30.09, -96.72), "Frame.006", (("A", "Index.001", "Index"), ("B", "Index Switch.001", "Output"), )),
            "Compare.004": ("FunctionNodeCompare", (201.5, -82.86), "Frame", (("A", "Index.004", "Index"), )),
            "Compare.005": ("FunctionNodeCompare", (208.76, -57.55), "Frame.004", (("A", "Index.006", "Index"), )),
            "Compare.008": ("FunctionNodeCompare", (201.7, -125.34), "Frame", (("A", "Index.004", "Index"), ("B", "Integer Math.008", "Value"), )),
            "Compare.009": ("FunctionNodeCompare", (208.96, -100.03), "Frame.004", (("A", "Index.006", "Index"), ("B", "Integer Math.001", "Value"), )),
            "Frame": ("NodeFrame", (-320.82, -416.08), None, ()),
            "Frame.002": ("NodeFrame", (30.18, -137.43), "Frame.005", ()),
            "Frame.003": ("NodeFrame", (175.49, -30.18), "Frame.005", ()),
            "Frame.004": ("NodeFrame", (-419.29, -734.79), None, ()),
            "Frame.005": ("NodeFrame", (59.53, -36.04), "Frame.013", ()),
            "Frame.006": ("NodeFrame", (904.76, 147.71), None, ()),
            "Frame.013": ("NodeFrame", (132.77, 656.78), None, ()),
            "Group Input": ("NodeGroupInput", (-887.66, 83.37), None, ()),
            "Group Output": ("NodeGroupOutput", (1484.74, 79.24), None, (("Length", "Index Switch.001", "Output"), ("Mult", "Switch.002", "Output"), )),
            "Index Switch": ("GeometryNodeIndexSwitch", (604.03, 91.24), None, (("1", "Switch.008", "Output"), ("3", "Switch.009", "Output"), ("Index", "Integer Math.004", "Value"), )),
            "Index Switch.001": ("GeometryNodeIndexSwitch", (603.72, -160.67), None, (("0", "Integer Math.011", "Value"), ("1", "Integer Math.005", "Value"), ("2", "Integer Math.012", "Value"), ("3", "Integer Math.002", "Value"), ("Index", "Integer Math.004", "Value"), )),
            "Index.001": ("GeometryNodeInputIndex", (30.02, -29.99), "Frame.006", ()),
            "Index.004": ("GeometryNodeInputIndex", (30.22, -78.41), "Frame", ()),
            "Index.006": ("GeometryNodeInputIndex", (37.47, -53.1), "Frame.004", ()),
            "Integer Math": ("FunctionNodeIntegerMath", (127.06, 90.52), None, (("Value", "Group Input", "Count"), ("Value#1", "Group Input", "Degree"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (29.95, -122.02), "Frame.004", (("Value", "Integer Math.008", "Value"), )),
            "Integer Math.002": ("FunctionNodeIntegerMath", (52.67, -267.84), None, (("Value", "Integer Math.008", "Value"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (54.21, -312.25), "Frame.013", (("Value", "Reroute.026", "Output"), ("Value#1", "Reroute.026", "Output"), )),
            "Integer Math.004": ("FunctionNodeIntegerMath", (210.23, -297.32), "Frame.013", (("Value", "Reroute.047", "Output"), ("Value#1", "Integer Math.003", "Value"), )),
            "Integer Math.005": ("FunctionNodeIntegerMath", (54.44, -132.53), None, (("Value", "Integer Math.008", "Value"), )),
            "Integer Math.008": ("FunctionNodeIntegerMath", (-428.06, -180.26), None, (("Value", "Group Input", "Count"), ("Value#1", "Group Input", "Degree"), )),
            "Integer Math.009": ("FunctionNodeIntegerMath", (194.6, -185.82), "Frame", (("Value", "Group Input", "Degree"), )),
            "Integer Math.011": ("FunctionNodeIntegerMath", (304.71, 73.95), None, (("Value", "Integer Math", "Value"), )),
            "Integer Math.012": ("FunctionNodeIntegerMath", (307.31, -63.95), None, (("Value", "Group Input", "Count"), )),
            "Mesh Line": ("GeometryNodeMeshLine", (1000.67, -203.74), None, ()),
            "Reroute.005": ("NodeReroute", (35.21, -35.72), "Frame.002", ()),
            "Reroute.006": ("NodeReroute", (39.48, -35.21), "Frame.003", ()),
            "Reroute.013": ("NodeReroute", (180.0, -35.21), "Frame.002", ()),
            "Reroute.021": ("NodeReroute", (112.74, -35.72), "Frame.002", ()),
            "Reroute.025": ("NodeReroute", (35.21, -142.46), "Frame.003", ()),
            "Reroute.026": ("NodeReroute", (35.21, -338.17), "Frame.013", (("Input", "Group Input", "Cyclic"), )),
            "Reroute.030": ("NodeReroute", (148.55, -108.48), "Frame.005", ()),
            "Reroute.033": ("NodeReroute", (39.98, -76.42), "Frame.003", ()),
            "Reroute.047": ("NodeReroute", (51.9, -297.62), "Frame.013", (("Input", "Group Input", "Clamped"), )),
            "Switch.002": ("GeometryNodeSwitch", (218.43, -46.29), "Frame.006", (("False", "Index Switch", "Output"), ("Switch", "Compare.002", "Result"), )),
            "Switch.008": ("GeometryNodeSwitch", (489.23, -36.23), "Frame", (("Switch", "Boolean Math.003", "Boolean"), ("True", "Integer Math.009", "Value"), )),
            "Switch.009": ("GeometryNodeSwitch", (517.2, -36.25), "Frame.004", (("Switch", "Boolean Math.004", "Boolean"), ("True", "Group Input", "Degree"), )),
            "Viewer": ("GeometryNodeViewer", (1361.05, -159.61), None, (("Mesh", "Mesh Line", "Mesh"), ("Output", "Switch.002", "Output"), )),
        }