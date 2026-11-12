from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPTrimParallelBezierPatch(CustomGeometryGroup):
    _name = "SP - Trim parallel Bezier Patch"
    _color_tag = "VECTOR"
    _tree_properties = {"node_tool_idname": "geometry.sp_trim_parallel_bezier_patch", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        cp = tree.inputs.vector("CP", (0.0, 0.0, 0.0))
        u_count = tree.inputs.integer("U Count", 0)
        v_count = tree.inputs.integer("V Count", 0)
        factor = tree.inputs.float("Factor", 0.5, min_value=0.0, max_value=1.0, subtype="FACTOR")
        cp_1 = tree.outputs.vector("CP")

        index = g.Index()
        integer_math = (index.o.index % u_count).props(hide=True)
        points = g.Points((u_count * v_count).props(hide=True)).props(hide=True)
        repeat_zone = g.RepeatZone((u_count - 1).props(hide=True))
        geometry = repeat_zone.items.geometry(points, "Geometry")
        point_count = repeat_zone.items.integer(name="Point Count")
        vector = repeat_zone.items.vector(cp, "Vector")
        integer_math_1 = (point_count.current + 1).props(width=100.0, hide=True)
        mix = g.Mix.vector(factor, vector.current, vector.current.point.at((index.o.index - 1).props(hide=True)), clamp_factor=False)
        switch = (integer_math < integer_math_1).props(hide=True).switch.vector(mix.o.result_vector, vector.current)
        capture = g.CaptureAttribute.point(geometry=geometry.current)
        value = capture.items.vector(switch, "Value")
        capture.o.geometry >> geometry.next
        integer_math_1 >> point_count.next
        value.output >> vector.next
        (
            geometry.result
            >> g.SampleIndex.point.vector(value=vector.result, index=g.Index())
            >> cp_1
        )
        viewer = g.Viewer()
        viewer.items.geometry(points, "Geometry")
        viewer.items.integer(integer_math, "Value")

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Capture Attribute": ("GeometryNodeCaptureAttribute", (531.07, 202.92), None, (("Geometry", "Repeat Input.001", "Geometry"), ("Value", "Switch", "Output"), )),
            "Compare": ("FunctionNodeCompare", (86.39, 102.22), None, (("A", "Integer Math.004", "Value"), ("B", "Integer Math.003", "Value"), )),
            "Evaluate at Index": ("GeometryNodeFieldAtIndex", (-126.12, -63.6), None, (("Index", "Integer Math.001", "Value"), ("Value", "Repeat Input.001", "Vector"), )),
            "Group Input": ("NodeGroupInput", (-889.51, 17.77), None, ()),
            "Group Output": ("NodeGroupOutput", (1131.38, 163.93), None, (("CP", "Sample Index", "Value"), )),
            "Index": ("GeometryNodeInputIndex", (727.06, 33.3), None, ()),
            "Index.001": ("GeometryNodeInputIndex", (-507.24, -113.94), None, ()),
            "Integer Math": ("FunctionNodeIntegerMath", (-502.46, 146.47), None, (("Value", "Group Input", "U Count"), ("Value#1", "Group Input", "V Count"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (-290.85, -158.89), None, (("Value", "Index.001", "Index"), )),
            "Integer Math.002": ("FunctionNodeIntegerMath", (-496.89, 184.82), None, (("Value", "Group Input", "U Count"), )),
            "Integer Math.003": ("FunctionNodeIntegerMath", (-76.29, 105.61), None, (("Value", "Repeat Input.001", "Point Count"), )),
            "Integer Math.004": ("FunctionNodeIntegerMath", (-318.5, -13.25), None, (("Value", "Index.001", "Index"), ("Value#1", "Group Input", "U Count"), )),
            "Mix": ("ShaderNodeMix", (87.44, 62.38), None, (("A#1", "Repeat Input.001", "Vector"), ("B#1", "Evaluate at Index", "Value"), ("Factor", "Group Input", "Factor"), )),
            "Points": ("GeometryNodePoints", (-505.17, 104.31), None, (("Count", "Integer Math", "Value"), )),
            "Repeat Input.001": ("GeometryNodeRepeatInput", (-328.76, 189.18), None, (("Geometry", "Points", "Points"), ("Iterations", "Integer Math.002", "Value"), ("Vector", "Group Input", "CP"), )),
            "Repeat Output.001": ("GeometryNodeRepeatOutput", (737.1, 194.71), None, (("Geometry", "Capture Attribute", "Geometry"), ("Point Count", "Integer Math.003", "Value"), ("Vector", "Capture Attribute", "Value"), )),
            "Sample Index": ("GeometryNodeSampleIndex", (920.59, 243.86), None, (("Geometry", "Repeat Output.001", "Geometry"), ("Index", "Index", "Index"), ("Value", "Repeat Output.001", "Vector"), )),
            "Switch": ("GeometryNodeSwitch", (281.65, 45.57), None, (("False", "Mix", "Result#1"), ("Switch", "Compare", "Result"), ("True", "Repeat Input.001", "Vector"), )),
            "Viewer": ("GeometryNodeViewer", (-156.37, 69.33), None, (("Geometry", "Points", "Points"), ("Value", "Integer Math.004", "Value"), )),
        }