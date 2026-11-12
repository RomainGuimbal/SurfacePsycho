from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPIsolateSegments(CustomGeometryGroup):
    _name = "SP - Isolate Segments"
    _color_tag = "GEOMETRY"
    _tree_properties = {"default_group_node_width": 160}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        geometry = tree.inputs.geometry("Geometry")
        segment_index = tree.inputs.integer("Segment Index", 0)
        min = tree.inputs.integer("Min", 0, structure_type="SINGLE", force_non_field=True)
        max = tree.inputs.integer("Max", 0, structure_type="SINGLE", force_non_field=True)
        selection = tree.outputs.geometry("Selection", description="The parts of the geometry in the selection")

        boolean_math = ((segment_index >= min).props(width=160.0, hide=True) & (segment_index < max).props(width=160.0, hide=True)).props(width=100.0, hide=True)
        capture = g.CaptureAttribute.point(geometry=geometry)
        index = capture.items.integer(g.Index(), "Index")
        separate_geometry = (
            capture.o.geometry
            >> g.SeparateGeometry.edge(selection=boolean_math)
        )
        with g.Frame("Inversion because of point 0"):
            compare = g.Compare.integer.equal(g.SampleIndex.point.integer(separate_geometry.o.selection, index.output), 0)
            compare_1 = g.Compare.integer.not_equal(g.SampleIndex.point.integer(separate_geometry.o.selection, index.output, 1), 1)
            boolean_math_1 = compare.o.result & compare_1
        (
            boolean_math_1.switch.geometry(separate_geometry.o.selection, g.MeshToCurve(separate_geometry.o.selection) >> g.ReverseCurve() >> g.CurveToMesh())
            >> selection
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math": ("FunctionNodeBooleanMath", (396.32, -99.31), "Frame", (("Boolean", "Compare.001", "Result"), ("Boolean#1", "Compare.002", "Result"), )),
            "Boolean Math.004": ("FunctionNodeBooleanMath", (-52.05, -85.33), None, (("Boolean", "Compare.008", "Result"), ("Boolean#1", "Compare.007", "Result"), )),
            "Capture Attribute": ("GeometryNodeCaptureAttribute", (-135.56, 331.37), None, (("Geometry", "Group Input", "Geometry"), ("Index", "Index.001", "Index"), )),
            "Compare.001": ("FunctionNodeCompare", (194.69, -52.17), "Frame", (("A", "Sample Index", "Value"), )),
            "Compare.002": ("FunctionNodeCompare", (195.33, -212.98), "Frame", (("A", "Sample Index.001", "Value"), )),
            "Compare.007": ("FunctionNodeCompare", (-246.8, -102.89), None, (("A", "Group Input", "Segment Index"), ("B", "Group Input", "Max"), )),
            "Compare.008": ("FunctionNodeCompare", (-245.18, -64.68), None, (("A", "Group Input", "Segment Index"), ("B", "Group Input", "Min"), )),
            "Curve to Mesh": ("GeometryNodeCurveToMesh", (809.01, -53.64), None, (("Curve", "Reverse Curve", "Curve"), )),
            "Frame": ("NodeFrame", (462.18, 554.86), None, ()),
            "Group Input": ("NodeGroupInput", (-586.37, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (1623.8, 41.03), None, (("Selection", "Switch", "Output"), )),
            "Index.001": ("GeometryNodeInputIndex", (-355.56, 307.33), None, ()),
            "Mesh to Curve": ("GeometryNodeMeshToCurve", (477.73, -60.41), None, (("Mesh", "Separate Geometry.001", "Selection"), )),
            "Reverse Curve": ("GeometryNodeReverseCurve", (641.28, -74.19), None, (("Curve", "Mesh to Curve", "Curve"), )),
            "Sample Index": ("GeometryNodeSampleIndex", (32.89, -36.03), "Frame", (("Geometry", "Separate Geometry.001", "Selection"), ("Value", "Capture Attribute", "Index"), )),
            "Sample Index.001": ("GeometryNodeSampleIndex", (30.34, -239.6), "Frame", (("Geometry", "Separate Geometry.001", "Selection"), ("Value", "Capture Attribute", "Index"), )),
            "Separate Geometry.001": ("GeometryNodeSeparateGeometry", (124.13, 11.87), None, (("Geometry", "Capture Attribute", "Geometry"), ("Selection", "Boolean Math.004", "Boolean"), )),
            "Switch": ("GeometryNodeSwitch", (1250.41, 58.17), None, (("False", "Separate Geometry.001", "Selection"), ("Switch", "Boolean Math", "Boolean"), ("True", "Curve to Mesh", "Mesh"), )),
        }