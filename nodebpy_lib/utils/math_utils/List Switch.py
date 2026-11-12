from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("List Switch", arrange=None, clear=True) as tree:
    count = tree.inputs.integer("Count", 0)
    switch = tree.inputs.boolean("Switch", False)
    false = tree.inputs.float("False", 0.0)
    true = tree.inputs.float("True", 0.0)
    output = tree.outputs.float("Output", description="Output list with evaluated field values")

    index = g.Index().props(width=100.0, hide=True)
    switch_1 = g.GetListItem.boolean(switch, index).props(hide=True).o.value.switch.float(g.GetListItem.float(false, index).props(hide=True), g.GetListItem.float(true, index).props(hide=True))
    g.FieldToList(count=count, items={"Output": switch_1}) >> output

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Field to List.001": ("GeometryNodeFieldToList", (163.03, 92.73), None, (("Count", "Group Input", "Count"), ("Output", "Switch.009", "Output"), )),
    "Get List Item.010": ("GeometryNodeListGetItem", (-170.9, -28.21), None, (("Index", "Index.006", "Index"), ("List", "Group Input", "False"), )),
    "Get List Item.011": ("GeometryNodeListGetItem", (-170.9, -70.54), None, (("Index", "Index.006", "Index"), ("List", "Group Input", "True"), )),
    "Get List Item.012": ("GeometryNodeListGetItem", (-170.9, 14.13), None, (("Index", "Index.006", "Index"), ("List", "Group Input", "Switch"), )),
    "Group Input": ("NodeGroupInput", (-392.4, 73.53), None, ()),
    "Group Output": ("NodeGroupOutput", (363.03, 0.0), None, (("Output", "Field to List.001", "Output"), )),
    "Index.006": ("GeometryNodeInputIndex", (-158.04, -123.7), None, ()),
    "Switch.009": ("GeometryNodeSwitch", (1.5, 72.03), None, (("False", "Get List Item.010", "Value"), ("Switch", "Get List Item.012", "Value"), ("True", "Get List Item.011", "Value"), )),
}