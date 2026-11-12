from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class MaterialPassThrough(CustomGeometryGroup):
    _name = "Material Pass Through"
    _color_tag = "GEOMETRY"
    _tree_properties = {"node_tool_idname": "geometry.material_pass_through", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        geom_to_paint = tree.inputs.geometry("Geom To paint")
        painted_geom = tree.inputs.geometry("Painted Geom")
        enable = tree.inputs.boolean("Enable", True)
        output = tree.outputs.geometry("Output")

        separate_components = g.SeparateComponents(geom_to_paint).props(width=140.0, hide_outputs=["Curve", "Grease Pencil", "Point Cloud", "Volume", "Instances"])
        reroute = g.Reroute(input=separate_components.o.mesh).props(width=9.5)
        remove_named_attribute = ((painted_geom >> g.SeparateComponents()).props(width=140.0, hide_outputs=["Curve", "Grease Pencil", "Point Cloud", "Volume", "Instances"]) >> g.RemoveNamedAttribute(pattern_mode="Wildcard", name="*")).props(width=170.0, warning_propagation="NONE")
        capture = g.CaptureAttribute.point(geometry=remove_named_attribute)
        value = capture.items.boolean(True, "Value")
        delete_geometry = (
            g.JoinGeometry((capture.o.geometry, reroute))
            >> g.SetMaterialIndex(material_index=g.SampleIndex.face.integer(remove_named_attribute, g.MaterialIndex()))
            >> g.DeleteGeometry.point(selection=value.output)
        )
        enable.switch.geometry(reroute, delete_geometry) >> output

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Capture Attribute": ("GeometryNodeCaptureAttribute", (-406.91, 13.75), None, (("Geometry", "Remove Named Attribute", "Geometry"), )),
            "Delete Geometry.001": ("GeometryNodeDeleteGeometry", (79.75, 37.48), None, (("Geometry", "Set Material Index", "Geometry"), ("Selection", "Capture Attribute", "Value"), )),
            "Group Input": ("NodeGroupInput", (-977.68, 178.63), None, ()),
            "Group Output": ("NodeGroupOutput", (464.12, 175.54), None, (("Output", "Switch.006", "Output"), )),
            "Join Geometry.004": ("GeometryNodeJoinGeometry", (-236.81, 38.09), None, (("Geometry", "Capture Attribute", "Geometry"), ("Geometry", "Reroute", "Output"), )),
            "Material Index": ("GeometryNodeInputMaterialIndex", (-597.65, -266.39), None, ()),
            "Remove Named Attribute": ("GeometryNodeRemoveAttribute", (-620.72, -6.64), None, (("Geometry", "Separate Components.001", "Mesh"), )),
            "Reroute": ("NodeReroute", (-323.44, 77.35), None, (("Input", "Separate Components", "Mesh"), )),
            "Sample Index": ("GeometryNodeSampleIndex", (-406.49, -144.56), None, (("Geometry", "Remove Named Attribute", "Geometry"), ("Value", "Material Index", "Material Index"), )),
            "Separate Components": ("GeometryNodeSeparateComponents", (-763.52, 199.34), None, (("Geometry", "Group Input", "Geom To paint"), )),
            "Separate Components.001": ("GeometryNodeSeparateComponents", (-791.34, -22.11), None, (("Geometry", "Group Input", "Painted Geom"), )),
            "Set Material Index": ("GeometryNodeSetMaterialIndex", (-79.47, 40.27), None, (("Geometry", "Join Geometry.004", "Geometry"), ("Material Index", "Sample Index", "Value"), )),
            "Switch.006": ("GeometryNodeSwitch", (286.32, 180.68), None, (("False", "Reroute", "Output"), ("Switch", "Group Input", "Enable"), ("True", "Delete Geometry.001", "Geometry"), )),
        }