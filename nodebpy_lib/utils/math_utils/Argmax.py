from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class Argmax(CustomGeometryGroup):
    _name = "Argmax"
    _color_tag = "CONVERTER"
    _tree_properties = {"node_tool_idname": "geometry.argmax", "show_modifier_manage_panel": False, "is_modifier": True}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        geometry = tree.inputs.geometry("Geometry")
        attribute = tree.inputs.float("Attribute", 0.0)
        point_count = tree.inputs.integer("Point Count", 0)
        argmax = tree.outputs.integer("Argmax")
        value = tree.outputs.float("Value")

        capture = g.CaptureAttribute.point(geometry=geometry)
        index = capture.items.integer(g.Index(), "Index")
        attribute_1 = capture.items.float(attribute, "Attribute")
        integer_math = (point_count - 1).props(hide=True)
        sort_elements = capture.o.geometry >> g.SortElements.point(sort_weight=attribute)
        sample_index = g.SampleIndex.point.integer(sort_elements, index.output, integer_math).props(hide=True)
        sample_index_1 = g.SampleIndex.point.float(sort_elements, attribute_1.output, integer_math).props(hide=True)

        sample_index >> argmax
        sample_index_1 >> value

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Capture Attribute": ("GeometryNodeCaptureAttribute", (547.83, 158.87), None, (("Attribute", "Group Input", "Attribute"), ("Geometry", "Group Input", "Geometry"), ("Index", "Index.003", "Index"), )),
            "Group Input": ("NodeGroupInput", (247.22, 7.2), None, ()),
            "Group Output": ("NodeGroupOutput", (1282.76, 66.3), None, (("Argmax", "Sample Index.001", "Value"), ("Value", "Sample Index.002", "Value"), )),
            "Index.003": ("GeometryNodeInputIndex", (333.01, 181.38), None, ()),
            "Integer Math": ("FunctionNodeIntegerMath", (816.65, -81.22), None, (("Value", "Group Input", "Point Count"), )),
            "Sample Index.001": ("GeometryNodeSampleIndex", (1091.37, 71.28), None, (("Geometry", "Sort Elements", "Geometry"), ("Index", "Integer Math", "Value"), ("Value", "Capture Attribute", "Index"), )),
            "Sample Index.002": ("GeometryNodeSampleIndex", (1086.85, -17.82), None, (("Geometry", "Sort Elements", "Geometry"), ("Index", "Integer Math", "Value"), ("Value", "Capture Attribute", "Attribute"), )),
            "Sort Elements": ("GeometryNodeSortElements", (817.58, 165.65), None, (("Geometry", "Capture Attribute", "Geometry"), ("Sort Weight", "Group Input", "Attribute"), )),
        }