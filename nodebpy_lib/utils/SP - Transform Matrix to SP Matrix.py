from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("SP - Transform Matrix to SP Matrix", arrange=None, clear=True) as tree:
    matrix = tree.inputs.matrix("Matrix")
    output = tree.outputs.float("Output")

    separate_matrix = g.SeparateMatrix(matrix)
    (
        g.IndexSwitch.float(g.Index(), (separate_matrix.o.column_1_row_1, separate_matrix.o.column_1_row_2, separate_matrix.o.column_1_row_3, separate_matrix.o.column_1_row_4, separate_matrix.o.column_2_row_1, separate_matrix.o.column_2_row_2, separate_matrix.o.column_2_row_3, separate_matrix.o.column_2_row_4, separate_matrix.o.column_3_row_1, separate_matrix.o.column_3_row_2, separate_matrix.o.column_3_row_3, separate_matrix.o.column_3_row_4, separate_matrix.o.column_4_row_1, separate_matrix.o.column_4_row_2, separate_matrix.o.column_4_row_3, separate_matrix.o.column_4_row_4))
        >> output
    )

# Restore authored node names and positions (matched by tree
# structure — see TreeBuilder.layout_snapshot).
tree.layout_snapshot = {
    "Group Input": ("NodeGroupInput", (-305.11, 0.0), None, ()),
    "Group Output": ("NodeGroupOutput", (295.11, 0.0), None, (("Output", "Index Switch", "Output"), )),
    "Index": ("GeometryNodeInputIndex", (-96.28, 31.05), None, ()),
    "Index Switch": ("GeometryNodeIndexSwitch", (105.11, -10.95), None, (("0", "Separate Matrix", "Column 1 Row 1"), ("1", "Separate Matrix", "Column 1 Row 2"), ("10", "Separate Matrix", "Column 3 Row 3"), ("11", "Separate Matrix", "Column 3 Row 4"), ("12", "Separate Matrix", "Column 4 Row 1"), ("13", "Separate Matrix", "Column 4 Row 2"), ("14", "Separate Matrix", "Column 4 Row 3"), ("15", "Separate Matrix", "Column 4 Row 4"), ("2", "Separate Matrix", "Column 1 Row 3"), ("3", "Separate Matrix", "Column 1 Row 4"), ("4", "Separate Matrix", "Column 2 Row 1"), ("5", "Separate Matrix", "Column 2 Row 2"), ("6", "Separate Matrix", "Column 2 Row 3"), ("7", "Separate Matrix", "Column 2 Row 4"), ("8", "Separate Matrix", "Column 3 Row 1"), ("9", "Separate Matrix", "Column 3 Row 2"), ("Index", "Index", "Index"), )),
    "Separate Matrix": ("FunctionNodeSeparateMatrix", (-105.11, -31.05), None, (("Matrix", "Group Input", "Matrix"), )),
}