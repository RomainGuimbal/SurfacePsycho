from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class VLetterWire(CustomGeometryGroup):
    _name = "V Letter Wire"
    _color_tag = "INPUT"
    _tree_properties = {"default_group_node_width": 160}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        geometry = tree.outputs.geometry("Geometry")

        with g.Frame():
            vector_math = g.IndexSwitch.vector(g.Index(), ((0.1, 0.2, 0.0), (0.0, -0.06, 0.0), (-0.1, 0.2, 0.0))).o.output * 0.23
            g.MeshLine(3) >> g.SetPosition(position=vector_math) >> geometry

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Frame.001": ("NodeFrame", (-369.53, 159.35), None, ()),
            "Group Input": ("NodeGroupInput", (-569.09, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (589.08, 0.0), None, (("Geometry", "Set Position.001", "Geometry"), )),
            "Index Switch.001": ("GeometryNodeIndexSwitch", (206.04, -103.94), "Frame.001", (("Index", "Index.001", "Index"), )),
            "Index.001": ("GeometryNodeInputIndex", (30.35, -179.33), "Frame.001", ()),
            "Mesh Line.002": ("GeometryNodeMeshLine", (392.09, -30.02), "Frame.001", ()),
            "Set Position.001": ("GeometryNodeSetPosition", (738.62, -230.49), "Frame.001", (("Geometry", "Mesh Line.002", "Mesh"), ("Position", "Vector Math.002", "Vector"), )),
            "Vector Math.002": ("ShaderNodeVectorMath", (386.0, -318.89), "Frame.001", (("Vector", "Index Switch.001", "Output"), )),
        }