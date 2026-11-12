from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPGetWeight(CustomGeometryGroup):
    _name = "SP - Get Weight"
    _color_tag = "INPUT"

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        geometry = tree.inputs.geometry("Geometry", description="Geometry to sample a value on")
        weights = tree.outputs.float("Weights")
        exists = tree.outputs.boolean("Exists")

        named_attribute = g.NamedAttribute.float("Weight")
        compare = g.Compare.float.equal(named_attribute.o.attribute, 0.0, 0.0).props(width=100.0, hide=True)
        boolean_math = (compare.o.result | (~named_attribute.o.exists).props(width=100.0, hide=True)).props(width=100.0, hide=True)
        (
            (geometry >> g.SampleIndex.point.boolean(value=named_attribute.o.exists)).props(hide=True)
            >> exists
        )
        boolean_math.switch.float(named_attribute.o.attribute, 1.0) >> weights

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Boolean Math.001": ("FunctionNodeBooleanMath", (-34.96, -73.35), None, (("Boolean", "Named Attribute", "Exists"), )),
            "Boolean Math.002": ("FunctionNodeBooleanMath", (90.84, -43.61), None, (("Boolean", "Compare.002", "Result"), ("Boolean#1", "Boolean Math.001", "Boolean"), )),
            "Compare.002": ("FunctionNodeCompare", (-36.58, -31.81), None, (("A", "Named Attribute", "Attribute"), )),
            "Group Input": ("NodeGroupInput", (-449.9, 148.79), None, ()),
            "Group Output": ("NodeGroupOutput", (468.73, 161.6), None, (("Exists", "Sample Index.003", "Value"), ("Weights", "Switch.001", "Output"), )),
            "Named Attribute": ("GeometryNodeInputNamedAttribute", (-248.7, 44.23), None, ()),
            "Sample Index.003": ("GeometryNodeSampleIndex", (-76.93, 146.7), None, (("Geometry", "Group Input", "Geometry"), ("Value", "Named Attribute", "Exists"), )),
            "Switch.001": ("GeometryNodeSwitch", (248.7, 73.35), None, (("False", "Named Attribute", "Attribute"), ("Switch", "Boolean Math.002", "Boolean"), )),
        }