import numpy as np
from ..common.enums import SP_segment_type
from ..common.utils import (
    gp_list_to_arrayofpnt,
    vec_list_to_gp_pnt2d,
    vec_list_to_step_cartesian2d,
    vec_list_to_step_cartesian,
    float_list_to_tcolstd_H,
    int_list_to_tcolstd_H,
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
from OCP.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCP.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Pnt2d, gp_Vec
from OCP.StepGeom import (
    StepGeom_BSplineCurveWithKnotsAndRationalBSplineCurve,
    StepGeom_BSplineCurveForm,
    StepGeom_KnotType,
)
from OCP.StepData import StepData_Logical, StepData_Factors
from OCP.StepToGeom import StepToGeom
from OCP.TCollection import TCollection_HAsciiString


def knot_tcol_from_att(knots, mults, degree, isclamped, iscyclic):
    unique_knot_length = int(sum(np.asarray(mults) > 0))  # uncompatible with mirror
    k = knots[:unique_knot_length]
    m = mults[:unique_knot_length]
    if iscyclic and not isclamped:
        dk = np.array([k[i + 1] - k[0] for i in range(int(degree))])
        k_end = dk + k[-1]
        k = np.append(k, k_end)
        m = np.append(m, m[:degree])

    tcol_knot = float_list_to_tcolstd_H(k)
    tcol_mult = int_list_to_tcolstd_H(m)
    return tcol_knot, tcol_mult


class SP_Edge_export:
    def __init__(
        self,
        cp_aligned_attrs: dict[str:list],
        seg_aligned_attrs: dict[str:float],
        is2D=False,
        geom_surf=None,
        geom_plane=None,
        single_seg=False,
    ):
        self.vec_cp = cp_aligned_attrs["CP"]
        self.weight = cp_aligned_attrs["weight"]
        self.gp_cp = []
        self.p_count = len(self.vec_cp)
        self.seg_aligned_attrs = seg_aligned_attrs
        self.cp_aligned_attrs = cp_aligned_attrs
        self.is2D = is2D
        self.geom_plane = geom_plane
        self.single_seg = single_seg
        self.knot = seg_aligned_attrs["knot"]
        self.mult = seg_aligned_attrs["mult"]

        # Generate Geom
        self.format_cp()

        self.type = self.get_type()
        self.generate_geom()

        # Make edge
        self.make_edge(geom_surf)

    def format_cp(self):
        # Create GP points
        if self.is2D:
            self.gp_cp = [gp_Pnt2d(v[0], v[1]) for v in self.vec_cp]
        else:
            if self.geom_plane != None:
                self.gp_cp = [
                    GeomAPI_ProjectPointOnSurf(
                        gp_Pnt(v[0], v[1], v[2]), self.geom_plane
                    ).Point(1)
                    for v in self.vec_cp
                ]
            else:
                self.gp_cp = [gp_Pnt(v[0], v[1], v[2]) for v in self.vec_cp]

    def get_type(self):
        if "type" in self.seg_aligned_attrs.keys():
            return SP_segment_type(self.seg_aligned_attrs["type"])
        else:
            raise ValueError("Missing segment type")

    def generate_geom(self):
        match self.type:
            case SP_segment_type.BEZIER:
                if self.p_count == 2:
                    self.line()
                else:
                    self.bezier()
            case SP_segment_type.NURBS:
                if self.p_count == 2:
                    self.line()
                else:
                    self.bspline()
            case SP_segment_type.CIRCLE_ARC:
                self.circle_arc()
            case SP_segment_type.CIRCLE:
                self.circle()
            case SP_segment_type.ELLIPSE_ARC:
                self.ellipse_arc()
            case SP_segment_type.ELLIPSE:
                self.ellipse()
            case _:
                raise ValueError("Invalid segment type")

    def line(self):
        if self.is2D:
            makesegment = GCE2d_MakeSegment(self.gp_cp[0], self.gp_cp[1])
        else:
            makesegment = GC_MakeSegment(self.gp_cp[0], self.gp_cp[1])
        self.geom = makesegment.Value()

    def bezier(self):
        if self.is2D:
            segment_point_array = vec_list_to_gp_pnt2d(self.vec_cp)
            self.geom = Geom2d_BezierCurve(segment_point_array)
        else:
            segment_point_array = gp_list_to_arrayofpnt(self.gp_cp)
            self.geom = Geom_BezierCurve(segment_point_array)

    def bspline(self):
        isclamped = self.seg_aligned_attrs["isclamped"][0] if not None else True
        iscyclic = self.seg_aligned_attrs["isperiodic"][0] if not None else False
        degree = self.seg_aligned_attrs["degree"]

        if iscyclic:
            if isclamped:
                self.vec_cp = list(self.vec_cp)
                self.weight = list(self.weight)
                self.vec_cp.append(self.vec_cp[0])
                self.weight.append(self.weight[0])
                # self.vec_cp[-1] = self.vec_cp[0]
                # self.weight[-1] = self.weight[0]
            else:
                self.vec_cp = list(self.vec_cp)
                self.weight = list(self.weight)
                self.vec_cp.extend(self.vec_cp[0:degree])
                self.weight.extend(self.weight[0:degree])

        if self.is2D:
            segment_point_array = vec_list_to_step_cartesian2d(self.vec_cp)
        else:
            segment_point_array = vec_list_to_step_cartesian(self.vec_cp)

        tcol_weights = float_list_to_tcolstd_H(self.weight)

        # Knot and Multiplicity
        if self.knot is not None:
            tcol_knot, tcol_mult = knot_tcol_from_att(
                self.knot, self.mult, degree, isclamped, iscyclic
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
        if self.is2D:
            self.geom = StepToGeom.MakeBSplineCurve2d_s(step_curve, StepData_Factors())
        else:
            self.geom = StepToGeom.MakeBSplineCurve_s(step_curve, StepData_Factors())
        if self.geom == None:
            raise ValueError("Failed to create BSpline geometry")

    def circle_arc(self):
        if self.is2D:
            makesegment = GCE2d_MakeArcOfCircle(
                self.gp_cp[0], self.gp_cp[1], self.gp_cp[2]
            )
        else:
            makesegment = GC_MakeArcOfCircle(
                self.gp_cp[0], self.gp_cp[1], self.gp_cp[2]
            )
        self.geom = makesegment.Value()

    def circle(self):

        # Circle 2D
        if self.is2D:
            center = self.gp_cp[1]
            other = self.gp_cp[0]

            makesegment = GCE2d_MakeCircle(center, other)
            self.geom = makesegment.Value()

        # Circle 3D
        else:
            # Virtual 3rd point if 2
            if self.p_count == 2:
                p3_vec = gp_Vec(1.0, 0.0, 0.0)
            else:
                p3_vec = gp_Vec(self.gp_cp[2].X(), self.gp_cp[2].Y(), self.gp_cp[2].Z())

            center = self.gp_cp[1]
            center_vec = gp_Vec(center.X(), center.Y(), center.Z())
            p1_vec = gp_Vec(self.gp_cp[0].X(), self.gp_cp[0].Y(), self.gp_cp[0].Z())
            radius_vec = p1_vec - center_vec
            other_dir_vec = p3_vec - center_vec

            radius = radius_vec.Magnitude()

            # Circle on plane
            if self.geom_plane != None:
                normal_dir = self.geom_plane.Pln().Axis().Direction()
                makesegment = GC_MakeCircle(gp_Ax2(center, normal_dir), radius)
            else:
                normal_dir = gp_Dir(radius_vec.Crossed(other_dir_vec))
                makesegment = GC_MakeCircle(
                    gp_Ax2(center, normal_dir, gp_Dir(radius_vec)), radius
                )

            self.geom = makesegment.Value()

    def ellipse_arc(self):
        if self.is2D:
            p_center = self.gp_cp[2]
            gp_ellipse = gp_Elips2d_from_3_points(
                p_center, self.gp_cp[1], self.gp_cp[3]
            )

            makesegment = GCE2d_MakeArcOfEllipse(
                gp_ellipse, self.gp_cp[0], self.gp_cp[4]
            )
            self.geom = makesegment.Value()
        else:
            p_center = self.gp_cp[2]
            gp_ellipse = gp_Elips_from_3_points(p_center, self.gp_cp[1], self.gp_cp[3])

            makesegment = GC_MakeArcOfEllipse(
                gp_ellipse, self.gp_cp[0], self.gp_cp[4], True
            )
            self.geom = makesegment.Value()

    def ellipse(self):
        if self.is2D:
            gp_elips = gp_Elips2d_from_3_points(
                self.gp_cp[1], self.gp_cp[0], self.gp_cp[2]
            )
            makesegment = GCE2d_MakeEllipse(gp_elips)
            self.geom = makesegment.Value()
        else:
            gp_elips = gp_Elips_from_3_points(
                self.gp_cp[1], self.gp_cp[0], self.gp_cp[2]
            )
            makesegment = GC_MakeEllipse(gp_elips)
            self.geom = makesegment.Value()

    def make_edge(self, geom_surf):
        if geom_surf == None:
            builder = BRepBuilderAPI_MakeEdge(self.geom)
            if not builder.IsDone():
                raise RuntimeError(
                    f"Edge creation failed with error: {builder.Error()}"
                )
            self.topods_edge = builder.Edge()
        else:  # UV space
            adapt = GeomAdaptor_Surface(geom_surf)
            builder = BRepBuilderAPI_MakeEdge(self.geom, adapt.Surface())
            if not builder.IsDone():
                raise RuntimeError(
                    f"Edge creation failed with error: {builder.Error()}"
                )
            self.topods_edge = builder.Edge()
