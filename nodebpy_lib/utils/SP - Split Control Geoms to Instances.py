from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPSplitControlGeomsToInstances(CustomGeometryGroup):
    _name = "SP - Split Control Geoms to Instances"
    _color_tag = "GEOMETRY"
    _tree_properties = {"default_group_node_width": 240, "node_tool_idname": "geometry.sp_split_control_geoms_to_instances", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        patches = tree.inputs.geometry("Patches")
        instances = tree.outputs.geometry("Instances")

        (
            patches
            >> g.SplitEdges(selection=g.NamedAttribute.boolean("Endpoints").o.attribute)
            >> g.SplitToInstances.point(group_id=g.MeshIsland().o.island_index)
            >> instances
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Group Input": ("NodeGroupInput", (-258.89, 49.49), None, ()),
            "Group Output": ("NodeGroupOutput", (520.63, 3.77), None, (("Instances", "Split to Instances", "Instances"), )),
            "Mesh Island": ("GeometryNodeInputMeshIsland", (110.04, -102.32), None, ()),
            "Named Attribute": ("GeometryNodeInputNamedAttribute", (-68.21, -14.94), None, ()),
            "Split Edges": ("GeometryNodeSplitEdges", (112.92, 51.78), None, (("Mesh", "Group Input", "Patches"), ("Selection", "Named Attribute", "Attribute"), )),
            "Split to Instances": ("GeometryNodeSplitToInstances", (295.0, 41.07), None, (("Geometry", "Split Edges", "Mesh"), ("Group ID", "Mesh Island", "Island Index"), )),
        }