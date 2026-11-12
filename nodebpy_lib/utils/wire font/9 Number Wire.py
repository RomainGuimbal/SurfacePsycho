from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("9 Number Wire", arrange="sugiyama", clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((-0.09, 0.06, 0.0), (-0.08, 0.03, 0.0), (-0.05, 0.01, 0.0), (-0.015, 0.0, 0.0), (0.065, 0.0, 0.0), (0.09, 0.019999996, 0.0), (0.1, 0.05000001, 0.0), (0.1, 0.2, 0.0), (0.09, 0.23, 0.0), (0.065, 0.25, 0.0), (0.03, 0.26, 0.0), (-0.03, 0.26, 0.0), (-0.065, 0.25, 0.0), (-0.09, 0.23, 0.0), (-0.1, 0.19, 0.0), (-0.09, 0.16, 0.0), (-0.07, 0.145, 0.0), (-0.04000001, 0.14, 0.0), (0.1, 0.14, 0.0)))
    g.MeshLine(19) >> g.SetPosition(position=index_switch) >> geometry