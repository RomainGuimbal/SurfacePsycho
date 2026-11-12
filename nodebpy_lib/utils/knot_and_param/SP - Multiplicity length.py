from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Multiplicity length", arrange=None, clear=True) as tree:
    geometry = tree.inputs.geometry("Geometry")
    multiplicity = tree.inputs.integer("Multiplicity", 0, description="Must not have parasit tail")
    length = tree.outputs.integer("Length")

    with g.Frame("Mult length"):
        attribute_statistic = g.AttributeStatistic.point.float(geometry, attribute=multiplicity > 0).props(hide_inputs=["Selection"], hide_outputs=["Mean", "Median", "Min", "Max", "Range", "Standard Deviation", "Variance"])
        float_to_integer = g.FloatToInteger(float=attribute_statistic.o.sum, rounding_mode="FLOOR")

    float_to_integer >> length

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Attribute Statistic.001": ("GeometryNodeAttributeStatistic", (207.4, -36.16), "Frame.015", (("Attribute", "Compare.016", "Result"), ("Geometry", "Group Input", "Geometry"), )),
    "Compare.016": ("FunctionNodeCompare", (30.02, -155.72), "Frame.015", (("A", "Group Input", "Multiplicity"), )),
    "Float to Integer": ("FunctionNodeFloatToInt", (369.13, -63.83), "Frame.015", (("Float", "Attribute Statistic.001", "Sum"), )),
    "Frame.015": ("NodeFrame", (-447.35, 188.51), None, ()),
    "Group Input": ("NodeGroupInput", (-670.95, 96.71), None, ()),
    "Group Output": ("NodeGroupOutput", (128.73, 96.07), None, (("Length", "Float to Integer", "Integer"), )),
}