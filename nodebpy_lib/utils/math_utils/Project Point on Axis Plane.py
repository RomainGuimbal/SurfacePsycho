from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class ProjectPointOnAxisPlane(CustomGeometryGroup):
    _name = "Project Point on Axis Plane"
    _color_tag = "VECTOR"
    _tree_properties = {"node_tool_idname": "geometry.project_vector_on_plane", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        object_matrix = tree.inputs.matrix("Object Matrix")
        axis = tree.inputs.integer("Axis", 0, min_value=0, max_value=2)
        point = tree.inputs.vector("Point", (0.0, 0.0, 0.0), subtype="XYZ")
        vector = tree.outputs.vector("Vector", subtype="XYZ")

        vector_math = point.project_point(object_matrix.invert()) * g.IndexSwitch.vector(axis, ((0.0, 1.0, 1.0), (1.0, 0.0, 1.0), (1.0, 1.0, 0.0)))
        vector_math.transform(object_matrix) >> vector

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-473.74, 52.86), None, ()),
            "Group Output": ("NodeGroupOutput", (561.22, 0.0), None, (("Vector", "Transform Point", "Vector"), )),
            "Index Switch": ("GeometryNodeIndexSwitch", (-78.53, -37.21), None, (("Index", "Group Input", "Axis"), )),
            "Invert Matrix": ("FunctionNodeInvertMatrix", (-203.17, 130.07), None, (("Matrix", "Group Input", "Object Matrix"), )),
            "Project Point": ("FunctionNodeProjectPoint", (4.63, 108.53), None, (("Transform", "Invert Matrix", "Matrix"), ("Vector", "Group Input", "Point"), )),
            "Transform Point": ("FunctionNodeTransformPoint", (368.92, 61.21), None, (("Transform", "Group Input", "Object Matrix"), ("Vector", "Vector Math.001", "Vector"), )),
            "Vector Math.001": ("ShaderNodeVectorMath", (182.4, 65.37), None, (("Vector", "Project Point", "Vector"), ("Vector#1", "Index Switch", "Output"), )),
        }