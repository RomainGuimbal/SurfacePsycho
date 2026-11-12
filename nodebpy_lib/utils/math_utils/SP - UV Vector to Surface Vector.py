from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPUVVectorToSurfaceVector(CustomGeometryGroup):
    _name = "SP - UV Vector to Surface Vector"
    _color_tag = "VECTOR"
    _tree_properties = {"default_group_node_width": 220}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        uv_vector = tree.inputs.vector("UV Vector", (0.0, 0.0), dimensions=2)
        su = tree.inputs.vector("Su", (0.0, 0.0, 0.0), hide_value=True)
        sv = tree.inputs.vector("Sv", (0.0, 0.0, 0.0), hide_value=True)
        vector = tree.outputs.vector("Vector")

        math_1 = ((uv_vector.x * su.x).props(hide=True) + (uv_vector.y * sv.x).props(hide=True)).props(hide=True)
        math_2 = ((uv_vector.x * su.y).props(hide=True) + (uv_vector.y * sv.y).props(hide=True)).props(hide=True)
        math_3 = ((uv_vector.x * su.z).props(hide=True) + (uv_vector.y * sv.z).props(hide=True)).props(hide=True)
        combine_xyz = g.CombineXYZ(x=math_1, y=math_2, z=math_3)

        combine_xyz >> vector

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Combine XYZ": ("ShaderNodeCombineXYZ", (316.39, 8.54), None, (("X", "Math.002", "Value"), ("Y", "Math.005", "Value"), ("Z", "Math.008", "Value"), )),
            "Group Input": ("NodeGroupInput", (-519.81, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (516.39, 0.0), None, (("Vector", "Combine XYZ", "Vector"), )),
            "Math": ("ShaderNodeMath", (-63.88, 65.55), None, (("Value", "Separate XYZ.001", "X"), ("Value#1", "Separate XYZ", "X"), )),
            "Math.001": ("ShaderNodeMath", (-64.98, 23.75), None, (("Value", "Separate XYZ.001", "Y"), ("Value#1", "Separate XYZ.002", "X"), )),
            "Math.002": ("ShaderNodeMath", (115.01, 33.65), None, (("Value", "Math", "Value"), ("Value#1", "Math.001", "Value"), )),
            "Math.003": ("ShaderNodeMath", (-66.08, -16.95), None, (("Value", "Separate XYZ.001", "X"), ("Value#1", "Separate XYZ", "Y"), )),
            "Math.004": ("ShaderNodeMath", (-67.18, -58.76), None, (("Value", "Separate XYZ.001", "Y"), ("Value#1", "Separate XYZ.002", "Y"), )),
            "Math.005": ("ShaderNodeMath", (116.57, -38.34), None, (("Value", "Math.003", "Value"), ("Value#1", "Math.004", "Value"), )),
            "Math.006": ("ShaderNodeMath", (-66.08, -98.36), None, (("Value", "Separate XYZ.001", "X"), ("Value#1", "Separate XYZ", "Z"), )),
            "Math.007": ("ShaderNodeMath", (-67.18, -140.16), None, (("Value", "Separate XYZ.001", "Y"), ("Value#1", "Separate XYZ.002", "Z"), )),
            "Math.008": ("ShaderNodeMath", (116.57, -119.74), None, (("Value", "Math.006", "Value"), ("Value#1", "Math.007", "Value"), )),
            "Separate XYZ": ("ShaderNodeSeparateXYZ", (-319.81, 16.53), None, (("Vector", "Group Input", "Su"), )),
            "Separate XYZ.001": ("ShaderNodeSeparateXYZ", (-317.87, 131.65), None, (("Vector", "Group Input", "UV Vector"), )),
            "Separate XYZ.002": ("ShaderNodeSeparateXYZ", (-317.61, -118.23), None, (("Vector", "Group Input", "Sv"), )),
        }