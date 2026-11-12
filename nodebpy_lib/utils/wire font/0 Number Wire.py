from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("0 Number Wire", arrange="sugiyama", clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((0.1, 0.2, 0.0), (0.1, 0.06, 0.0), (0.09, 0.03, 0.0), (0.065, 0.01, 0.0), (0.03, 0.0, 0.0), (-0.03, 0.0, 0.0), (-0.065, 0.01, 0.0), (-0.09, 0.03, 0.0), (-0.1, 0.06, 0.0), (-0.1, 0.2, 0.0), (-0.09, 0.23, 0.0), (-0.065, 0.25, 0.0), (-0.03, 0.26, 0.0), (0.03, 0.26, 0.0), (0.065, 0.25, 0.0), (0.09, 0.23, 0.0)))
    set_position = g.SetPosition(geometry=g.MeshCircle(16), position=index_switch)
    viewer = g.Viewer()
    viewer.items.geometry(set_position, "Geometry")

    set_position >> geometry