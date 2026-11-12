from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPEvaluateCircleAtParameter(CustomGeometryGroup):
    _name = "SP - Evaluate Circle at Parameter"
    _color_tag = "VECTOR"
    _tree_properties = {"default_group_node_width": 215, "node_tool_idname": "geometry.sp_evaluate_circle_at_parameter", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        scaled_basis = tree.inputs.matrix("Scaled Basis")
        parameter_pseudo_angle = tree.inputs.float("Parameter (pseudo angle)", 0.0, description="Pseudo angle")
        position = tree.outputs.vector("Position", subtype="XYZ")
        tangent = tree.outputs.vector("Tangent", subtype="XYZ")
        curvature = tree.outputs.vector("Curvature", subtype="XYZ")
        jerk = tree.outputs.vector("Jerk", subtype="XYZ")
        snap = tree.outputs.vector("Snap", subtype="XYZ")

        math_1 = parameter_pseudo_angle.sin()
        math_2 = 0.0 - math_1
        math_3 = parameter_pseudo_angle.cos()
        math_4 = 0.0 - math_3
        reroute = g.Reroute(input=g.CombineTransform(rotation=scaled_basis.rotation, scale=scaled_basis.scale).o.transform).props(width=19.0)
        g.CombineXYZ(x=math_2, y=math_3).o.vector.transform(reroute) >> tangent
        g.CombineXYZ(x=math_4, y=math_2).o.vector.transform(reroute) >> curvature
        g.CombineXYZ(x=math_1, y=math_4).o.vector.transform(reroute) >> jerk
        g.CombineXYZ(x=math_3, y=math_1).o.vector.transform(reroute) >> snap
        g.CombineXYZ(x=math_3, y=math_1).o.vector.transform(scaled_basis) >> position

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Combine Transform.002": ("FunctionNodeCombineTransform", (-590.31, -243.06), None, (("Rotation", "Separate Transform", "Rotation"), ("Scale", "Separate Transform", "Scale"), )),
            "Combine XYZ": ("ShaderNodeCombineXYZ", (257.23, -92.09), None, (("X", "Math.001", "Value"), ("Y", "Math.003", "Value"), )),
            "Combine XYZ.001": ("ShaderNodeCombineXYZ", (261.04, -268.71), None, (("X", "Math.002", "Value"), ("Y", "Math.001", "Value"), )),
            "Combine XYZ.002": ("ShaderNodeCombineXYZ", (257.3, -447.61), None, (("X", "Math", "Value"), ("Y", "Math.002", "Value"), )),
            "Combine XYZ.003": ("ShaderNodeCombineXYZ", (255.8, -621.32), None, (("X", "Math.003", "Value"), ("Y", "Math", "Value"), )),
            "Combine XYZ.004": ("ShaderNodeCombineXYZ", (254.21, 85.81), None, (("X", "Math.003", "Value"), ("Y", "Math", "Value"), )),
            "Group Input": ("NodeGroupInput", (-1171.71, -111.31), None, ()),
            "Group Output": ("NodeGroupOutput", (1019.8, -387.73), None, (("Curvature", "Transform Point.001", "Vector"), ("Jerk", "Transform Point.002", "Vector"), ("Position", "Transform Point.004", "Vector"), ("Snap", "Transform Point.003", "Vector"), ("Tangent", "Transform Point", "Vector"), )),
            "Math": ("ShaderNodeMath", (-613.6, 212.7), None, (("Value", "Group Input", "Parameter (pseudo angle)"), )),
            "Math.001": ("ShaderNodeMath", (-205.36, -349.35), None, (("Value#1", "Math", "Value"), )),
            "Math.002": ("ShaderNodeMath", (-208.31, -522.79), None, (("Value#1", "Math.003", "Value"), )),
            "Math.003": ("ShaderNodeMath", (-614.45, 73.87), None, (("Value", "Group Input", "Parameter (pseudo angle)"), )),
            "Reroute": ("NodeReroute", (461.98, -239.27), None, (("Input", "Combine Transform.002", "Transform"), )),
            "Separate Transform": ("FunctionNodeSeparateTransform", (-762.72, -276.88), None, (("Transform", "Group Input", "Scaled Basis"), )),
            "Transform Point": ("FunctionNodeTransformPoint", (504.96, -92.82), None, (("Transform", "Reroute", "Output"), ("Vector", "Combine XYZ", "Vector"), )),
            "Transform Point.001": ("FunctionNodeTransformPoint", (506.44, -277.29), None, (("Transform", "Reroute", "Output"), ("Vector", "Combine XYZ.001", "Vector"), )),
            "Transform Point.002": ("FunctionNodeTransformPoint", (502.81, -451.02), None, (("Transform", "Reroute", "Output"), ("Vector", "Combine XYZ.002", "Vector"), )),
            "Transform Point.003": ("FunctionNodeTransformPoint", (501.36, -619.71), None, (("Transform", "Reroute", "Output"), ("Vector", "Combine XYZ.003", "Vector"), )),
            "Transform Point.004": ("FunctionNodeTransformPoint", (502.03, 79.94), None, (("Transform", "Group Input", "Scaled Basis"), ("Vector", "Combine XYZ.004", "Vector"), )),
        }