from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("2 Number Wire", arrange="sugiyama", clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((0.1, 0.0, 0.0), (-0.1, 0.0, 0.0), (-0.09, 0.05, 0.0), (-0.065, 0.085, 0.0), (0.065, 0.145, 0.0), (0.09, 0.17, 0.0), (0.1, 0.2, 0.0), (0.09, 0.23, 0.0), (0.065, 0.25, 0.0), (0.03, 0.26, 0.0), (-0.03, 0.26, 0.0), (-0.065, 0.25, 0.0), (-0.09, 0.23, 0.0)))
    g.MeshLine(13) >> g.SetPosition(position=index_switch) >> geometry