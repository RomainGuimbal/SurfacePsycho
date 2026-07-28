from enum import StrEnum, IntEnum
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
    GeomAbs_OffsetSurface,
    GeomAbs_OtherSurface,
)
from os.path import dirname, abspath, basename, join
from pathlib import Path

ADDON_PATH = dirname(dirname(abspath(__file__)))  # The PsychoPath ;)


def get_addon_version():
    # get version from toml file
    path = ADDON_PATH + "/blender_manifest.toml"
    with open(path, "r") as f:
        for line in f:
            if line.startswith("version"):
                version = line.split('"')[1]
                break
    return version


VERSION_STR = get_addon_version()
ASSETS_PATH = Path(join(ADDON_PATH, "assets")).resolve()
ASSETS_FILE = Path(join(ASSETS_PATH, "assets.blend")).resolve()
ADDON_PREF_KEY = "bl_ext." + basename(dirname(ADDON_PATH)) + ".SurfacePsycho"


class SP_obj_type(IntEnum):
    PLANE = 0
    CYLINDER = 1
    CONE = 2
    SPHERE = 3
    TORUS = 4
    BEZIER_SURFACE = 5
    BSPLINE_SURFACE = 6
    SURFACE_OF_REVOLUTION = 7
    SURFACE_OF_EXTRUSION = 8
    OFFSET_SURFACE = 9
    CURVE = 10
    INSTANCE = 11
    EMPTY = 12
    COMPOUND = 13
    OTHER_SURFACE = 14

    @property
    def mesher_name(self) -> "MesherName":
        """Get corresponding MesherName."""
        return MesherName[self.name] if self.name in MesherName.keys() else None


GEOM_TO_SP_TYPE = {
    GeomAbs_Plane: SP_obj_type.PLANE,
    GeomAbs_Cylinder: SP_obj_type.CYLINDER,
    GeomAbs_Cone: SP_obj_type.CONE,
    GeomAbs_Sphere: SP_obj_type.SPHERE,
    GeomAbs_Torus: SP_obj_type.TORUS,
    GeomAbs_BezierSurface: SP_obj_type.BEZIER_SURFACE,
    GeomAbs_BSplineSurface: SP_obj_type.BSPLINE_SURFACE,
    GeomAbs_SurfaceOfRevolution: SP_obj_type.SURFACE_OF_REVOLUTION,
    GeomAbs_SurfaceOfExtrusion: SP_obj_type.SURFACE_OF_EXTRUSION,
    GeomAbs_OffsetSurface: SP_obj_type.OFFSET_SURFACE,
    GeomAbs_OtherSurface: SP_obj_type.OTHER_SURFACE,
}


class MesherName(StrEnum):
    PLANE = "SP - FlatPatch Meshing"
    CYLINDER = "SP - Cylindrical Meshing"
    CONE = "SP - Conical Meshing"
    SPHERE = "SP - Spherical Meshing"
    TORUS = "SP - Toroidal Meshing"
    BEZIER_SURFACE = "SP - Bezier Patch Meshing"
    BSPLINE_SURFACE = "SP - NURBS Patch Meshing"
    SURFACE_OF_REVOLUTION = "SP - Surface of Revolution Meshing"
    SURFACE_OF_EXTRUSION = "SP - Surface of Extrusion Meshing"
    OFFSET_SURFACE = ""
    CURVE = "SP - Curve Meshing"
    COMPOUND = "SP - Compound Meshing"

    @classmethod
    def keys(self):
        return [s.name for s in self]


# to replace with official index
class SP_segment_type(IntEnum):
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
