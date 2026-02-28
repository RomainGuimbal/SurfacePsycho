from enum import Enum
from OCP.GeomAbs import (
    GeomAbs_Plane,
    GeomAbs_Cylinder,
    GeomAbs_Cone,
    GeomAbs_Sphere,
    GeomAbs_Torus,
    GeomAbs_BezierSurface,
    GeomAbs_BSplineSurface,
    GeomAbs_SurfaceOfRevolution,
    GeomAbs_SurfaceOfExtrusion,
    GeomAbs_OtherSurface,
)


class SP_obj_type(Enum):
    PLANE = 0
    CYLINDER = 1
    CONE = 2
    SPHERE = 3
    TORUS = 4
    BEZIER_SURFACE = 5
    BSPLINE_SURFACE = 6
    SURFACE_OF_REVOLUTION = 7
    SURFACE_OF_EXTRUSION = 8
    OTHER_SURFACE = 9
    INSTANCE = 10
    EMPTY = 11
    CURVE = 12
    COMPOUND = 13


# TYPES_FROM_CP_ATTR = {
#     "CP_any_order_surf": SP_obj_type.BEZIER_SURFACE,
#     "CP_NURBS_surf": SP_obj_type.BSPLINE_SURFACE,
#     "CP_planar": SP_obj_type.PLANE,
#     "CP_curve": SP_obj_type.CURVE,
#     "axis3_cylinder": SP_obj_type.CYLINDER,
#     "axis3_torus": SP_obj_type.TORUS,
#     "axis3_cone": SP_obj_type.CONE,
#     "axis3_sphere": SP_obj_type.SPHERE,
#     "CP_extrusion": SP_obj_type.SURFACE_OF_EXTRUSION,
#     "CP_revolution": SP_obj_type.SURFACE_OF_REVOLUTION,
# }

geom_to_sp_type = {
    GeomAbs_Plane: SP_obj_type.PLANE,
    GeomAbs_Cylinder: SP_obj_type.CYLINDER,
    GeomAbs_Cone: SP_obj_type.CONE,
    GeomAbs_Sphere: SP_obj_type.SPHERE,
    GeomAbs_Torus: SP_obj_type.TORUS,
    GeomAbs_BezierSurface: SP_obj_type.BEZIER_SURFACE,
    GeomAbs_BSplineSurface: SP_obj_type.BSPLINE_SURFACE,
    GeomAbs_SurfaceOfRevolution: SP_obj_type.SURFACE_OF_REVOLUTION,
    GeomAbs_SurfaceOfExtrusion: SP_obj_type.SURFACE_OF_EXTRUSION,
    GeomAbs_OtherSurface: SP_obj_type.OTHER_SURFACE,
}

MESHER_NAMES = {
    SP_obj_type.PLANE: "SP - FlatPatch Meshing",
    SP_obj_type.CYLINDER: "SP - Cylindrical Meshing",
    SP_obj_type.CONE: "SP - Conical Meshing",
    SP_obj_type.SPHERE: "SP - Spherical Meshing",
    SP_obj_type.TORUS: "SP - Toroidal Meshing",
    SP_obj_type.BEZIER_SURFACE: "SP - Bezier Patch Meshing",
    SP_obj_type.BSPLINE_SURFACE: "SP - NURBS Patch Meshing",
    SP_obj_type.SURFACE_OF_REVOLUTION: "SP - Surface of Revolution Meshing",
    SP_obj_type.SURFACE_OF_EXTRUSION: "SP - Surface of Extrusion Meshing",
    SP_obj_type.CURVE: "SP - Curve Meshing",
    SP_obj_type.COMPOUND: "SP - Compound Meshing",
}


# to replace with official index
class SP_segment_type(Enum):
    BEZIER = 0
    NURBS = 1
    CIRCLE_ARC = 2
    CIRCLE = 3
    ELLIPSE_ARC = 4
    ELLIPSE = 5


EDGES_TYPES = {
    "line": 0,  # Not absurd
    "bezier": 0,
    "nurbs": 1,
    "circle_arc": 2,
    "circle": 3,
    "ellipse_arc": 4,
    "ellipse": 5,
}


ASSET_NODE_GROUPS_CURVE_AND_FLATPATCH = {
    "SP - Blend Curve",
    "SP - Connect Curve",
    "SP - Continuities between Segments",
    "SP - Convert Circles and Ellipses to Splines",
    "SP - Copy Mesh Face",
    "SP - Crop or Extend Curve",
    "SP - Crown Curve",
    "SP - Curve Meshing",
    "SP - Distance Between Curves",
    "SP - Fillet Curve or FlatPatch",
    "SP - Fillet Polyline with Circles",
    "SP - Fit Curve",
    "SP - FlatPatch Meshing",
    "SP - Inset FlatPatch",
    "SP - Interpolate Curve or FlatPatch",
    "SP - Interval Curve",
    "SP - Make SVG Ready",
    "SP - Mirror Curve Control Points",
    "SP - Mirror FlatPatch or Curve",
    "SP - Multi Split Curve",
    "SP - NURBS to Bezier Curve or FlatPatch",
    "SP - Oblong Wire",
    "SP - Offset Curve",
    "SP - Project on Flat Patch",
    "SP - Radial Array FlatPatch",
    "SP - Raise or Lower Curve Degree",
    "SP - Raise or Lower Order of Selected Segment",
    "SP - Reorder Curve Index",
    "SP - Reorder Curve Selection",
    "SP - Reproject Ellipse Arcs Ends",
    "SP - Resample Selection",
    "SP - Sample Curve Per Degree",
    "SP - Set Edge Length",
    "SP - Split Curve",
    "SP - Switch Curve Direction",
    # "SP - Bezier Circlular Arc",
    # "SP - Compose FlatPatch From Sides",
    # "SP - Curve on Surface from UV",
}

ASSET_NODE_GROUPS_BEZIER_PATCH = {
    "SP - Bezier Patch Meshing",
    "SP - Coon Patch",
    "SP - Blend Surfaces",
    "SP - Connect Bezier Patch",
    "SP - Convert Contour",
    "SP - Crop Patch to Point",
    "SP - Displace Bezier Patch Control Grid",
    "SP - Offset Precisely",
    "SP - Fillet Trim Contour",
    "SP - Flatten Patch",
    "SP - Flatten Patch Side",
    "SP - Gradient Map",
    "SP - Loft",
    "SP - Loft from Internal Curves",
    "SP - Mirror Patch Control Points",
    "SP - Nearest Curve on Bezier Patch",
    "SP - Patch Exact Normals",
    "SP - Project Curve on Bezier Patch",
    "SP - Raise or Lower Degree Bezier Patch",
    "SP - Reorder Grid Index",
    "SP - Ruled Surface from Mesh Loop",
    "SP - Select Patch Range",
    "SP - Convert Flat Patch to Bezier Patch",
    "SP - Trim Bezier Surface from Projected Wires",
}

ASSET_NODE_GROUPS_NURBS_PATCH = {
    "SP - NURBS Patch Meshing",
    "SP - NURBS Weighting",
    "SP - Set Knot NURBS Patch",
    "SP - Crop or Extend Patch",
    "SP - Insert Knot NURBS Patch",
    "SP - Curvature Analysis",
    "SP - Continuity Analysis",
    "SP - Fit Patch",
    "SP - Interpolate Patch",
    "SP_Curvature",
    "SP - Normalize NURBS Patch Knots",
}

ASSET_NODE_GROUPS_OTHER_SURFACES = {
    "SP - Cylindrical Meshing",
    "SP - Toroidal Meshing",
    "SP - Spherical Meshing",
    "SP - Conical Meshing",
    "SP - Surface of Extrusion Meshing",
    "SP - Surface of Revolution Meshing",
    "SP - Plot Distance from Mesh",
    "SP - Copy Geometry",
    "SP - Adjust Revolution Sweep Angle",
    "SP - Transform UVMap",
    "SP - Isoparametric Curve",
}

ASSET_NODE_GROUPS_COMPOUND = {
    "SP - Compound Meshing",
    "SP - SubD to Compound",
    "SP - Poly to Compound",
    "SP - Text to Compound",
    "SP - Set Patch Instance Type",
    "SP - Split to Patches",
    "SP - Intersect Bezier Patches",
    "SP - Extrude FlatPatch",
    "SP - Interval Curves",
    "SP - NURBS to Bezier Patches",
    "SP - Profile Revolution Compound",
}

ASSET_NODE_GROUPS_SHAPE_PRESETS = {
    "SP - Cylinder Compound",
    "SP - Disc CP",
    "SP - Frame Compound",
    "SP - Oblong Extrusion Compound",
    "SP - Slab Compound",
    "SP - Tubes Compound",
}

ASSET_NODE_GROUPS = (
    ASSET_NODE_GROUPS_CURVE_AND_FLATPATCH
    | ASSET_NODE_GROUPS_BEZIER_PATCH
    | ASSET_NODE_GROUPS_NURBS_PATCH
    | ASSET_NODE_GROUPS_OTHER_SURFACES
    | ASSET_NODE_GROUPS_COMPOUND
    | ASSET_NODE_GROUPS_SHAPE_PRESETS
)
