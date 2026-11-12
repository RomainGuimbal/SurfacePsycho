from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class InstancesPassThrough(CustomGeometryGroup):
    _name = "Instances Pass Through"
    _color_tag = "GEOMETRY"
    _tree_properties = {"default_group_node_width": 160, "node_tool_idname": "geometry.instances_pass_through", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        geom = tree.inputs.geometry("Geom")
        all = tree.inputs.geometry("All")
        enable = tree.inputs.boolean("Enable", True, structure_type="SINGLE", force_non_field=True)
        output = tree.outputs.geometry("Output")

        join_geometry = g.JoinGeometry((geom, g.GetGeometryComponent(geometry=all, type="Instances", remove=False).o.component))
        enable.switch.geometry(geom, join_geometry) >> output

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Get Geometry Component": ("GeometryNodeGetGeometryComponent", (-186.32, -73.18), None, (("Geometry", "Group Input", "All"), )),
            "Group Input": ("NodeGroupInput", (-440.0, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (448.46, -1.13), None, (("Output", "Switch", "Output"), )),
            "Join Geometry": ("GeometryNodeJoinGeometry", (70.43, -9.62), None, (("Geometry", "Get Geometry Component", "Component"), ("Geometry", "Group Input", "Geom"), )),
            "Switch": ("GeometryNodeSwitch", (248.55, 160.27), None, (("False", "Group Input", "Geom"), ("Switch", "Group Input", "Enable"), ("True", "Join Geometry", "Geometry"), )),
        }