from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("5 Number Wire", arrange="sugiyama", clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((-0.09, 0.03, 0.0), (-0.065, 0.01, 0.0), (-0.030000005, 0.00000000745058, 0.0), (0.03, 0.0, 0.0), (0.065, 0.01, 0.0), (0.09, 0.02999999, 0.0), (0.1, 0.07000002, 0.0), (0.1, 0.12, 0.0), (0.075, 0.155, 0.0), (0.03, 0.17, 0.0), (-0.06, 0.17, 0.0), (-0.06, 0.26, 0.0), (0.1, 0.26, 0.0)))
    g.MeshLine(13) >> g.SetPosition(position=index_switch) >> geometry