from nodebpy import geometry as g, TreeBuilder

with TreeBuilder("4 Number Wire", arrange="sugiyama", clear=True) as tree:
    geometry = tree.outputs.geometry("Geometry")

    index_switch = g.IndexSwitch.vector(g.Index(), ((0.0, 0.0, 0.0), (0.0, 0.13, 0.0), (0.0, 0.26, 0.0), (-0.1, 0.07, 0.0), (0.1, 0.07, 0.0)))
    (
        g.JoinGeometry((g.MeshLine(count=2, offset=(1.0, 0.0, 0.0)).props(hide=True), g.MeshLine(count=3, offset=(1.0, 0.0, 0.0))))
        >> g.SetPosition(position=index_switch)
        >> geometry
    )