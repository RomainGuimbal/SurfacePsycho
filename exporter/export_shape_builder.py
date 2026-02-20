import bpy
import numpy as np
import math
import warnings
from mathutils import Vector, Matrix
from collections import Counter


from ..common.enums import SP_obj_type, SP_segment_type
from ..common.utils import (
    read_attribute_by_name,
    dict_to_list_missing_index_filled,
    split_by_index_dict,
    gp_list_to_arrayofpnt,
    vec_list_to_gp_pnt2d,
    vec_list_to_step_cartesian2d,
    vec_list_to_step_cartesian,
    float_list_to_tcolstd_H,
    int_list_to_tcolstd_H,
    rebound_UV,
    vec_grid_to_step_cartesian,
    float_list_to_tcolstd_H_2d,
    sp_type_of_object,
    split_by_index,
    blender_matrix_to_gp_trsf,
    shape_list_to_compound,
    shells_to_solids,
)
from ..common.compound_utils import (
    convert_compound_to_patches,
)
from .export_ellipse import gp_Elips_from_3_points, gp_Elips2d_from_3_points

from OCP.TColgp import TColgp_Array2OfPnt
from OCP.TColStd import (
    TColStd_HArray1OfReal,
    TColStd_HArray1OfInteger,
)

from OCP.BRepBuilderAPI import (
    BRepBuilderAPI_GTransform,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_Sewing,
    BRepBuilderAPI_Transform,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeEdge,
)
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
from OCP.Geom import (
    Geom_BezierSurface,
    Geom_Plane,
    Geom_BezierCurve,
    Geom_ToroidalSurface,
    Geom_ConicalSurface,
    Geom_CylindricalSurface,
    Geom_SphericalSurface,
    Geom_SurfaceOfLinearExtrusion,
    Geom_SurfaceOfRevolution,
    Geom_TrimmedCurve,
)
from OCP.Geom2d import Geom2d_BezierCurve
from OCP.GeomAdaptor import GeomAdaptor_Surface
from OCP.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCP.gp import (
    gp_Pnt,
    gp_Dir,
    gp_Pln,
    gp_Trsf,
    gp_Ax1,
    gp_Ax2,
    gp_Ax3,
    gp_Pnt2d,
    gp_Vec,
    gp_GTrsf,
    gp_Mat,
)
from OCP.ShapeFix import ShapeFix_Face
from OCP.TColgp import TColgp_Array2OfPnt
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import (
    TopoDS,
    TopoDS_Compound,
)

from OCP.StepGeom import (
    StepGeom_BSplineCurveWithKnotsAndRationalBSplineCurve,
    StepGeom_BSplineCurveForm,
    StepGeom_KnotType,
    StepGeom_BSplineSurfaceForm,
    StepGeom_BSplineSurfaceWithKnotsAndRationalBSplineSurface,
)
from OCP.StepData import StepData_Logical, StepData_Factors
from OCP.StepToGeom import StepToGeom
from OCP.TCollection import TCollection_HAsciiString


##############################
##    Converter classes     ##
##############################

def knot_tcol_from_att(knots, mults, degree, isclamped, iscyclic):
    unique_knot_length = sum(np.asarray(mults) > 0) # uncompatible with mirror
    k = knots[:unique_knot_length]
    m = mults[:unique_knot_length]
    if iscyclic and not isclamped:
        dk = np.array([k[i + 1] - k[0] for i in range(degree)])
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
            tcol_knot, tcol_mult = knot_tcol_from_att(self.knot, self.mult, degree, isclamped, iscyclic)
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
            self.topods_edge = BRepBuilderAPI_MakeEdge(self.geom).Edge()
        else:  # 2D
            adapt = GeomAdaptor_Surface(geom_surf)
            self.topods_edge = BRepBuilderAPI_MakeEdge(
                self.geom, adapt.Surface()
            ).Edge()


def get_patch_knot_and_mult(ob,  degree_u, degree_v, isclamped_u, isclamped_v, iscyclic_u, iscyclic_v):
    # U
    umult_att = read_attribute_by_name(ob, "Multiplicity U")
    try:
        u_length = sum(np.asarray(umult_att) > 0)  # uncompatible with mirror
    except KeyError: # weird
        u_length = int(sum(np.asarray(umult_att) > 0))
    uknots_att = list(read_attribute_by_name(ob, "Knot U", u_length))
    uknot, umult = knot_tcol_from_att(uknots_att, umult_att, degree_u, isclamped_u, iscyclic_u)
    
    # V
    vmult_att = read_attribute_by_name(ob, "Multiplicity V")
    try:
        v_length = sum(np.asarray(vmult_att) > 0)
    except Exception:
        v_length = int(sum(np.asarray(vmult_att) > 0))
    vknots_att = list(read_attribute_by_name(ob, "Knot V", v_length))
    vknot, vmult = knot_tcol_from_att(vknots_att, vmult_att, degree_v, isclamped_v, iscyclic_v)

    return uknot, vknot, umult, vmult


class SP_Wire_export:
    def __init__(
        self,
        cp_aligned_attrs: dict,
        seg_aligned_attrs: dict,
        geom_surf=None,
        geom_plane=None,
        is2D=False,
    ):
        # Get attributes
        ## CP aligned
        self.CP = [Vector(v) for v in cp_aligned_attrs["CP"]]
        self.p_count = len(cp_aligned_attrs["CP"])
        if "weight" in list(cp_aligned_attrs.keys()):
            self.weight_attr = cp_aligned_attrs["weight"]
        else:
            self.weight_attr = [1.0] * self.p_count

        ## Wire aligned
        self.is2D = is2D
        self.geom_surf = geom_surf
        self.geom_plane = geom_plane

        ## Segment aligned
        self.segs_p_counts = seg_aligned_attrs["p_count"]
        self.seg_count = len(self.segs_p_counts)
        self.segs_type_seg_aligned = seg_aligned_attrs["type"]
        self.segs_degrees = seg_aligned_attrs["degree"]
        self.isclamped_per_seg = seg_aligned_attrs["isclamped"]
        self.isperiodic_per_seg = seg_aligned_attrs["isperiodic"]
        self.knot = seg_aligned_attrs["knot"]
        self.mult = seg_aligned_attrs["mult"]

        # Domains :
        ## Is closed : per wire
        ## Is periodic/cyclic : per segment

        # Is closed
        self.isclosed = sum([s - 1 for s in self.segs_p_counts]) == len(self.CP) or (
            sum(self.isperiodic_per_seg) > 0
        )

    def split_cp_aligned_attr_per_seg(self, attr: list) -> list[list]:
        attr = list(attr)
        split_attr = []
        inf = 0
        sup = self.segs_p_counts[0]
        for i in range(self.seg_count):
            # for last segment but not only segment
            if i == self.seg_count - 1 and self.isclosed and self.seg_count > 1:
                split_attr.append(attr[inf : len(self.CP)] + [attr[0]])
            else:
                split_attr.append(attr[inf:sup])
                if i < self.seg_count - 1:  # Skip increment in last loop
                    inf = sup - 1
                    sup = inf + self.segs_p_counts[i + 1]
        return split_attr

    def get_topods_wire(self):
        # Split because not needed with svg. Can be judged unnecessary

        # Split attrs per segment
        vec_cp_per_seg = self.split_cp_aligned_attr_per_seg(self.CP)
        weight = self.split_cp_aligned_attr_per_seg(self.weight_attr)
        edges_degrees = self.segs_degrees

        # Make Edges
        edges_list = [
            SP_Edge_export(
                {"CP": vec_cp_per_seg[i], "weight": weight[i]},
                {
                    "degree": edges_degrees[i],
                    "isclamped": self.isclamped_per_seg,
                    "isperiodic": self.isperiodic_per_seg,
                    "type": self.segs_type_seg_aligned[i],
                    "knot": self.knot[i] if len(self.knot) > i else None,
                    "mult": self.mult[i] if len(self.mult) > i else None,
                },
                geom_plane=self.geom_plane,
                geom_surf=self.geom_surf,
                single_seg=self.seg_count == 1,
                is2D=self.is2D,
            ).topods_edge
            for i in range(self.seg_count)
        ]

        # Make contour
        makeWire = BRepBuilderAPI_MakeWire()
        for e in edges_list:
            makeWire.Add(TopoDS.Edge_s(e))
        wire = makeWire.Wire()
        self.topods_wire = wire
        return wire

    def mirror_CP(self, axis, object_matrix, mirror_obj_matrix=None):
        if mirror_obj_matrix == None:
            mirror_obj_matrix = object_matrix
        # Example :
        # w_M_o @ p_o = p_w : matrix transform of p in object coords to p in world coords (w)
        match axis:
            # the initial mirror matrix is either expressed in object coords (o) or in mirror object coords (t)
            case "X":
                m_M_o_or_t = Matrix(
                    ((-1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
                )
            case "Y":
                m_M_o_or_t = Matrix(
                    ((1, 0, 0, 0), (0, -1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
                )
            case "Z":
                m_M_o_or_t = Matrix(
                    ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, -1, 0), (0, 0, 0, 1))
                )

        o_or_t_M_w = mirror_obj_matrix.inverted()  # t_M_w or o_M_w
        m_M_w = m_M_o_or_t @ o_or_t_M_w

        self.CP = [o_or_t_M_w.inverted() @ (m_M_w @ pw) for pw in self.CP]

    def scale(self, scale_factor):
        self.CP = [v * scale_factor for v in self.CP]

    def offset(self, offset: Vector):
        self.CP = [v + offset for v in self.CP]


class SP_Contour_export:
    def __init__(
        self,
        ob,
        cp_attr_name,
        p_count_attr_name,
        isclamped_attr_name,
        isperiodic_attr_name,
        scale=1,
        is2D=False,
        geom_surf=None,
        geom_plane=None,
        curr_bounds=None,
        new_bounds=None,
    ):
        # Check if trimmed
        try:
            self.segs_p_counts = read_attribute_by_name(ob, p_count_attr_name)
            self.wire_index = read_attribute_by_name(ob, "Wire")
            self.seg_count_per_wire = read_attribute_by_name(ob, "seg_count_per_wire")
            self.has_wire = True
        # No trim
        except Exception:
            self.has_wire = False

        # Make wire
        if self.has_wire:
            self.compute_total_p_count()
            self.compute_segment_count()

            # crop wire_index
            self.wire_index = self.wire_index[: self.total_p_count]
            self.p_count_per_wire = Counter(self.wire_index)

            # crop seg_count_per_wire
            self.wire_index_order = list(dict.fromkeys(self.wire_index))
            self.wir_count = len(self.wire_index_order)
            self.seg_count_per_wire = self.seg_count_per_wire[: self.wir_count]

            # crop segs_p_counts
            self.segs_p_counts = self.segs_p_counts[: self.segment_count]
            self.segs_p_counts_per_wire = self.split_seg_attr_per_wire(
                self.segs_p_counts
            )

            # Get CP aligned attrs
            ## CP
            points = read_attribute_by_name(ob, cp_attr_name, self.total_p_count)
            if type(scale) == tuple:
                points[:, 0] *= scale[0]
                points[:, 1] *= scale[1]
            else:
                points *= scale

            if curr_bounds is not None and new_bounds is not None:
                points = rebound_UV(points, curr_bounds, new_bounds)

            if is2D:
                points = [Vector((p[0], p[1], 0.0)) for p in points]
            points_per_wire = self.split_cp_attr_per_wire(points[: self.total_p_count])

            ## Weight
            try:
                weight_attr = read_attribute_by_name(ob, "Weight", self.total_p_count)
            except KeyError:
                weight_attr = [1.0] * self.total_p_count
            weight_per_wire = self.split_cp_attr_per_wire(
                weight_attr[: self.total_p_count]
            )

            # Get seg aligned attrs
            ## Type
            try:
                type_att = read_attribute_by_name(ob, "Type", self.segment_count)
            except KeyError:
                type_att = [0] * self.segment_count
            type_att_per_wire = self.split_seg_attr_per_wire(type_att)

            ## Degree
            try:
                try:
                    try:
                        segs_degrees = read_attribute_by_name(
                            ob, "Contour Degree", self.segment_count
                        )
                    except KeyError:
                        segs_degrees = read_attribute_by_name(
                            ob, "Degree", self.segment_count
                        )
                except KeyError:
                    segs_degrees = read_attribute_by_name(
                        ob, "Contour Order", self.segment_count
                    )
            except KeyError:
                segs_degrees = [c - 1 for c in self.segs_p_counts]
            segs_degrees_per_wire = self.split_seg_attr_per_wire(segs_degrees)

            ## IsClamped
            try:
                isclamped = read_attribute_by_name(
                    ob, isclamped_attr_name, self.segment_count
                )
            except KeyError:
                isclamped = [True] * self.segment_count
            isclamped_per_wire = self.split_seg_attr_per_wire(isclamped)

            ## IsPeriodic
            try:
                isperiodic = read_attribute_by_name(
                    ob, isperiodic_attr_name, self.segment_count
                )
            except KeyError:
                isperiodic = [False] * self.segment_count
            isperiodic_per_wire = self.split_seg_attr_per_wire(isperiodic)

            ## Knot
            knot = read_attribute_by_name(ob, "Knot")
            mult = read_attribute_by_name(ob, "Multiplicity")
            knot_segment = list(read_attribute_by_name(ob, "knot_segment"))
            knot_per_seg = dict_to_list_missing_index_filled(
                split_by_index_dict(knot_segment, knot), self.segment_count
            )
            mult_per_seg = dict_to_list_missing_index_filled(
                split_by_index_dict(knot_segment, mult), self.segment_count
            )
            knot_per_wire = self.split_seg_attr_per_wire(knot_per_seg)
            mult_per_wire = self.split_seg_attr_per_wire(mult_per_seg)

            # Build wires
            self.wires_dict = {}
            for w in set(self.wire_index):
                self.wires_dict[w] = SP_Wire_export(
                    {"CP": points_per_wire[w], "weight": weight_per_wire[w]},
                    {
                        "p_count": self.segs_p_counts_per_wire[w],
                        "degree": segs_degrees_per_wire[w],
                        "isclamped": isclamped_per_wire[w],
                        "isperiodic": isperiodic_per_wire[w],
                        "type": type_att_per_wire[w],
                        "knot": knot_per_wire[w],
                        "mult": mult_per_wire[w],
                    },
                    geom_surf=geom_surf,
                    geom_plane=geom_plane,
                    is2D=is2D,
                )

    def split_cp_attr_per_wire(self, attr):
        # Prepare dict
        attr_dict_per_wire = {}
        for w in set(self.wire_index):
            attr_dict_per_wire[w] = []

        # Fill dict
        for i, a in enumerate(attr[: self.total_p_count]):
            attr_dict_per_wire[self.wire_index[i]].append(a)

        return attr_dict_per_wire

    def split_seg_attr_per_wire(self, attr):
        attr_dict_per_wire = {}
        start = 0
        end = 0
        for i, w in enumerate(self.wire_index_order):
            end += self.seg_count_per_wire[i]
            attr_dict_per_wire[w] = attr[start:end]
            start = end

        return attr_dict_per_wire

    def get_topods_wires(self):
        wires = self.wires_dict
        outer_wire = None
        inner_wires = []
        for k in wires.keys():
            if k > 0:
                inner_wires.append(wires[k].get_topods_wire())
            elif k < 0:
                outer_wire = wires[k].get_topods_wire()
        if outer_wire == None:
            raise Exception("No outer wire found")

        return outer_wire, inner_wires

    def compute_total_p_count(self):
        # not sum because mirrors...
        self.total_p_count = 0
        for i, wi in enumerate(self.wire_index):
            if wi == 0:
                break
            self.total_p_count += 1

    def compute_segment_count(self):
        # not sum because mirrors...
        self.segment_count = 0
        for p in self.segs_p_counts:
            if p > 0:
                self.segment_count += 1
            else:
                break


##############################
##  Brep from SP entities   ##
##############################


def geom_to_topods_face(geom_surf=None, outer_wire=None, inner_wires=[]):
    # Make face
    if geom_surf != None:
        if outer_wire == None:
            makeface = BRepBuilderAPI_MakeFace(geom_surf, 1e-6)
            return makeface.Face()
        else:
            makeface = BRepBuilderAPI_MakeFace(geom_surf, outer_wire, False)  # ,1e-6)
    else:  # Flat face
        makeface = BRepBuilderAPI_MakeFace(outer_wire, True)

    # Add inner wires (holes)
    for inner_wire in inner_wires:
        makeface.Add(inner_wire)

    # Build the face
    makeface.Build()

    # makeface.Add(trim_wire)#.Reversed())
    face = makeface.Face()
    fix = ShapeFix_Face(face)
    fix.Perform()

    return fix.Face()


def bezier_face_to_topods(ob, scale=1000):
    u_count = int(ob.data.attributes["CP_count"].data[0].value)
    v_count = int(ob.data.attributes["CP_count"].data[1].value)
    points = read_attribute_by_name(ob, "CP_any_order_surf", u_count * v_count)
    points *= scale

    controlPoints = TColgp_Array2OfPnt(1, u_count, 1, v_count)
    for i in range(v_count):
        for j in range(u_count):
            id = u_count * i + j
            controlPoints.SetValue(
                j + 1, i + 1, gp_Pnt(points[id][0], points[id][1], points[id][2])
            )

    geom_surf = Geom_BezierSurface(controlPoints)

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
    )

    if not contour.has_wire:
        return geom_to_topods_face(geom_surf)
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def NURBS_face_to_topods(ob, scale=1000):
    # Get attributes
    u_count, v_count = read_attribute_by_name(ob, "CP_count", 2)
    points = read_attribute_by_name(ob, "CP_NURBS_surf", u_count * v_count)
    points *= scale
    degree_u, degree_v = read_attribute_by_name(ob, "Degrees", 2)
    
    try:
        isclamped_u, isclamped_v = read_attribute_by_name(ob, "IsClamped", 2)
    except KeyError:
        isclamped_u, isclamped_v = True, True

    try:
        isperiodic_u, isperiodic_v = read_attribute_by_name(ob, "IsPeriodic", 2)
    except KeyError:
        isperiodic_u, isperiodic_v = False, False

    try:
        weigths_att = read_attribute_by_name(ob, "Weights", u_count * v_count)
    except KeyError:
        weigths_att = np.ones(u_count * v_count, dtype=float)

    points = points.reshape(v_count, u_count, 3).transpose(1, 0, 2)
    weigths_att = weigths_att.reshape(v_count, u_count).transpose()

    # Wrap control points
    if isperiodic_u:
        if isclamped_u:
            points = np.append(points, points[0:1, :, :], axis=0)
            weigths_att = np.append(weigths_att, weigths_att[0:1, :], axis=0)
            u_count += 1
        else:
            points = np.append(points, points[0:degree_u, :, :], axis=0)
            weigths_att = np.append(weigths_att, weigths_att[0:degree_u, :], axis=0)
            u_count += degree_u
    if isperiodic_v:
        if isclamped_v:
            points = np.append(points, points[:, 0:1, :], axis=1)
            weigths_att = np.append(weigths_att, weigths_att[:, 0:1], axis=1)
            v_count += 1
        else:
            points = np.append(points, points[:, 0:degree_v, :], axis=1)
            weigths_att = np.append(weigths_att, weigths_att[:, 0:degree_v], axis=1)
            v_count += degree_v

    # Knots and Multiplicities
    uknots, vknots, umult, vmult = get_patch_knot_and_mult(ob, degree_u, degree_v, isclamped_u, isclamped_v, isperiodic_u, isperiodic_v)

    # Poles grid
    poles = vec_grid_to_step_cartesian(list(points))

    # Weigths
    weigths = float_list_to_tcolstd_H_2d(list(weigths_att))

    # Create STEP B-spline surface
    name = TCollection_HAsciiString("bspline_surface")
    step_surf = StepGeom_BSplineSurfaceWithKnotsAndRationalBSplineSurface()
    step_surf.Init(
        name,
        degree_u,
        degree_v,
        poles,
        StepGeom_BSplineSurfaceForm(10),
        StepData_Logical(isperiodic_u),
        StepData_Logical(isperiodic_v),
        StepData_Logical(False),
        umult,
        vmult,
        uknots,
        vknots,
        StepGeom_KnotType(1),
        weigths,
    )

    geom_surf = StepToGeom.MakeBSplineSurface_s(step_surf, StepData_Factors())
    if geom_surf == None:
        raise ValueError("Failed to create BSpline surface geometry")

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
    )
    if not contour.has_wire:
        face = geom_to_topods_face(geom_surf)
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def cone_face_to_topods(ob, scale=1000):
    # Get attr
    origin, dir1, dir2 = read_attribute_by_name(ob, "axis3_cone", 3)
    semi_angle, radius = read_attribute_by_name(ob, "angle_radius", 2)
    radius *= scale
    origin *= scale

    # Create geom
    axis3 = gp_Ax3(
        gp_Pnt(*origin),
        gp_Dir(*dir1),
        gp_Dir(*dir2),
    )
    geom_surf = Geom_ConicalSurface(axis3, semi_angle, 0.0)

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
        scale=(1, 2),
    )

    # Create topods face
    if not contour.has_wire:
        face = geom_to_topods_face(geom_surf)
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def sphere_face_to_topods(ob, scale=1000):
    # Get attr
    origin, dir1, dir2 = read_attribute_by_name(ob, "axis3_sphere", 3)
    radius = float(ob.data.attributes["radius"].data[0].value)

    # Create geom
    axis3 = gp_Ax3(
        gp_Pnt(*(origin * scale)),
        gp_Dir(dir1[0], dir1[1], dir1[2]),
        gp_Dir(dir2[0], dir2[1], dir2[2]),
    )
    geom_surf = Geom_SphericalSurface(axis3, radius * scale)

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
    )

    # Create topods face
    if not contour.has_wire:
        face = geom_to_topods_face(geom_surf)
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def torus_face_to_topods(ob, scale=1000):
    # Get attr
    origin, dir1, dir2 = read_attribute_by_name(ob, "axis3_torus", 3)
    radius_major, radius_minor = read_attribute_by_name(ob, "radius", 2)

    # Create geom
    axis3 = gp_Ax3(
        gp_Pnt(origin[0] * scale, origin[1] * scale, origin[2] * scale),
        gp_Dir(dir1[0], dir1[1], dir1[2]),
        gp_Dir(dir2[0], dir2[1], dir2[2]),
    )
    geom_surf = Geom_ToroidalSurface(axis3, radius_major * scale, radius_minor * scale)

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
    )

    # Create topods face
    if not contour.has_wire:
        face = geom_to_topods_face(geom_surf)
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def cylinder_face_to_topods(ob, scale=1000):
    # Get attr
    origin, dir1, dir2 = read_attribute_by_name(ob, "axis3_cylinder", 3)
    radius, length = read_attribute_by_name(ob, "radius_length", 2)

    # Create geom
    axis3 = gp_Ax3(
        gp_Pnt(*(origin * scale)),
        gp_Dir(*dir1),
        gp_Dir(*dir2),
    )
    geom_surf = Geom_CylindricalSurface(axis3, radius * scale)

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
        scale=(1, length * scale),
    )

    # Create topods face
    if not contour.has_wire:
        face = BRepBuilderAPI_MakeFace(
            geom_surf, 0, 2 * math.pi, 0, length * scale, 1e-6
        ).Face()
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def revolution_face_to_topods(ob, scale=1000):
    # Get attr
    origin, dir1 = read_attribute_by_name(ob, "axis1_revolution", 2)
    p_count = read_attribute_by_name(ob, "p_count_revolution", 1)[0]
    segment_CP = read_attribute_by_name(ob, "CP_revolution", p_count)
    segment_CP *= scale
    try:
        weight = read_attribute_by_name(ob, "weight_revolution", p_count)
    except KeyError:
        weight = [1.0] * p_count
    type = read_attribute_by_name(ob, "type_revolution", 1)[0]
    degree = read_attribute_by_name(ob, "degree_revolution", 1)[0]
    is_clamped, is_periodic = read_attribute_by_name(
        ob, "clamped_periodic_revolution", 2
    )

    # Get knot
    try:
        mult = read_attribute_by_name(ob, "Multiplicity")
        knot_length = int(sum(np.asarray(mult) > 0))
        knot = read_attribute_by_name(ob, "Knot", knot_length)
        mult = mult[:knot_length]
    except KeyError:
        knot = []
        mult = []

    # Create geom
    geom_segment = SP_Edge_export(
        {"CP": segment_CP, "weight": weight},
        {
            "degree": degree,
            "isclamped": [is_clamped],
            "isperiodic": [is_periodic],
            "type": type,
            "knot": knot,
            "mult": mult,
        },
        single_seg=True,
        is2D=False,
    ).geom

    # Create geom
    axis1 = gp_Ax1(
        gp_Pnt(origin[0] * scale, origin[1] * scale, origin[2] * scale),
        gp_Dir(dir1[0], dir1[1], dir1[2]),
    )
    geom_surf = Geom_SurfaceOfRevolution(geom_segment, axis1)

    # Get bounds
    v_min = 0.0
    v_max = 1.0
    if isinstance(geom_segment, Geom_TrimmedCurve):
        v_min = geom_segment.FirstParameter()
        v_max = geom_segment.LastParameter()

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
        curr_bounds=(None, None, 0.0, 1.0),
        new_bounds=(None, None, v_min, v_max),
    )

    # Create topods face
    if not contour.has_wire:
        face = geom_to_topods_face(geom_surf)
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def extrusion_face_to_topods(ob, scale=1000):
    # Get attr
    dir_att = read_attribute_by_name(ob, "dir_extrusion", 1)[0]
    p_count = read_attribute_by_name(ob, "p_count_extrusion", 1)[0]
    segment_CP = read_attribute_by_name(ob, "CP_extrusion", p_count)
    segment_CP *= scale
    weight = read_attribute_by_name(ob, "weight_extrusion", p_count)
    type = read_attribute_by_name(ob, "type_extrusion", 1)[0]
    degree = read_attribute_by_name(ob, "degree_extrusion", 1)[0]
    is_clamped, is_periodic = read_attribute_by_name(
        ob, "clamped_periodic_extrusion", 2
    )

    length = Vector(dir_att).length * scale

    try:
        # Get knot
        mult = read_attribute_by_name(ob, "Multiplicity")
        knot_length = int(sum(np.asarray(mult) > 0))
        knot = read_attribute_by_name(ob, "Knot", knot_length)
        mult = mult[:knot_length]
    except KeyError:
        knot = []
        mult = []

    geom_segment = SP_Edge_export(
        {"CP": segment_CP, "weight": weight},
        {
            "degree": degree,
            "isclamped": [is_clamped],
            "isperiodic": [is_periodic],
            "type": type,
            "knot": knot,
            "mult": mult,
        },
        single_seg=True,
        is2D=False,
    ).geom

    # Create geom
    dir = gp_Dir(*dir_att)
    geom_surf = Geom_SurfaceOfLinearExtrusion(geom_segment, dir)

    # Build trim contour
    contour = SP_Contour_export(
        ob,
        "CP_trim_contour_UV",
        "CP_count_trim_contour_UV",
        "IsClamped_trim_contour",
        "IsPeriodic_trim_contour",
        is2D=True,
        geom_surf=geom_surf,
        curr_bounds=(None, None, 0.0, 1.0),
        new_bounds=(None, None, 0.0, length),
    )

    # Create topods face
    if not contour.has_wire:
        u_min, u_max = geom_segment.FirstParameter(), geom_segment.LastParameter()
        v_min, v_max = 0.0, length  # Extrusion length
        face = BRepBuilderAPI_MakeFace(
            geom_surf, u_min, u_max, v_min, v_max, 1e-6
        ).Face()
    else:
        outer_wire, inner_wires = contour.get_topods_wires()
        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def curve_to_topods(ob, scale=1000):
    # Get point count attr
    segs_p_counts = read_attribute_by_name(ob, "CP_count")

    # get total_p_count and segment_count
    total_p_count, segment_count = 1, 0
    for p in segs_p_counts:
        if p > 1:
            total_p_count += p - 1
            segment_count += 1
        else:
            break
    # crop segs_p_counts
    segs_p_counts = segs_p_counts[:segment_count]

    # is closed
    is_closed = read_attribute_by_name(ob, "closed", 1)[0]

    # One point less if closed
    total_p_count -= is_closed and segment_count > 1

    # is clamped
    is_clamped = read_attribute_by_name(ob, "IsClamped", 1)[0]

    # is periodic
    is_periodic = read_attribute_by_name(ob, "IsPeriodic", 1)[0]

    # Type
    try:
        type_att = read_attribute_by_name(ob, "Type", segment_count)
    except KeyError:
        type_att = [0] * segment_count

    # Degree
    try:
        segs_degrees = read_attribute_by_name(ob, "Degree", segment_count)
    except KeyError:
        segs_degrees = [0] * segment_count

    # Get CP position attr
    points = read_attribute_by_name(ob, "CP_curve", total_p_count)
    points *= scale

    # Weight
    try:
        weight_attr = read_attribute_by_name(ob, "Weight", total_p_count)
    except KeyError:
        weight_attr = [1.0] * total_p_count

    # Knots
    mult = read_attribute_by_name(ob, "Multiplicity")
    knot = read_attribute_by_name(ob, "Knot")
    knot_segment = list(read_attribute_by_name(ob, "knot_segment"))
    knot_per_seg = split_by_index(knot_segment, knot)
    mult_per_seg = split_by_index(knot_segment, mult)

    # Build wire
    wire = SP_Wire_export(
        {"CP": points, "weight": weight_attr},
        {
            "p_count": segs_p_counts,
            "degree": segs_degrees,
            "isperiodic": [is_periodic] * segment_count,
            "isclamped": [is_clamped] * segment_count,
            "type": type_att,
            "knot": knot_per_seg,
            "mult": mult_per_seg,
        },
        is2D=False,
    )
    topods_wire = wire.get_topods_wire()

    return topods_wire


def flat_patch_to_topods(ob, scale=1000):
    # Get point count attr
    # Orient and offset
    loc, rot, _ = ob.matrix_world.decompose()
    try:
        offset = read_attribute_by_name(ob, "planar_offset", 1)[0]
        orient = read_attribute_by_name(ob, "planar_orient", 1)[0]
    except KeyError:
        offset = [0, 0, 0]
        orient = [0, 0, 1]
    loc += rot @ Vector(offset)
    loc *= scale
    pl_normal = rot @ Vector(orient)
    pl_normal_dir = gp_Dir(pl_normal.x, pl_normal.y, pl_normal.z)
    pl = gp_Pln(gp_Pnt(loc.x, loc.y, loc.z), pl_normal_dir)
    geom_pl = Geom_Plane(pl)

    # Build Contour
    contour = SP_Contour_export(
        ob,
        "CP_planar",
        "CP_count",
        "IsClamped",
        "IsPeriodic",
        scale,
        geom_plane=geom_pl,
        is2D=False,
    )

    # Get occ wires
    outer_wire, inner_wires = contour.get_topods_wires()

    face = geom_to_topods_face(None, outer_wire, inner_wires)
    return face


def empty_to_topods(o, scale=1000):
    # Orient and offset
    gp_trsf = blender_matrix_to_gp_trsf(o.matrix_world, scale)
    gp_pln = gp_Pln(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)).Transformed(gp_trsf)
    # gp_pnt = TopoDS_Vertex(gp_Pnt(0,0,0).Transformed(gp_trsf)) vertices cannot be exported :c
    topods_plane = geom_to_topods_face(Geom_Plane(gp_pln))
    return topods_plane


def mirror_topods_shape(o, shape, scale=1000):
    shape_list = [shape]

    loc, rot, _ = o.matrix_world.decompose()

    for m in o.modifiers:
        if m.type == "MIRROR" and m.show_viewport:

            # Get mirror offset
            if m.mirror_object == None:
                mirror_offset = loc * scale
            else:
                loc, rot, _ = m.mirror_object.matrix_world.decompose()
                mirror_offset = loc * scale

            # Fill configurations array
            configurations = [False] * 7

            x = m.use_axis[0]
            y = m.use_axis[1]
            z = m.use_axis[2]

            configurations[0] = x
            configurations[1] = y
            configurations[2] = z
            configurations[3] = x and y and z
            configurations[4] = y and z
            configurations[5] = x and z
            configurations[6] = x and y

            xscales = [1, 0, 0, 1, 0, 1, 1]
            yscales = [0, 1, 0, 1, 1, 0, 1]
            zscales = [0, 0, 1, 1, 1, 1, 0]
            symtype = [x + y + z for x, y, z in zip(xscales, yscales, zscales)]

            # Loop through configurations
            for i in range(7):  # 7 = 8 mirror configs -1 original config
                if configurations[i]:
                    # Create transforms

                    # planar symmetry
                    if symtype[i] == 1:
                        base = rot @ (Vector([xscales[i], yscales[i], zscales[i]]))
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(
                            gp_Ax2(
                                gp_Pnt(
                                    mirror_offset[0], mirror_offset[1], mirror_offset[2]
                                ),
                                gp_Dir(base.x, base.y, base.z),
                            )
                        )
                    # axis symmetry
                    elif symtype[i] == 2:
                        base = rot @ (
                            Vector(
                                [
                                    xscales[i] - 1,
                                    abs(yscales[i] - 1),
                                    abs(zscales[i] - 1),
                                ]
                            )
                        )
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(
                            gp_Ax1(
                                gp_Pnt(
                                    mirror_offset[0], mirror_offset[1], mirror_offset[2]
                                ),
                                gp_Dir(base.x, base.y, base.z),
                            )
                        )

                    # centric symmetry
                    else:
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(
                            gp_Pnt(mirror_offset[0], mirror_offset[1], mirror_offset[2])
                        )

                    for s in range(len(shape_list)):
                        sh = BRepBuilderAPI_Transform(shape_list[s], atrsf).Shape()
                        shape_list.append(sh)

    return shape_list


# not a true hierarchy. too complex for now
class ShapeHierarchy_export:
    def __init__(self, context, use_selection, scale, sew, sew_tolerance):
        self.context = context
        self.use_selection = use_selection
        self.scale = scale
        self.sew = sew
        self.sew_tolerance = sew_tolerance
        self.depsgraph = context.evaluated_depsgraph_get()

        objs, shapes, empties, instances, compounds = self.create_shape_hierarchy(
            context.scene.collection
        )
        self.shapes = shapes
        self.instances = instances
        self.empties = empties
        self.compounds = compounds

        # objs is used only for instancing
        self.obj_shapes = {}  # {obj: shape}
        for i, o in enumerate(objs):
            self.obj_shapes[o] = shapes[i]

    def create_shape_hierarchy(self, parent):
        objs, shapes, empties, instances, compounds = [], [], [], [], []

        for child in parent.children:
            o, s, e, i, c = self.create_shape_hierarchy(child)
            objs.extend(o)
            shapes.extend(s)
            empties.extend(e)
            instances.extend(i)
            compounds.extend(c)

        for o in parent.objects:
            if ((not self.use_selection) or (o in self.context.selected_objects)) and (
                not o.hide_viewport
            ):
                sp_type = sp_type_of_object(o)
                match sp_type:
                    case None:
                        pass
                    case SP_obj_type.INSTANCE:
                        instances.append(o)
                    case SP_obj_type.EMPTY:
                        empties.append(o)
                        # treat empties later as they should not be sew (and are instances of the same compound)

                    # empty_to_topods(object, context, scale)
                    case SP_obj_type.COMPOUND:
                        new_objects = convert_compound_to_patches(
                            o, self.context, objects_suffix="_export", resolution=1
                        )
                        comp_shapes = []

                        # from line_profiler import LineProfiler
                        # lp = LineProfiler()
                        # lp.add_function(SP_Contour_export.__init__)
                        # lp.enable()

                        for o_new in new_objects:
                            # Temporarily link
                            self.context.view_layer.active_layer_collection.collection.objects.link(
                                o_new
                            )

                        # bpy.context.view_layer.update()
                        depsgraph = self.context.evaluated_depsgraph_get()

                        for o_new in new_objects:
                            type = sp_type_of_object(o_new)

                            sh = blender_object_to_topods_shapes(
                                depsgraph,
                                o_new,
                                type,
                                scale=self.scale,
                                sew=self.sew,
                            )
                            comp_shapes.append(sh)

                            # Unlink
                            bpy.context.collection.objects.unlink(o_new)

                        new_objects.clear()
                        del new_objects[:]
                        shapes.append(shape_list_to_compound(comp_shapes))
                        objs.append(o)

                        # lp.disable()
                        # lp.print_stats()

                    # Standard shape
                    case _:

                        s = blender_object_to_topods_shapes(
                            self.depsgraph,
                            o,
                            sp_type,
                            self.scale,
                            self.sew,
                            self.sew_tolerance,
                        )
                        objs.append(o)
                        shapes.append(s)

        return objs, shapes, empties, instances, compounds


def blender_object_to_topods_shapes(
    depsgraph, object, sp_type, scale=1000, sew=True, sew_tolerance=1e-1
):
    ob = object.evaluated_get(depsgraph)

    match sp_type:
        case SP_obj_type.CONE:
            shape = cone_face_to_topods(ob, scale)

        case SP_obj_type.SPHERE:
            shape = sphere_face_to_topods(ob, scale)

        case SP_obj_type.CYLINDER:
            shape = cylinder_face_to_topods(ob, scale)
 
        case SP_obj_type.TORUS:
            shape = torus_face_to_topods(ob, scale)

        case SP_obj_type.BEZIER_SURFACE:
            shape = bezier_face_to_topods(ob, scale)

        case SP_obj_type.BSPLINE_SURFACE:
            shape = NURBS_face_to_topods(ob, scale)

        case SP_obj_type.PLANE:
            shape = flat_patch_to_topods(ob, scale)

        case SP_obj_type.CURVE:
            shape = curve_to_topods(ob, scale)

        case SP_obj_type.SURFACE_OF_REVOLUTION:
            shape = revolution_face_to_topods(ob, scale)

        case SP_obj_type.SURFACE_OF_EXTRUSION:
            shape = extrusion_face_to_topods(ob, scale)

        case _:
            raise Exception(f"Invalid shape of type {sp_type}")

    # Mirror
    shape_list_mirrored = mirror_topods_shape(object, shape, scale)

    # Sew
    if sew:
        compound = sew_shapes(shape_list_mirrored, sew_tolerance)
    else:
        compound = shape_list_to_compound(shape_list_mirrored)

    return compound


def blender_instances_to_topods_instances(
    context, hierarchy, scale=1000, sew_tolerance=1e-1
):
    sewed_shapes_list = []
    depsgraph = context.evaluated_depsgraph_get()
    
    for ins in hierarchy.instances:
        if ins.scale.x<0 or ins.scale.y<0 or ins.scale.z<0:
            warnings.warn("Negative instance scale not supported")

        swd = blender_instance_to_topods_instance(
            ins, depsgraph, hierarchy, scale, sew_tolerance
        )
        sewed_shapes_list.append(swd)

    return sewed_shapes_list


def blender_instance_to_topods_instance(
    ins, depsgraph, hierarchy, scale=1000, sew=True, sew_tolerance=1e-1
):
    if ins.scale != Vector((1.0, 1.0, 1.0)):
        print(f"Scale not 1, instance is realized (Scale = {ins.scale})")

    to_sew_shape_list = []
    ins_obj = list(ins.instance_collection.objects)

    # # create compound
    # builder = BRep_Builder()
    # comp = TopoDS_Compound()
    # builder.MakeCompound(comp)
    # is_nested = False

    # add obj of child collections (doesn't support nested instances)
    for col in ins.instance_collection.children_recursive:
        for o in col.objects:
            ins_obj.append(o)

    for o in ins_obj:
        sp_type = sp_type_of_object(o)
        if sp_type not in (None, SP_obj_type.EMPTY, SP_obj_type.INSTANCE):
            if o in hierarchy.obj_shapes.keys():
                shape = hierarchy.obj_shapes[o]
            elif not o.hide_viewport:
                shape = blender_object_to_topods_shapes(
                    depsgraph, o, sp_type, scale, sew, sew_tolerance
                )

            if ins.scale == Vector((1.0, 1.0, 1.0)):
                trsf = blender_matrix_to_gp_trsf(ins.matrix_world, scale)
                trsf.SetScaleFactor(1)
                location = TopLoc_Location(trsf)
                instance = shape.Located(location)
                to_sew_shape_list.append(instance)
            else:
                trsf = blender_matrix_to_gp_trsf(ins.matrix_world, scale)
                trsf.SetScaleFactor(1)
                scalingMatrix = gp_Mat()
                scalingMatrix.SetDiagonal(ins.scale.x, ins.scale.y, ins.scale.z)
                gtrsf = gp_GTrsf()
                gtrsf.SetVectorialPart(scalingMatrix)
                shape = BRepBuilderAPI_GTransform(shape, gtrsf, True).Shape()
                shape = BRepBuilderAPI_Transform(shape, trsf, False).Shape()
                to_sew_shape_list.append(shape)

        # elif sp_type == SP_obj_type.INSTANCE:
        #     warnings.warn("Nested instances not supported yet")
        # #     # nested instance HARD, need to call an instance already built somewhere
        # #     #
        # #     # swd_nested = blender_instance_to_topods_instance(ins, context, hierarchy, scale, sew_tolerance)
        # #     builder.Add(comp, swd_nested)
        # #     is_nested=True

    # each collection instance is sewed separately
    swd = sew_shapes(to_sew_shape_list, sew_tolerance)

    # if is_nested:
    #     builder.Add(comp, swd)
    #     return comp
    # else :
    return swd


def sew_shapes(shape_list, tolerance=1e-1):
    aSew = BRepBuilderAPI_Sewing(tolerance)
    for shape in shape_list:
        aSew.Add(shape)

    # Sew
    aSew.SetNonManifoldMode(True)

    # try :
    aSew.Perform()
    return aSew.SewedShape()


def gather_export_shapes(
    context, use_selection: bool, scale=1000, sew: bool = True, sew_tolerance=1e-1
) -> TopoDS_Compound:

    separated_shapes_list = []
    hierarchy = ShapeHierarchy_export(context, use_selection, scale, sew, sew_tolerance)

    # prepare shapes
    if len(hierarchy.shapes) > 0:
        if sew:
            sewed = sew_shapes(hierarchy.shapes, sew_tolerance)
            separated_shapes_list.extend(shells_to_solids(sewed))
        else:
            separated_shapes_list.extend(hierarchy.shapes)

    # TODO prepare sp compound objects
    # if len(hierarchy.compounds) > 0:
    #     pass
    #     sewed = sew_shapes(hierarchy.shapes, sew_tolerance)
    #     separated_shapes_list.extend(shells_to_solids(sewed))

    # prepare instances
    if len(hierarchy.instances) > 0:
        sewed_instances_list = blender_instances_to_topods_instances(
            context, hierarchy, scale
        )

        for s in sewed_instances_list:
            separated_shapes_list.extend(shells_to_solids(s))

    if len(separated_shapes_list) > 0:
        root_compound = shape_list_to_compound(separated_shapes_list)
    else:
        return None

    return root_compound
