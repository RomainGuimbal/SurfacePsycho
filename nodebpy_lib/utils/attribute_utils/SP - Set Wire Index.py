from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPSetWireIndex(CustomGeometryGroup):
    _name = "SP - Set Wire Index"
    _color_tag = "ATTRIBUTE"
    _tree_properties = {"node_tool_idname": "geometry.sp_set_wire_index", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        input = tree.inputs.geometry("Input")
        wire_index_of_cp = tree.outputs.integer("Wire Index of CP")

        mesh_island = g.MeshIsland()
        with g.Frame("detect outer wire"):
            integer_math = (mesh_island.o.island_index + 1).props(label="no wire 0", width=138.73)
            position = g.Position()
            reroute = g.Reroute(input=input).props(width=19.0)
            attribute_statistic = g.AttributeStatistic.point.vector(reroute, attribute=position).props(hide_inputs=["Selection"], hide_outputs=["Mean", "Sum", "Min", "Max", "Range", "Standard Deviation", "Variance"])
            capture = g.CaptureAttribute.point(geometry=reroute)
            island_index = capture.items.integer(integer_math, "Island Index")
            sample_index = (
                capture.o.geometry
                >> g.SortElements.point(sort_weight=0.0 - position.o.position.distance(attribute_statistic.o.median).props(hide=True))
                >> g.SampleIndex.point.integer(value=island_index.output)
            )
        reroute_1 = g.Reroute(input=input).props(width=19.0)
        reroute_2 = g.Reroute(input=integer_math).props(width=19.0)
        switch = g.Compare.integer.equal(reroute_2, sample_index).props(hide=True).o.result.switch.integer(reroute_2, 0 - reroute_2)
        sample_index_1 = g.SampleIndex.point.integer(reroute_1, switch, g.Index()).props(width=138.7)
        with g.Frame("Speed up with single wire"):
            compare = g.Compare.integer.equal(g.SampleIndex.point.integer(reroute_1, mesh_island.o.island_count).props(hide=True), 1)
            compare.o.result.switch.integer(sample_index_1, -1) >> wire_index_of_cp

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Attribute Statistic.002": ("GeometryNodeAttributeStatistic", (269.24, -373.36), "Frame.015", (("Attribute", "Position.007", "Position"), ("Geometry", "Reroute.030", "Output"), )),
            "Capture Attribute.002": ("GeometryNodeCaptureAttribute", (365.51, -131.13), "Frame.015", (("Geometry", "Reroute.030", "Output"), ("Island Index", "Integer Math.001", "Value"), )),
            "Compare.005": ("FunctionNodeCompare", (209.73, -36.07), "Frame.004", (("A", "Sample Index.003", "Value"), )),
            "Compare.010": ("FunctionNodeCompare", (294.08, 106.33), None, (("A", "Reroute.031", "Output"), ("B", "Sample Index.012", "Value"), )),
            "Frame.004": ("NodeFrame", (492.35, 529.98), None, ()),
            "Frame.015": ("NodeFrame", (-846.0, 142.45), None, ()),
            "Group Input": ("NodeGroupInput", (-1077.57, 520.5), None, ()),
            "Group Output": ("NodeGroupOutput", (1173.95, 391.94), None, (("Wire Index of CP", "Switch.012", "Output"), )),
            "Index.012": ("GeometryNodeInputIndex", (461.65, 9.36), None, ()),
            "Integer Math": ("FunctionNodeIntegerMath", (279.36, -3.47), None, (("Value#1", "Reroute.031", "Output"), )),
            "Integer Math.001": ("FunctionNodeIntegerMath", (173.09, -35.99), "Frame.015", (("Value", "Mesh Island.004", "Island Index"), )),
            "Math.003": ("ShaderNodeMath", (438.76, -372.16), "Frame.015", (("Value#1", "Vector Math.004", "Value"), )),
            "Mesh Island.004": ("GeometryNodeInputMeshIsland", (-1018.45, 312.79), None, ()),
            "Position.007": ("GeometryNodeInputPosition", (30.14, -300.82), "Frame.015", ()),
            "Reroute": ("NodeReroute", (400.76, 445.18), None, (("Input", "Group Input", "Input"), )),
            "Reroute.030": ("NodeReroute", (144.6, -180.09), "Frame.015", (("Input", "Group Input", "Input"), )),
            "Reroute.031": ("NodeReroute", (201.84, 63.41), None, (("Input", "Integer Math.001", "Value"), )),
            "Sample Index.003": ("GeometryNodeSampleIndex", (30.25, -87.1), "Frame.004", (("Geometry", "Reroute", "Output"), ("Value", "Mesh Island.004", "Island Count"), )),
            "Sample Index.011": ("GeometryNodeSampleIndex", (720.11, 263.57), None, (("Geometry", "Reroute", "Output"), ("Index", "Index.012", "Index"), ("Value", "Switch.011", "Output"), )),
            "Sample Index.012": ("GeometryNodeSampleIndex", (766.0, -130.98), "Frame.015", (("Geometry", "Sort Elements.002", "Geometry"), ("Value", "Capture Attribute.002", "Island Index"), )),
            "Sort Elements.002": ("GeometryNodeSortElements", (604.11, -128.23), "Frame.015", (("Geometry", "Capture Attribute.002", "Geometry"), ("Sort Weight", "Math.003", "Value"), )),
            "Switch.011": ("GeometryNodeSwitch", (465.39, 167.65), None, (("False", "Reroute.031", "Output"), ("Switch", "Compare.010", "Result"), ("True", "Integer Math", "Value"), )),
            "Switch.012": ("GeometryNodeSwitch", (399.83, -47.78), "Frame.004", (("False", "Sample Index.011", "Value"), ("Switch", "Compare.005", "Result"), )),
            "Vector Math.004": ("ShaderNodeVectorMath", (439.21, -329.7), "Frame.015", (("Vector", "Position.007", "Position"), ("Vector#1", "Attribute Statistic.002", "Median"), )),
        }