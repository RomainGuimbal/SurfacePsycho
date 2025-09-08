import numpy as np
from mathutils import Vector
from os.path import dirname, abspath, isfile
from ..utils import *
from collections import Counter
from .export_ellipse import *


from OCP.BRepBuilderAPI import (
    BRepBuilderAPI_Copy,
    BRepBuilderAPI_GTransform,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_Sewing,
    BRepBuilderAPI_Transform,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeSolid,
)
from OCP.BRepCheck import BRepCheck_Analyzer
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
    Geom_BSplineSurface,
    Geom_Plane,
    Geom_BezierCurve,
    Geom_BSplineCurve,
    Geom_ToroidalSurface,
    Geom_ConicalSurface,
    Geom_CylindricalSurface,
    Geom_SphericalSurface,
    Geom_SurfaceOfLinearExtrusion,
    Geom_SurfaceOfRevolution,
)
from OCP.Geom2d import Geom2d_BezierCurve, Geom2d_BSplineCurve
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
    gp_Circ,
    gp_Ax2d,
    gp_Pnt2d,
    gp_Circ2d,
    gp_Dir2d,
    gp_Vec,
    gp_Vec2d,
    gp_GTrsf,
    gp_Mat,
)
from OCP.IFSelect import IFSelect_RetDone
from OCP.IGESControl import IGESControl_Writer
from OCP.Interface import Interface_Static
from OCP.ShapeFix import ShapeFix_Face
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.TColgp import TColgp_Array1OfPnt, TColgp_Array1OfPnt2d, TColgp_Array2OfPnt
from OCP.TColStd import TColStd_Array1OfInteger, TColStd_Array1OfReal
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import (
    TopoDS_Shape,
    TopoDS,
    TopoDS_Wire,
    TopoDS_Edge,
    TopoDS_Face,
    TopoDS_Shape,
    TopoDS_Compound,
    TopoDS_Iterator,
    TopoDS_Shell,
    TopoDS_Solid,
)


##############################
##    Converter classes     ##
##############################


class SP_Edge_export:
    def __init__(
        self,
        cp_aligned_attrs: dict[str:list],
        seg_attrs: dict[str:float],
        is2D=False,
        geom_surf=None,
        geom_plane=None,
        single_seg=False,
    ):
        self.vec_cp = cp_aligned_attrs["CP"]
        self.gp_cp = []
        self.p_count = len(self.vec_cp)
        self.seg_attrs = seg_attrs
        self.cp_aligned_attrs = cp_aligned_attrs
        self.is2D = is2D
        self.geom_plane = geom_plane
        self.single_seg = single_seg

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
        if "type" in self.seg_attrs.keys():
            return SP_segment_type(self.seg_attrs["type"])

        # Legacy system
        else:
            circle_exists = "circle" in self.seg_attrs.keys()
            if self.p_count < 2:
                raise Exception("Invalid segment")
            elif self.p_count == 2:
                if circle_exists and self.seg_attrs["circle"] > 0.1 and self.single_seg:
                    return SP_segment_type.CIRCLE
                else:
                    return SP_segment_type.BEZIER  # line
            elif circle_exists and self.p_count == 3 and self.seg_attrs["circle"] > 0.1:
                return SP_segment_type.CIRCLE_ARC
            elif (
                self.seg_attrs["degree"] == None
                or self.p_count == self.seg_attrs["degree"] + 1
            ) and not (self.seg_attrs["isperiodic"] or not self.seg_attrs["isclamped"]):
                return SP_segment_type.BEZIER
            else:
                return SP_segment_type.NURBS

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
                raise Exception("Invalid segment type")

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
        isclamped = self.seg_attrs["isclamped"][0] if not None else True
        is_unclamped_periodic = (
            self.seg_attrs["isperiodic"] if not None else False
        ) and not isclamped
        degree = self.seg_attrs["degree"]

        if is_unclamped_periodic:
            self.p_count -= 1
            self.vec_cp = self.vec_cp[:-1]
            self.gp_cp = self.gp_cp[:-1]
            self.cp_aligned_attrs["weight"] = self.cp_aligned_attrs["weight"][:-1]

        if self.is2D:
            segment_point_array = vec_list_to_gp_pnt2d(self.vec_cp)
        else:
            segment_point_array = gp_list_to_arrayofpnt(self.gp_cp)

        tcol_weights = float_list_to_tcolstd(self.cp_aligned_attrs["weight"])
        # TODO custom knot/mult per edge, no design yet
        # try :
        #     if isclamped :
        #         knot_length = self.p_count - degree + 1
        #     else :
        #         knot_length = self.p_count + degree

        #     # knot
        #     knot = float_list_to_tcolstd(read_attribute_by_name(ob, 'Knot', knot_length))

        #     # Multiplicities
        #     mult = TColStd_Array1OfInteger(1, knot_length)
        #     for j in range(knot_length):
        #         if isclamped and (j == 0 or j == knot_length-1):
        #             mult.SetValue(j+1, degree+1)
        #         else :
        #             mult.SetValue(j+1, 1)
        # except Exception:
        #    knot, mult = self.auto_knot_and_mult(degree, isclamped, is_unclamped_periodic)

        knot, mult = auto_knot_and_mult(
            self.p_count, degree, isclamped, is_unclamped_periodic
        )
        if self.is2D:
            self.geom = Geom2d_BSplineCurve(
                segment_point_array,
                tcol_weights,
                knot,
                mult,
                degree,
                is_unclamped_periodic,
            )
        else:
            self.geom = Geom_BSplineCurve(
                segment_point_array,
                tcol_weights,
                knot,
                mult,
                degree,
                is_unclamped_periodic,
            )

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

            # Circle on plane
            if self.geom_plane != None:
                normal_dir = self.geom_plane.Pln().Axis().Direction()
            else:
                normal_dir = gp_Dir(radius_vec.Crossed(other_dir_vec))

            radius = radius_vec.Magnitude()
            makesegment = GC_MakeCircle(gp_Ax1(center, normal_dir), radius)
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

            makesegment = GC_MakeArcOfEllipse(gp_ellipse, self.gp_cp[0], self.gp_cp[4])
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


def auto_knot_and_mult(p_count, degree, isclamped=True, is_unclamped_periodic=False):
    if isclamped:
        knot_length = p_count - degree + 1
        knot_att = [r / (knot_length - 1) for r in range(knot_length)]
        mult_att = [degree + 1] + [1] * (knot_length - 2) + [degree + 1]
    elif is_unclamped_periodic:
        knot_length = p_count + 1
        knot_att = list(range(-degree, p_count + 1 + degree))
        mult_att = [1] * knot_length
    else:
        knot_length = p_count + degree + 1
        knot_att = list(
            range(knot_length)
        )  # [r/(knot_length-1) for r in range(knot_length)]
        mult_att = [1] * knot_length

    knot = TColStd_Array1OfReal(1, knot_length)
    mult = TColStd_Array1OfInteger(1, knot_length)
    for i in range(knot_length):
        knot.SetValue(i + 1, knot_att[i])
        mult.SetValue(i + 1, mult_att[i])

    return knot, mult


def get_patch_knot_and_mult(
    ob,
    u_count,
    v_count,
    degree_u,
    degree_v,
    isclamped_u,
    isclamped_v,
    isperiodic_u,
    isperiodic_v,
):
    try:
        try:
            umult_att = read_attribute_by_name(ob, "Multiplicity U")
            u_length = sum(np.asarray(umult_att) > 0)
        except KeyError:
            umult_att = read_attribute_by_name(ob, "Multiplicity U")
            u_length = int(sum(np.asarray(umult_att) > 0))
        uknots_att = read_attribute_by_name(ob, "Knot U", u_length)

        try:
            vmult_att = read_attribute_by_name(ob, "Multiplicity V")
            v_length = sum(np.asarray(vmult_att) > 0)
        except Exception:
            vmult_att = read_attribute_by_name(ob, "Multiplicity V")
            v_length = int(sum(np.asarray(vmult_att) > 0))
        vknots_att = read_attribute_by_name(ob, "Knot V", v_length)

    except KeyError:  # No custom knot
        uknot, umult = auto_knot_and_mult(u_count, degree_u, isclamped_u, isperiodic_u)
        vknot, vmult = auto_knot_and_mult(v_count, degree_v, isclamped_v, isperiodic_v)
        return uknot, vknot, umult, vmult

    uknot = TColStd_Array1OfReal(1, u_length)
    umult = TColStd_Array1OfInteger(1, u_length)
    for i in range(u_length):
        uknot.SetValue(i + 1, uknots_att[i])
        umult.SetValue(i + 1, umult_att[i])

    vknot = TColStd_Array1OfReal(1, v_length)
    vmult = TColStd_Array1OfInteger(1, v_length)
    for i in range(v_length):
        vknot.SetValue(i + 1, vknots_att[i])
        vmult.SetValue(i + 1, vmult_att[i])

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
        if "circle" in list(seg_aligned_attrs.keys()):
            self.circle_att_seg_aligned = seg_aligned_attrs["circle"]
        else:
            self.circle_att_seg_aligned = [0.0] * self.seg_count

        # Domains :
        ## Is closed : per wire
        ## Is periodic : per segment

        self.isclosed = sum([s - 1 for s in self.segs_p_counts]) == len(self.CP) or (
            sum(self.isperiodic_per_seg) > 0
        )

        p_count = 0  # (total)
        p_count_accumulate = self.segs_p_counts[:]
        for i, p in enumerate(self.segs_p_counts):
            if p > 0:
                p_count += p - 1
            elif p == 0:
                break
            if i > 0:
                p_count_accumulate[i] += p_count_accumulate[i - 1] - 1

        self.seg_first_P_id = [0] + [
            p - 1 for p in p_count_accumulate[: self.seg_count - 1]
        ]
        # self.p_count_accumulate = p_count_accumulate[:len(self.segs_p_counts)]

    def split_cp_aligned_attr_per_seg(self, attr) -> list[list]:
        split_attr = []
        inf = 0
        sup = self.segs_p_counts[0]
        for i in range(self.seg_count):
            # for last segment but not only segment
            if (
                i == self.seg_count - 1
                and self.isclosed
                and self.seg_count > 1
                and self.circle_att_seg_aligned[i] < 0.1
            ):
                split_attr.append(attr[inf : len(self.CP)] + [attr[0]])
            else:
                split_attr.append(attr[inf:sup])
                if i < self.seg_count - 1:  # Skip increment in last loop
                    inf = sup - 1
                    sup = inf + self.segs_p_counts[i + 1]
        return split_attr

    def get_topods_wire(self):
        # split because not needed with svg. Can be judged unnecessary

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
                    "circle": self.circle_att_seg_aligned[i],
                    "isclamped": self.isclamped_per_seg,
                    "isperiodic": self.isperiodic_per_seg,
                    "type": self.segs_type_seg_aligned[i],
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
    ):
        # Check if trimmed
        try:
            self.segs_p_counts = read_attribute_by_name(ob, p_count_attr_name)
            self.wire_index = read_attribute_by_name(ob, "Wire")
            self.seg_count_per_wire = read_attribute_by_name(ob, "seg_count_per_wire")
            self.has_wire = True
        except Exception:  # No trim
            self.has_wire = False

        if self.has_wire:
            # Get total_p_count
            self.total_p_count = 0
            for i, wi in enumerate(self.wire_index):
                if wi == 0:
                    break
                self.total_p_count += 1

            # crop wire_index
            self.wire_index = self.wire_index[: self.total_p_count]
            self.p_count_per_wire = Counter(self.wire_index)

            # crop seg_count_per_wire
            self.wire_index_order = list(dict.fromkeys(self.wire_index))
            self.wir_count = len(self.wire_index_order)
            self.seg_count_per_wire = self.seg_count_per_wire[: self.wir_count]

            # Get segment count
            self.segment_count = 0
            for p in self.segs_p_counts:
                if p > 0:
                    self.segment_count += 1
                else:
                    break

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

            if is2D:
                points = [Vector((p[1], p[0], 0.0)) for p in points]
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

            ## Circle LEGACY
            try:
                circle_att = read_attribute_by_name(ob, "Circle", self.segment_count)
            except KeyError:
                circle_att = [0.0] * self.segment_count
            circle_att_per_wire = self.split_seg_attr_per_wire(circle_att)

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
                        "circle": circle_att_per_wire[w],
                        "type": type_att_per_wire[w],
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
        wir_i = 0
        wir_key = self.wire_index_order[wir_i]
        seg_added = 0

        # Prepare dict
        attr_dict_per_wire = {}
        for w in set(self.wire_index):
            attr_dict_per_wire[w] = []

        # Itterate over segments
        for i, att_val in enumerate(attr[: self.segment_count]):
            seg_added += 1
            attr_dict_per_wire[wir_key].append(att_val)

            if (
                seg_added >= self.seg_count_per_wire[wir_i]
                and wir_i < self.wir_count - 1
            ):
                wir_i += 1
                wir_key = self.wire_index_order[wir_i]
                seg_added = 0

        return attr_dict_per_wire


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


def bezier_face_to_topods(o, context, scale=1000):
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
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
        wires = contour.wires_dict

    # Get topods wires
    outer_wire = wires[-1].get_topods_wire()
    inner_wires = []
    for k in wires.keys():
        if k != -1:
            inner_wires.append(wires[k].get_topods_wire())

    face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def NURBS_face_to_topods(o, context, scale=1000):
    # Get attributes
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    u_count = int(ob.data.attributes["CP_count"].data[0].value)
    v_count = int(ob.data.attributes["CP_count"].data[1].value)
    points = read_attribute_by_name(ob, "CP_NURBS_surf", u_count * v_count)
    points *= scale
    degree_u, degree_v = read_attribute_by_name(ob, "Degrees", 2)
    try:
        isclamped_u, isclamped_v = read_attribute_by_name(ob, "IsClamped", 2)
        isperiodic_u, isperiodic_v = read_attribute_by_name(ob, "IsPeriodic", 2)
    except KeyError:
        isclamped_u, isclamped_v, isperiodic_u, isperiodic_v = True, True, False, False

    # Knots and Multiplicities
    uknots, vknots, umult, vmult = get_patch_knot_and_mult(
        ob,
        u_count,
        v_count,
        degree_u,
        degree_v,
        isclamped_u,
        isclamped_v,
        isperiodic_u,
        isperiodic_v,
    )

    # Poles grid
    poles = TColgp_Array2OfPnt(1, u_count, 1, v_count)
    for i in range(v_count):
        for j in range(u_count):
            id = u_count * i + j
            poles.SetValue(
                j + 1, i + 1, gp_Pnt(points[id][0], points[id][1], points[id][2])
            )

    # Compose Geom
    geom_surf = Geom_BSplineSurface(
        poles,
        uknots,
        vknots,
        umult,
        vmult,
        degree_u,
        degree_v,
        isperiodic_u,
        isperiodic_v,
    )

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
        wires = contour.wires_dict

        # Get topods wires
        outer_wire = wires[-1].get_topods_wire()
        inner_wires = []
        for k in wires.keys():
            if k != -1:
                inner_wires.append(wires[k].get_topods_wire())

        face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
        return face


def cone_face_to_topods(o, context, scale=1000):
    # Get attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
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
        scale=(radius / math.sin(semi_angle), 1),
    )

    # Create topods face
    if not contour.has_wire:
        return geom_to_topods_face(geom_surf)
    else:
        wires = contour.wires_dict

    # Get topods wires
    outer_wire = wires[-1].get_topods_wire()
    inner_wires = []
    for k in wires.keys():
        if k != -1:
            inner_wires.append(wires[k].get_topods_wire())

    face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def sphere_face_to_topods(o, context, scale=1000):
    # Get attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    origin, dir1, dir2 = read_attribute_by_name(ob, "axis3_sphere", 3)
    radius = float(ob.data.attributes["radius"].data[0].value)

    # Create geom
    axis3 = gp_Ax3(
        gp_Pnt(origin[0] * scale, origin[1] * scale, origin[2] * scale),
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
        return geom_to_topods_face(geom_surf)
    else:
        wires = contour.wires_dict

    # Get topods wires
    outer_wire = wires[-1].get_topods_wire()
    inner_wires = []
    for k in wires.keys():
        if k != -1:
            inner_wires.append(wires[k].get_topods_wire())

    face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def torus_face_to_topods(o, context, scale=1000):
    # Get attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
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
        return geom_to_topods_face(geom_surf)
    else:
        wires = contour.wires_dict

    # Get topods wires
    outer_wire = wires[-1].get_topods_wire()
    inner_wires = []
    for k in wires.keys():
        if k != -1:
            inner_wires.append(wires[k].get_topods_wire())

    face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def cylinder_face_to_topods(o, context, scale=1000):
    # Get attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    origin, dir1, dir2 = read_attribute_by_name(ob, "axis3_cylinder", 3)
    radius, length = read_attribute_by_name(ob, "radius_length", 2)

    # Create geom
    axis3 = gp_Ax3(
        gp_Pnt(origin[0] * scale, origin[1] * scale, origin[2] * scale),
        gp_Dir(dir1[0], dir1[1], dir1[2]),
        gp_Dir(dir2[0], dir2[1], dir2[2]),
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
        scale=(length * scale, 1),
    )

    # Create topods face
    if not contour.has_wire:
        return geom_to_topods_face(geom_surf)
    else:
        wires = contour.wires_dict

    # Get topods wires
    outer_wire = wires[-1].get_topods_wire()
    inner_wires = []
    for k in wires.keys():
        if k != -1:
            inner_wires.append(wires[k].get_topods_wire())

    face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def revolution_face_to_topods(o, context, scale=1000):
    # Get attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
    origin, dir1 = read_attribute_by_name(ob, "axis1_revolution", 2)
    p_count = read_attribute_by_name(ob, "p_count_revolution", 1)[0]
    segment_CP = read_attribute_by_name(ob, "CP_revolution", p_count)
    segment_CP *= scale
    weight = read_attribute_by_name(ob, "weight_revolution", p_count)
    type = read_attribute_by_name(ob, "type_revolution", 1)[0]
    degree = read_attribute_by_name(ob, "degree_revolution", 1)[0]
    is_clamped, is_periodic = read_attribute_by_name(
        ob, "clamped_periodic_revolution", 2
    )

    geom_segment = SP_Edge_export(
        {"CP": segment_CP, "weight": weight},
        {
            "degree": degree,
            "isclamped": [is_clamped],
            "isperiodic": [is_periodic],
            "type": type,
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
        return geom_to_topods_face(geom_surf)
    else:
        wires = contour.wires_dict

    # Get topods wires
    outer_wire = wires[-1].get_topods_wire()
    inner_wires = []
    for k in wires.keys():
        if k != -1:
            inner_wires.append(wires[k].get_topods_wire())

    face = geom_to_topods_face(geom_surf, outer_wire, inner_wires)
    return face


def curve_to_topods(o, context, scale=1000):
    # Get point count attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())
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

    # 1 point less if closed
    is_closed = bool(ob.data.attributes["IsPeriodic"].data[0].value)
    total_p_count -= is_closed and segment_count > 1

    # is clamped
    is_clamped = bool(ob.data.attributes["IsClamped"].data[0].value)

    # Type
    try:
        type_att = read_attribute_by_name(ob, "Type", segment_count)
    except Exception:
        type_att = [0] * segment_count

    # Degree
    try:
        segs_degrees = read_attribute_by_name(ob, "Degree", segment_count)
    except Exception:
        segs_degrees = [0] * segment_count

    # Circles LEGACY
    try:
        circle_att = read_attribute_by_name(ob, "Circle", segment_count)
    except KeyError:
        circle_att = [0.0] * segment_count

    # Get CP position attr
    points = read_attribute_by_name(ob, "CP_curve", total_p_count)
    points *= scale

    ## Weight
    try:
        weight_attr = read_attribute_by_name(ob, "Weight", total_p_count)
    except KeyError:
        weight_attr = [1.0] * total_p_count

    wire = SP_Wire_export(
        {"CP": points, "weight": weight_attr},
        {
            "p_count": segs_p_counts,
            "degree": segs_degrees,
            "isperiodic": [is_closed] * segment_count,
            "isclamped": [is_clamped] * segment_count,
            "circle": circle_att,
            "type": type_att,
        },
        is2D=False,
    )
    topods_wire = wire.get_topods_wire()

    return topods_wire


def flat_patch_to_topods(o, context, scale=1000):
    # Get point count attr
    ob = o.evaluated_get(context.evaluated_depsgraph_get())

    # Orient and offset
    loc, rot, _ = o.matrix_world.decompose()
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
    wires = SP_Contour_export(
        ob,
        "CP_planar",
        "CP_count",
        "IsClamped",
        "IsPeriodic",
        scale,
        geom_plane=geom_pl,
        is2D=False,
    ).wires_dict

    # Get occ wires
    outer_wire = wires[-1].get_topods_wire()
    inner_wires = []
    for k in wires.keys():
        if k != -1:
            inner_wires.append(wires[k].get_topods_wire())

    face = geom_to_topods_face(None, outer_wire, inner_wires)
    return face


def empty_to_topods(o, context, scale=1000):

    # Orient and offset
    gp_trsf = blender_matrix_to_gp_trsf(o.matrix_world, scale)
    gp_pln = gp_Pln(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)).Transformed(gp_trsf)
    # gp_pnt = TopoDS_Vertex(gp_Pnt(0,0,0).Transformed(gp_trsf)) vertices cannot be exported :c
    topods_plane = geom_to_topods_face(Geom_Plane(gp_pln))
    return topods_plane


def mirror_topods_shape(o, shape, scale=1000, sew_tolerance=1e-1):
    ms = BRepBuilderAPI_Sewing(sew_tolerance)
    ms.SetNonManifoldMode(True)
    ms.Add(shape)

    ms.Perform()
    shape = ms.SewedShape()
    loc, rot, _ = o.matrix_world.decompose()

    for m in o.modifiers:
        if m.type == "MIRROR" and m.show_viewport:
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

            ms2 = BRepBuilderAPI_Sewing(1e-1)
            ms2.SetNonManifoldMode(True)

            for i in range(7):  # 7 = 8 mirror configs -1 original config
                if configurations[i]:
                    if symtype[i] == 1:  # planar sym
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

                    elif symtype[i] == 2:  # axis sym
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

                    else:  # centric sym
                        atrsf = gp_Trsf()
                        atrsf.SetMirror(
                            gp_Pnt(mirror_offset[0], mirror_offset[1], mirror_offset[2])
                        )

                    mshape = BRepBuilderAPI_Transform(shape, atrsf).Shape()
                    ms2.Add(shape)
                    ms2.Add(mshape)
                    # mshape = BRepBuilderAPI_Transform(shape, atrsf).Shape()
                    # ms.Add(mshape)

            ms2.Perform()
            shape = ms2.SewedShape()
            # ms.Perform()
            # shape = ms.SewedShape()

    # ms.Perform()
    # shape = ms.SewedShape()
    return shape


# not a true hierarchy. too complex for now
class ShapeHierarchy_export:
    def __init__(self, context, use_selection=True, scale=1000, sew_tolerance=1e-1):
        self.context = context
        self.use_selection = use_selection
        self.scale = scale
        self.sew_tolerance = sew_tolerance

        objs, shapes, empties, instances, compounds = self.create_shape_hierarchy(
            context.scene.collection
        )
        self.shapes = shapes
        self.instances = instances
        self.empties = empties
        self.compounds = compounds

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
                sp_type = sp_type_of_object(o, self.context)
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
                        dg = self.context.evaluated_depsgraph_get()
                        ob = o.evaluated_get(dg)
                        for inst in dg.object_instances:
                            if inst.is_instance and inst.parent == ob:
                                # TODO
                                #         blender_object_to_topods_shapes(self.context, o, sp_type, self.scale, self.sew_tolerance)
                                # sewed = sew_shapes(hierarchy.shapes, sew_tolerance)
                                # separated_shapes_list.extend(shells_to_solids(sewed))
                                # compounds.append(o)
                                pass

                    # Standard shape
                    case _:
                        s = blender_object_to_topods_shapes(
                            self.context, o, sp_type, self.scale, self.sew_tolerance
                        )
                        objs.append(o)
                        shapes.append(s)

        return objs, shapes, empties, instances, compounds


def blender_object_to_topods_shapes(
    context, object, sp_type, scale=1000, sew_tolerance=1e-1
):
    match sp_type:
        case SP_obj_type.CONE:
            shape = cone_face_to_topods(object, context, scale)
            shape_mirrored = mirror_topods_shape(object, shape, scale, sew_tolerance)

        case SP_obj_type.SPHERE:
            shape = sphere_face_to_topods(object, context, scale)
            shape_mirrored = mirror_topods_shape(object, shape, scale, sew_tolerance)

        case SP_obj_type.CYLINDER:
            shape = cylinder_face_to_topods(object, context, scale)
            shape_mirrored = mirror_topods_shape(object, shape, scale, sew_tolerance)

        case SP_obj_type.TORUS:
            shape = torus_face_to_topods(object, context, scale)
            shape_mirrored = mirror_topods_shape(object, shape, scale, sew_tolerance)

        case SP_obj_type.BEZIER_SURFACE:
            shape = bezier_face_to_topods(object, context, scale)
            shape_mirrored = mirror_topods_shape(object, shape, scale, sew_tolerance)

        case SP_obj_type.BSPLINE_SURFACE:
            shape = NURBS_face_to_topods(object, context, scale)
            shape_mirrored = mirror_topods_shape(object, shape, scale, sew_tolerance)

        case SP_obj_type.PLANE:
            shape = flat_patch_to_topods(object, context, scale)
            shape_mirrored = mirror_topods_shape(object, shape, scale, sew_tolerance)

        case SP_obj_type.CURVE:
            shape = curve_to_topods(object, context, scale)
            shape_mirrored = mirror_topods_shape(object, shape, scale, sew_tolerance)

        case SP_obj_type.SURFACE_OF_REVOLUTION:
            shape = revolution_face_to_topods(object, context, scale)
            shape_mirrored = mirror_topods_shape(object, shape, scale, sew_tolerance)

        case _:
            raise Exception(f"Invalid type {sp_type}")

    return shape_mirrored


def blender_instances_to_topods_instances(
    context, hierarchy, scale=1000, sew_tolerance=1e-1
):
    sewed_shapes_list = []

    for ins in hierarchy.instances:
        swd = blender_instance_to_topods_instance(
            ins, context, hierarchy, scale, sew_tolerance
        )

    sewed_shapes_list.append(swd)
    return sewed_shapes_list


def blender_instance_to_topods_instance(
    ins, context, hierarchy, scale=1000, sew_tolerance=1e-1
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
        sp_type = sp_type_of_object(o, context)
        if sp_type not in (None, SP_obj_type.EMPTY, SP_obj_type.INSTANCE):
            if o in hierarchy.obj_shapes.keys():
                shape = hierarchy.obj_shapes[o]
            elif not o.hide_viewport:
                shape = blender_object_to_topods_shapes(
                    context, o, sp_type, scale, sew_tolerance
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
    # except Exception:
    #     return shape_list_to_compound(shape_list) # necessary ?


def prepare_export(
    context, use_selection: bool, scale=1000, sew_tolerance=1e-1
) -> TopoDS_Compound:
    separated_shapes_list = []
    hierarchy = ShapeHierarchy_export(context, use_selection, scale)

    # prepare shapes
    if len(hierarchy.shapes) > 0:
        sewed = sew_shapes(hierarchy.shapes, sew_tolerance)
        separated_shapes_list.extend(shells_to_solids(sewed))

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


def export_step(
    context,
    filepath,
    use_selection,
    scale,
    sew_tolerance,
):
    brep_shapes = prepare_export(context, use_selection, scale, sew_tolerance)
    if brep_shapes is not None:
        write_step_file(brep_shapes, filepath, application_protocol="AP203")
        return True
    else:
        return False


def export_iges(
    context,
    filepath,
    use_selection,
    scale,
    sew_tolerance,
):
    brep_shapes = prepare_export(context, use_selection, scale, sew_tolerance)
    if brep_shapes is not None:
        write_iges_file(brep_shapes, filepath)
        return True
    else:
        return False


###########################
# Step export OCC Extends #
###########################


def write_step_file(a_shape, filename, application_protocol="AP203"):
    """exports a shape to a STEP file
    a_shape: the topods_shape to export (a compound, a solid etc.)
    filename: the filename
    application protocol: "AP203" or "AP214IS" or "AP242DIS"
    """
    # a few checks
    if a_shape.IsNull():
        raise AssertionError(f"Shape {a_shape} is null.")
    if application_protocol not in ["AP203", "AP214IS", "AP242DIS"]:
        raise AssertionError(
            f"application_protocol must be either AP203 or AP214IS. You passed {application_protocol}."
        )
    if isfile(filename):
        print(f"Warning: {filename} file already exists and will be replaced")
    # creates and initialise the step exporter
    step_writer = STEPControl_Writer()
    Interface_Static.SetCVal_s("write.step.schema", application_protocol)

    # transfer shapes and write file
    step_writer.Transfer(a_shape, STEPControl_AsIs)
    status = step_writer.Write(filename)

    if status != IFSelect_RetDone:
        raise IOError("Error while writing shape to STEP file.")
    if not isfile(filename):
        raise IOError(f"{filename} not saved to filesystem.")


###########################
# IGES export OCC Extends #
###########################


def write_iges_file(a_shape, filename):
    """exports a shape to a STEP file
    a_shape: the topods_shape to export (a compound, a solid etc.)
    filename: the filename
    application protocol: "AP203" or "AP214"
    """
    # a few checks
    if a_shape.IsNull():
        raise AssertionError("Shape is null.")
    if isfile(filename):
        print(f"Warning: {filename} already exists and will be replaced")
    # creates and initialise the step exporter
    iges_writer = IGESControl_Writer()
    iges_writer.AddShape(a_shape)
    status = iges_writer.Write(filename)

    if status != IFSelect_RetDone:
        raise AssertionError("Not done.")
    if not isfile(filename):
        raise IOError("File not written to disk.")
