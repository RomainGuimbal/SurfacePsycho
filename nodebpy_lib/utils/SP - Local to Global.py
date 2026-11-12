from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPLocalToGlobal(CustomGeometryGroup):
    _name = "SP - Local to Global"
    _color_tag = "VECTOR"
    _tree_properties = {"node_tool_idname": "geometry.sp_local_to_global", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        vector = tree.inputs.vector("Vector", (0.0, 0.0, 0.0), min_value=-10_000.0, max_value=10_000.0, hide_value=True)
        vector_1 = tree.outputs.vector("Vector")

        vector.transform(g.ObjectInfo(g.SelfObject()).o.transform) >> vector_1

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-214.79, 132.18), None, ()),
            "Group Output": ("NodeGroupOutput", (311.39, 131.19), None, (("Vector", "Transform Point", "Vector"), )),
            "Object Info": ("GeometryNodeObjectInfo", (-204.75, -23.42), None, (("Object", "Self Object", "Self Object"), )),
            "Self Object": ("GeometryNodeSelfObject", (-362.58, -142.2), None, ()),
            "Transform Point": ("FunctionNodeTransformPoint", (-5.2, 133.07), None, (("Transform", "Object Info", "Transform"), ("Vector", "Group Input", "Vector"), )),
        }