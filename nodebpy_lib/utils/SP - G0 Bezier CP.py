from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - G0 Bezier CP", arrange=None, clear=True) as tree:
    position = tree.inputs.vector("Position", (0.0, 0.0, 0.0))
    target_position = tree.inputs.vector("Target Position", (0.0, 0.0, 0.0), hide_value=True)
    index = tree.inputs.integer("Index", 0, hide_value=True)
    position_1 = tree.outputs.vector("Position")

    (
        g.Compare.integer.equal(g.Index(), index.point.at()).o.result.switch.vector(position, target_position.point.at())
        >> position_1
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Compare": ("FunctionNodeCompare", (-18.46, 77.83), None, (("A", "Index", "Index"), ("B", "Evaluate at Index.006", "Value"), )),
    "Evaluate at Index.002": ("GeometryNodeFieldAtIndex", (-22.29, -77.83), None, (("Value", "Group Input", "Target Position"), )),
    "Evaluate at Index.006": ("GeometryNodeFieldAtIndex", (-197.8, -7.87), None, (("Value", "Group Input", "Index"), )),
    "Group Input": ("NodeGroupInput", (-399.07, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (389.07, 0.0), None, (("Position", "Switch.004", "Output"), )),
    "Index": ("GeometryNodeInputIndex", (-194.58, 50.54), None, ()),
    "Switch.004": ("GeometryNodeSwitch", (218.05, 48.1), None, (("False", "Group Input", "Position"), ("Switch", "Compare", "Result"), ("True", "Evaluate at Index.002", "Value"), )),
}