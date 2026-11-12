from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Object Type ID", arrange=None, clear=True) as tree:
    object_type = tree.inputs.menu("Object Type", "Plane", optional_label=True)
    id = tree.outputs.integer("ID")

    (
        g.MenuSwitch.integer(object_type, {"Plane": 0, "Cylinder": 1, "Cone": 2, "Shpere": 3, "Torus": 4, "Bezier Surface": 5, "Nurbs Surface": 6, "Revolution": 7, "Extrusion": 8, "Curve": 10, "Other": 14})
        >> id
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-106.61, -4.52), None, ()),
    "Group Output": ("NodeGroupOutput", (272.92, -12.54), None, (("ID", "Menu Switch", "Output"), )),
    "Menu Switch": ("GeometryNodeMenuSwitch", (84.48, -7.49), None, (("Menu", "Group Input", "Object Type"), )),
}