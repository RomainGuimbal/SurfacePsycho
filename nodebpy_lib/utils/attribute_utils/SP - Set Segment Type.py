from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPSetSegmentType(CustomGeometryGroup):
    _name = "SP - Set Segment Type"
    _color_tag = "ATTRIBUTE"
    _tree_properties = {"default_group_node_width": 180, "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        segment_cp = tree.inputs.geometry("Segment CP")
        type = tree.inputs.menu("Type", "Bezier", optional_label=True, structure_type="SINGLE", force_non_field=True)
        several_segments = tree.inputs.boolean("Several segments", False)
        output = tree.outputs.geometry("Output")

        menu_switch = g.MenuSwitch.integer(type, {"Bezier": 0, "NURBS": 1, "Circle Arc": 2, "Circle": 3, "Ellipse Arc": 4, "Ellipse": 5})
        (
            (segment_cp >> g.StoreNamedAttribute.point.integer(selection=g.Compare.integer.equal(g.Index(), 0).o.result | several_segments, name="Type", value=menu_switch.o.output)).props(width=140.0)
            >> output
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math": ("FunctionNodeBooleanMath", (115.61, 99.3), None, (("Boolean", "Compare", "Result"), ("Boolean#1", "Group Input", "Several segments"), )),
            "Compare": ("FunctionNodeCompare", (-99.62, 146.23), None, (("A", "Index", "Index"), )),
            "Group Input": ("NodeGroupInput", (-309.75, -12.46), None, ()),
            "Group Output": ("NodeGroupOutput", (520.58, -30.86), None, (("Output", "Store Named Attribute.005", "Geometry"), )),
            "Index": ("GeometryNodeInputIndex", (-315.36, 190.46), None, ()),
            "Menu Switch": ("GeometryNodeMenuSwitch", (-88.1, -90.79), None, (("Menu", "Group Input", "Type"), )),
            "Store Named Attribute.005": ("GeometryNodeStoreNamedAttribute", (355.39, 22.42), None, (("Geometry", "Group Input", "Segment CP"), ("Selection", "Boolean Math", "Boolean"), ("Value", "Menu Switch", "Output"), )),
        }