from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Is Rational", arrange=None, clear=True) as tree:
    geometry = tree.inputs.geometry("Geometry")
    is_rational = tree.outputs.boolean("Is Rational")

    domain_size = g.DomainSize(geometry).props(hide=True, hide_outputs=["Edge Count", "Face Count", "Face Corner Count"])
    compare = g.Compare.integer.equal((domain_size.o.point_count - 1).props(hide=True), g.Index()).props(hide=True)
    named_attribute = g.NamedAttribute.float("Weight")
    boolean_math = (g.Compare.float.not_equal(0.0, named_attribute.o.attribute, 0.0).o.result & g.Compare.float.not_equal(1.0, named_attribute.o.attribute, 0.0)).props(hide=True)
    attribute_statistic = g.AttributeStatistic.point.float(geometry, (~compare.o.result).props(hide=True), boolean_math).props(hide_outputs=["Mean", "Median", "Min", "Max", "Range", "Standard Deviation", "Variance"])
    g.Compare.integer.not_equal(attribute_statistic.o.sum, 0) >> is_rational

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Attribute Statistic": ("GeometryNodeAttributeStatistic", (245.08, 157.64), None, (("Attribute", "Boolean Math.023", "Boolean"), ("Geometry", "Group Input", "Geometry"), ("Selection", "Boolean Math.024", "Boolean"), )),
    "Boolean Math.023": ("FunctionNodeBooleanMath", (39.31, -176.78), None, (("Boolean", "Compare.015", "Result"), ("Boolean#1", "Compare.017", "Result"), )),
    "Boolean Math.024": ("FunctionNodeBooleanMath", (44.45, 164.49), None, (("Boolean", "Compare.019", "Result"), )),
    "Compare.015": ("FunctionNodeCompare", (-138.92, -21.65), None, (("B", "Named Attribute.006", "Attribute"), )),
    "Compare.017": ("FunctionNodeCompare", (-138.19, -199.85), None, (("B", "Named Attribute.006", "Attribute"), )),
    "Compare.018": ("FunctionNodeCompare", (409.67, 152.45), None, (("A", "Attribute Statistic", "Sum"), )),
    "Compare.019": ("FunctionNodeCompare", (35.15, 122.83), None, (("A", "Integer Math", "Value"), ("B", "Index", "Index"), )),
    "Domain Size": ("GeometryNodeAttributeDomainSize", (-124.2, 204.51), None, (("Geometry", "Group Input", "Geometry"), )),
    "Group Input": ("NodeGroupInput", (-385.87, 79.21), None, ()),
    "Group Output": ("NodeGroupOutput", (630.04, 0.0), None, (("Is Rational", "Compare.018", "Result"), )),
    "Index": ("GeometryNodeInputIndex", (-124.2, 125.61), None, ()),
    "Integer Math": ("FunctionNodeIntegerMath", (-120.96, 164.22), None, (("Value", "Domain Size", "Point Count"), )),
    "Named Attribute.006": ("GeometryNodeInputNamedAttribute", (-395.86, -192.86), None, ()),
}