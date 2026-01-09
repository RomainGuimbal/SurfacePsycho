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