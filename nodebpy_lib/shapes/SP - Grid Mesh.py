from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPGridMesh(CustomGeometryGroup):
    _name = "SP - Grid Mesh"
    _color_tag = "GEOMETRY"
    _tree_properties = {"node_tool_idname": "geometry.sp_grid_mesh", "show_modifier_manage_panel": False}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        u_count = tree.inputs.integer("U Count", 2, min_value=0)
        v_count = tree.inputs.integer("V Count", 2, min_value=0)
        min_u = tree.inputs.float("Min U", 0.0, min_value=-10_000.0, max_value=10_000.0)
        max_u = tree.inputs.float("Max U", 1.0, min_value=-10_000.0, max_value=10_000.0)
        min_v = tree.inputs.float("Min V", 0.0, min_value=-10_000.0, max_value=10_000.0)
        max_v = tree.inputs.float("Max V", 1.0, min_value=-10_000.0, max_value=10_000.0)
        shade_smooth = tree.inputs.boolean("Shade Smooth", True, structure_type="SINGLE", force_non_field=True)
        mesh = tree.outputs.geometry("Mesh")

        combine_xyz = g.CombineXYZ(x=min_u, y=min_v)
        grid = g.Grid(vertices_x=v_count, vertices_y=u_count)
        vector_math = g.CombineXYZ(x=grid.o.uv_map.y, y=grid.o.uv_map.x).o.vector * (g.CombineXYZ(x=max_u, y=max_v).o.vector - combine_xyz)
        (
            (grid >> g.SetPosition(position=vector_math, offset=combine_xyz) >> g.StoreNamedAttribute.corner.vector_2d(name="UVMap", value=g.Position())).props(width=140.0)
            >> g.FlipFaces()
            >> g.SetShadeSmooth.face(shade_smooth=shade_smooth)
            >> mesh
        )

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Combine XYZ": ("ShaderNodeCombineXYZ", (502.86, 35.87), None, (("X", "Separate XYZ", "Y"), ("Y", "Separate XYZ", "X"), )),
            "Combine XYZ.001": ("ShaderNodeCombineXYZ", (381.47, -164.34), None, (("X", "Group Input", "Min U"), ("Y", "Group Input", "Min V"), )),
            "Combine XYZ.002": ("ShaderNodeCombineXYZ", (380.9, -294.31), None, (("X", "Group Input", "Max U"), ("Y", "Group Input", "Max V"), )),
            "Flip Faces": ("GeometryNodeFlipFaces", (1366.34, 144.58), None, (("Mesh", "Store Named Attribute", "Geometry"), )),
            "Grid.001": ("GeometryNodeMeshGrid", (164.82, 138.06), None, (("Vertices X", "Group Input", "V Count"), ("Vertices Y", "Group Input", "U Count"), )),
            "Group Input": ("NodeGroupInput", (-237.82, -59.94), None, ()),
            "Group Output": ("NodeGroupOutput", (1717.23, 143.0), None, (("Mesh", "Set Shade Smooth", "Mesh"), )),
            "Position": ("GeometryNodeInputPosition", (1027.5, 71.42), None, ()),
            "Separate XYZ": ("ShaderNodeSeparateXYZ", (338.3, 29.27), None, (("Vector", "Grid.001", "UV Map"), )),
            "Set Position": ("GeometryNodeSetPosition", (1026.57, 208.26), None, (("Geometry", "Grid.001", "Mesh"), ("Offset", "Combine XYZ.001", "Vector"), ("Position", "Vector Math.001", "Vector"), )),
            "Set Shade Smooth": ("GeometryNodeSetShadeSmooth", (1553.6, 134.68), None, (("Mesh", "Flip Faces", "Mesh"), ("Shade Smooth", "Group Input", "Shade Smooth"), )),
            "Store Named Attribute": ("GeometryNodeStoreNamedAttribute", (1189.54, 201.61), None, (("Geometry", "Set Position", "Geometry"), ("Value", "Position", "Position"), )),
            "Vector Math": ("ShaderNodeVectorMath", (572.85, -218.18), None, (("Vector", "Combine XYZ.002", "Vector"), ("Vector#1", "Combine XYZ.001", "Vector"), )),
            "Vector Math.001": ("ShaderNodeVectorMath", (842.77, -3.95), None, (("Vector", "Combine XYZ", "Vector"), ("Vector#1", "Vector Math", "Vector"), )),
        }