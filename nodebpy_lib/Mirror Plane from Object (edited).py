from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class MirrorPlaneFromObjectEdited(CustomGeometryGroup):
    _name = "Mirror Plane from Object (edited)"
    _color_tag = "INPUT"
    _tree_properties = {"node_tool_idname": "geometry.mirror_plane_from_object", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        object = tree.inputs.object("Object")
        axis = tree.inputs.integer("Axis", 0, min_value=0, max_value=2, structure_type="SINGLE", force_non_field=True)
        normal = tree.outputs.vector("Normal", subtype="XYZ")
        location = tree.outputs.vector("Location")

        object_info = g.ObjectInfo(object=object, as_instance=True, transform_space="RELATIVE")
        (
            g.IndexSwitch.vector(axis, ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))).o.output.transform_direction(object_info.o.transform)
            >> normal
        )

        object_info.o.location >> location

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-476.81, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (312.02, 40.79), None, (("Location", "Object Info.001", "Location"), ("Normal", "Transform Direction", "Direction"), )),
            "Index Switch": ("GeometryNodeIndexSwitch", (-239.92, -52.11), None, (("Index", "Group Input", "Axis"), )),
            "Object Info.001": ("GeometryNodeObjectInfo", (-249.05, 173.62), None, (("Object", "Group Input", "Object"), )),
            "Transform Direction": ("FunctionNodeTransformDirection", (61.71, 169.08), None, (("Direction", "Index Switch", "Output"), ("Transform", "Object Info.001", "Transform"), )),
        }