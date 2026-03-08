from dataclasses import dataclass
from mathutils import Vector
from ..common.enums import SP_segment_type
from ..common.utils import (
    vec_list_to_step_cartesian2d,
    vec_list_to_step_cartesian,
    float_list_to_tcolstd_H,
    knot_tcol_from_att,
    vec_to_gp_pnt,
    vec_to_gp_pnt2d,
    vec_to_gp_pnt_on_plane,
)
from .export_ellipse import gp_Elips_from_3_points, gp_Elips2d_from_3_points
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCP.GC import (
    GC_MakeArcOfCircle,
    GC_MakeSegment,
    GC_MakeCircle,
    GC_MakeArcOfEllipse,
    GC_MakeEllipse,
)
from OCP.GCE2d import (
    GCE2d_MakeSegment,
    GCE2d_MakeArcOfCircle,
    GCE2d_MakeCircle,
    GCE2d_MakeArcOfEllipse,
    GCE2d_MakeEllipse,
)
from OCP.Geom import Geom_BezierCurve
from OCP.Geom2d import Geom2d_BezierCurve
from OCP.GeomAdaptor import GeomAdaptor_Surface
from OCP.gp import gp_Dir, gp_Ax2, gp_Vec
from OCP.StepGeom import (
    StepGeom_BSplineCurveWithKnotsAndRationalBSplineCurve,
    StepGeom_BSplineCurveForm,
    StepGeom_KnotType,
)
from OCP.StepData import StepData_Logical, StepData_Factors
from OCP.StepToGeom import StepToGeom
from OCP.TCollection import TCollection_HAsciiString
from OCP import GeomAbs


### Input data


@dataclass
class SP_Segment:
    type: SP_segment_type
    vec_cp: list[Vector]
    weight: list[float] = None
    degree: int = None
    is_clamped: bool = True
    is_periodic: bool = False
    knot: list = None
    mult: list = None

    def point_count(self):
        return len(self.vec_cp)

    def gp_cp(self):
        return map(vec_to_gp_pnt, self.vec_cp)


@dataclass
class SP_Segment_2d(SP_Segment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def gp_cp(self):
        return map(vec_to_gp_pnt2d, self.vec_cp)


@dataclass
class SP_Segment_on_plane(SP_Segment):
    def __init__(self, plane: GeomAbs.GeomAbs_Plane, **kwargs):
        super().__init__(**kwargs)
        self.geom_plane = plane

    def gp_cp(self):
        return map(
            lambda vec: vec_to_gp_pnt_on_plane(vec, self.geom_plane), self.vec_cp
        )


# Everything else should be Functional programming


def sp_segment_to_geom_line(sp_segment: SP_Segment):
    gp_cp = list(sp_segment.gp_cp())
    if isinstance(sp_segment, SP_Segment_2d):
        make_seg = GCE2d_MakeSegment(*gp_cp)
        if make_seg.IsDone():
            return make_seg.Value()
        else:
            raise ValueError(f"Failed to create line, Check point coincidendence. Coordinates are : [{gp_cp[0].X()}, {gp_cp[0].Y()}] and [{gp_cp[1].X()}, {gp_cp[1].Y()}]")
    return GC_MakeSegment(gp_cp[0], gp_cp[1]).Value()


def sp_segment_to_geom_bezier(sp_segment: SP_Segment):
    if sp_segment.point_count() == 2:
        return sp_segment_to_geom_line(sp_segment)
    gp_cp = list(sp_segment.gp_cp())
    if isinstance(sp_segment, SP_Segment_2d):
        return Geom2d_BezierCurve(gp_cp)
    return Geom_BezierCurve(gp_cp)


def sp_segment_to_geom_bspline(sp_segment: SP_Segment):
    if sp_segment.point_count() == 2:
        return sp_segment_to_geom_line(sp_segment)
    isclamped = sp_segment.is_clamped
    iscyclic = sp_segment.is_periodic
    degree = sp_segment.degree
    vec_cp = list(
        sp_segment.vec_cp
    )  # warning : it doesn't go through point projection like the other generators with gp_cp()
    weight = list(sp_segment.weight)

    if iscyclic:
        if isclamped:
            vec_cp.append(vec_cp[0])
            weight.append(weight[0])
            # vec_cp[-1] = vec_cp[0]
            # weight[-1] = weight[0]
        else:
            vec_cp.extend(vec_cp[0:degree])
            weight.extend(weight[0:degree])

    if isinstance(sp_segment, SP_Segment_2d):
        segment_point_array = vec_list_to_step_cartesian2d(vec_cp)
    else:
        segment_point_array = vec_list_to_step_cartesian(vec_cp)

    tcol_weights = float_list_to_tcolstd_H(sp_segment.weight)

    # Knot and Multiplicity
    if sp_segment.knot is not None:
        tcol_knot, tcol_mult = knot_tcol_from_att(
            sp_segment.knot, sp_segment.mult, degree, isclamped, iscyclic
        )
    else:
        raise ValueError("Missing knot on NURBS segment")

    # Create the STEP B-spline curve
    name = TCollection_HAsciiString("bspline_segment")

    step_curve = StepGeom_BSplineCurveWithKnotsAndRationalBSplineCurve()
    step_curve.Init(
        name,
        degree,
        segment_point_array,
        StepGeom_BSplineCurveForm(5),
        StepData_Logical(iscyclic),
        StepData_Logical(False),
        tcol_mult,
        tcol_knot,
        StepGeom_KnotType(1),
        tcol_weights,
    )

    # Convert to Geom
    if isinstance(sp_segment, SP_Segment_2d):
        geom = StepToGeom.MakeBSplineCurve2d_s(step_curve, StepData_Factors())
    else:
        geom = StepToGeom.MakeBSplineCurve_s(step_curve, StepData_Factors())
    if geom == None:
        raise ValueError("Failed to create BSpline geometry")
    return geom


def sp_segment_to_geom_circle_arc(sp_segment: SP_Segment):
    gp_cp = list(sp_segment.gp_cp())
    if isinstance(sp_segment, SP_Segment_2d):
        makesegment = GCE2d_MakeArcOfCircle(*gp_cp)
    else:
        makesegment = GC_MakeArcOfCircle(*gp_cp)
    return makesegment.Value()


def sp_segment_to_geom_circle(sp_segment: SP_Segment):
    gp_cp = list(sp_segment.gp_cp())
    # Circle 2D
    if isinstance(sp_segment, SP_Segment_2d):
        center = gp_cp[1]
        other = gp_cp[0]

        makesegment = GCE2d_MakeCircle(center, other)
        return makesegment.Value()

    # Circle 3D
    ## Virtual 3rd point if 2
    if sp_segment.point_count() == 2:
        p3_vec = gp_Vec(1.0, 0.0, 0.0)
    else:
        p3_vec = gp_Vec(
            gp_cp[2].X(), gp_cp[2].Y(), gp_cp[2].Z()
        )  # not directly gpVec(*vec_cp) because no projection

    center = gp_cp[1]
    center_vec = gp_Vec(center.X(), center.Y(), center.Z())
    p1_vec = gp_Vec(gp_cp[0].X(), gp_cp[0].Y(), gp_cp[0].Z())
    radius_vec = p1_vec - center_vec
    other_dir_vec = p3_vec - center_vec

    radius = radius_vec.Magnitude()

    # Circle on plane
    if isinstance(sp_segment, SP_Segment_on_plane):
        normal_dir = sp_segment.geom_plane.Pln().Axis().Direction()
        makesegment = GC_MakeCircle(gp_Ax2(center, normal_dir), radius)
    else:
        normal_dir = gp_Dir(radius_vec.Crossed(other_dir_vec))
        makesegment = GC_MakeCircle(
            gp_Ax2(center, normal_dir, gp_Dir(radius_vec)), radius
        )

    return makesegment.Value()


def sp_segment_to_geom_ellipse_arc(sp_segment: SP_Segment) -> GeomAbs.GeomAbs_CurveType:
    gp_cp = list(sp_segment.gp_cp())
    if isinstance(sp_segment, SP_Segment_2d):
        p_center = gp_cp[2]
        gp_ellipse = gp_Elips2d_from_3_points(p_center, gp_cp[1], gp_cp[3])

        makesegment = GCE2d_MakeArcOfEllipse(gp_ellipse, gp_cp[0], gp_cp[4])
        return makesegment.Value()

    p_center = gp_cp[2]
    gp_ellipse = gp_Elips_from_3_points(p_center, gp_cp[1], gp_cp[3])

    makesegment = GC_MakeArcOfEllipse(gp_ellipse, gp_cp[0], gp_cp[4], True)
    return makesegment.Value()


def sp_segment_to_geom_ellipse(sp_segment: SP_Segment):
    gp_cp = list(sp_segment.gp_cp())
    if isinstance(sp_segment, SP_Segment_2d):
        gp_elips = gp_Elips2d_from_3_points(gp_cp[1], gp_cp[0], gp_cp[2])
        makesegment = GCE2d_MakeEllipse(gp_elips)
        return makesegment.Value()

    gp_elips = gp_Elips_from_3_points(gp_cp[1], gp_cp[0], gp_cp[2])
    makesegment = GC_MakeEllipse(gp_elips)
    return makesegment.Value()


generators = {
    SP_segment_type.BEZIER: sp_segment_to_geom_bezier,
    SP_segment_type.NURBS: sp_segment_to_geom_bspline,
    SP_segment_type.CIRCLE_ARC: sp_segment_to_geom_circle_arc,
    SP_segment_type.CIRCLE: sp_segment_to_geom_circle,
    SP_segment_type.ELLIPSE_ARC: sp_segment_to_geom_ellipse_arc,
    SP_segment_type.ELLIPSE: sp_segment_to_geom_ellipse,
}


def sp_segment_to_geom_curve(sp_segment: SP_Segment) -> GeomAbs.GeomAbs_CurveType:
    generator = generators[sp_segment.type]
    return generator(sp_segment)


def geom_curve_to_topods_edge(geom):
    builder = BRepBuilderAPI_MakeEdge(geom)
    if not builder.IsDone():
        raise RuntimeError(f"Edge creation failed with error: {builder.Error()}")
    return builder.Edge()


def geom_curve_to_edge_on_surface(
    geom2d: GeomAbs.GeomAbs_CurveType, geom_surf: GeomAbs.GeomAbs_SurfaceType
):
    adapt = GeomAdaptor_Surface(geom_surf)
    builder = BRepBuilderAPI_MakeEdge(geom2d, adapt.Surface())
    if not builder.IsDone():
        raise RuntimeError(f"Edge creation failed with error: {builder.Error()}")
    return builder.Edge()
