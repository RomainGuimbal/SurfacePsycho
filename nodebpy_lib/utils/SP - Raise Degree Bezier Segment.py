from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPRaiseDegreeBezierSegment(CustomGeometryGroup):
    _name = "SP - Raise Degree Bezier Segment"
    _color_tag = "GEOMETRY"
    _tree_properties = {"default_group_node_width": 290, "node_tool_idname": "geometry.sp_raise_degree_bezier_segment", "show_modifier_manage_panel": False, "is_mode_edit": True, "is_type_mesh": True}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        geometry = tree.inputs.geometry("Geometry")
        iterations = tree.inputs.integer("Iterations", 1, min_value=0, max_value=6, structure_type="SINGLE", force_non_field=True)
        geometry_1 = tree.outputs.geometry("Geometry")

        domain_size = g.DomainSize(geometry).props(hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
        index = g.Index()
        mesh_to_curve = g.MeshToCurve(geometry)
        reroute = g.Reroute(input=index.o.index).props(width=19.0)
        resample_curve = g.ResampleCurve(curve=mesh_to_curve, count=domain_size.o.point_count + iterations, keep_last_segment=False)
        repeat_zone = g.RepeatZone(iterations)
        geometry_2 = repeat_zone.items.geometry(resample_curve, "Geometry")
        value = repeat_zone.items.vector(g.SampleIndex.point.vector(mesh_to_curve, g.Position(), index).props(width=153.51), "Value")
        math_1 = (reroute.o.output / (repeat_zone.iteration + domain_size.o.point_count).props(hide=True)).props(hide=True)
        mix = g.Mix.vector(math_1, value.current.point.at(reroute).props(hide=True), value.current.point.at((reroute.o.output - 1).props(hide=True)).props(hide=True), clamp_factor=False)
        capture = g.CaptureAttribute.point(geometry=geometry_2.current)
        value_1 = capture.items.vector(mix.o.result_vector, "Value")
        capture.o.geometry >> geometry_2.next
        value_1.output >> value.next
        (
            g.Compare.integer.equal(iterations, 0).o.result.switch.geometry(geometry_2.result >> g.SetPosition(position=value.result) >> g.CurveToMesh(), geometry)
            >> geometry_1
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Capture Attribute": ("GeometryNodeCaptureAttribute", (446.03, -15.13), None, (("Geometry", "Repeat Input", "Geometry"), ("Value", "Mix", "Result#1"), )),
            "Compare": ("FunctionNodeCompare", (1011.37, 161.55), None, (("A", "Group Input", "Iterations"), )),
            "Curve to Mesh": ("GeometryNodeCurveToMesh", (1031.76, -65.06), None, (("Curve", "Set Position", "Geometry"), )),
            "Domain Size.001": ("GeometryNodeAttributeDomainSize", (-1086.45, -411.37), None, (("Geometry", "Group Input", "Geometry"), )),
            "Evaluate at Index": ("GeometryNodeFieldAtIndex", (36.69, -315.51), None, (("Index", "Integer Math", "Value"), ("Value", "Repeat Input", "Value"), )),
            "Evaluate at Index.001": ("GeometryNodeFieldAtIndex", (38.12, -280.66), None, (("Index", "Reroute.002", "Output"), ("Value", "Repeat Input", "Value"), )),
            "Group Input": ("NodeGroupInput", (-1368.97, 13.6), None, ()),
            "Group Output": ("NodeGroupOutput", (1445.07, -62.63), None, (("Geometry", "Switch", "Output"), )),
            "Index": ("GeometryNodeInputIndex", (-1068.53, -322.54), None, ()),
            "Integer Math": ("FunctionNodeIntegerMath", (-146.04, -312.63), None, (("Value", "Reroute.002", "Output"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (-836.84, 34.24), None, (("Value", "Domain Size.001", "Point Count"), ("Value#1", "Group Input", "Iterations"), )),
            "Integer Math.002": ("FunctionNodeIntegerMath", (-167.81, -158.85), None, (("Value", "Repeat Input", "Iteration"), ("Value#1", "Domain Size.001", "Point Count"), )),
            "Math.003": ("ShaderNodeMath", (21.02, -214.7), None, (("Value", "Reroute.002", "Output"), ("Value#1", "Integer Math.002", "Value"), )),
            "Mesh to Curve": ("GeometryNodeMeshToCurve", (-1078.03, 28.53), None, (("Mesh", "Group Input", "Geometry"), )),
            "Mix": ("ShaderNodeMix", (247.87, -159.68), None, (("A#1", "Evaluate at Index.001", "Value"), ("B#1", "Evaluate at Index", "Value"), ("Factor", "Math.003", "Value"), )),
            "Position": ("GeometryNodeInputPosition", (-1060.78, -254.43), None, ()),
            "Repeat Input": ("GeometryNodeRepeatInput", (-449.67, -52.6), None, (("Geometry", "Resample Curve", "Curve"), ("Iterations", "Group Input", "Iterations"), ("Value", "Sample Index", "Value"), )),
            "Repeat Output": ("GeometryNodeRepeatOutput", (615.29, -20.4), None, (("Geometry", "Capture Attribute", "Geometry"), ("Value", "Capture Attribute", "Value"), )),
            "Reroute.002": ("NodeReroute", (-220.32, -279.86), None, (("Input", "Index", "Index"), )),
            "Resample Curve": ("GeometryNodeResampleCurve", (-666.52, 69.27), None, (("Count", "Integer Math.001", "Value"), ("Curve", "Mesh to Curve", "Curve"), )),
            "Sample Index": ("GeometryNodeSampleIndex", (-835.61, -125.23), None, (("Geometry", "Mesh to Curve", "Curve"), ("Index", "Index", "Index"), ("Value", "Position", "Position"), )),
            "Set Position": ("GeometryNodeSetPosition", (810.41, -14.77), None, (("Geometry", "Repeat Output", "Geometry"), ("Position", "Repeat Output", "Value"), )),
            "Switch": ("GeometryNodeSwitch", (1206.02, 82.22), None, (("False", "Curve to Mesh", "Mesh"), ("Switch", "Compare", "Result"), ("True", "Group Input", "Geometry"), )),
        }