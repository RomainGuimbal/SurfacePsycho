from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPFlatten(CustomGeometryGroup):
    _name = "SP - Flatten"
    _color_tag = "GEOMETRY"
    _tree_properties = {"node_tool_idname": "geometry.sp_flatten", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        geometry = tree.inputs.geometry("Geometry")
        orient = tree.inputs.boolean("Orient", False)
        offset = tree.inputs.vector("Offset", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0)
        normal = tree.inputs.vector("Normal", (0.0, 0.0, 1.0))
        geometry_1 = tree.outputs.geometry("Geometry")

        with g.Frame("flatten"):
            reroute = g.Reroute(input=geometry).props(width=19.0)
            transform_geometry = g.TransformGeometry(geometry=reroute, translation=((0.0, 0.0, 0.0) - offset).props(hide=True)).props(width=140.0, hide_inputs=["Rotation", "Scale"])
            transform_geometry_1 = g.TransformGeometry(geometry=transform_geometry, rotation=g.AlignRotationToVector(vector=normal, factor=-1.0)).props(width=140.0, hide_inputs=["Translation", "Scale"])
            (
                (orient.switch.geometry(reroute, transform_geometry_1) >> g.TransformGeometry(scale=(1.0, 1.0, 0.0))).props(width=140.0)
                >> geometry_1
            )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Align Rotation to Vector": ("FunctionNodeAlignRotationToVector", (205.49, -353.28), "Frame.012", (("Vector", "Group Input", "Normal"), )),
            "Frame.012": ("NodeFrame", (-380.12, 187.86), None, ()),
            "Group Input": ("NodeGroupInput", (-628.57, 66.33), None, ()),
            "Group Output": ("NodeGroupOutput", (649.37, 116.52), None, (("Geometry", "Transform Geometry.001", "Geometry"), )),
            "Reroute.038": ("NodeReroute", (148.43, -153.52), "Frame.012", (("Input", "Group Input", "Geometry"), )),
            "Switch.015": ("GeometryNodeSwitch", (553.48, -80.33), "Frame.012", (("False", "Reroute.038", "Output"), ("Switch", "Group Input", "Orient"), ("True", "Transform Geometry.013", "Geometry"), )),
            "Transform Geometry.001": ("GeometryNodeTransform", (770.56, -56.11), "Frame.012", (("Geometry", "Switch.015", "Output"), )),
            "Transform Geometry.013": ("GeometryNodeTransform", (367.58, -211.96), "Frame.012", (("Geometry", "Transform Geometry.014", "Geometry"), ("Rotation", "Align Rotation to Vector", "Rotation"), )),
            "Transform Geometry.014": ("GeometryNodeTransform", (203.21, -214.71), "Frame.012", (("Geometry", "Reroute.038", "Output"), ("Translation", "Vector Math", "Vector"), )),
            "Vector Math": ("ShaderNodeVectorMath", (30.11, -269.49), "Frame.012", (("Vector#1", "Group Input", "Offset"), )),
        }