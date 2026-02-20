import numpy as np
from mathutils import Vector, Matrix
from collections import Counter
from ..common.enums import SP_segment_type
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
)
from .export_ellipse import gp_Elips_from_3_points, gp_Elips2d_from_3_points
from OCP.BRepBuilderAPI import (
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
from OCP.Geom import Geom_BezierCurve
from OCP.Geom2d import Geom2d_BezierCurve
from OCP.GeomAdaptor import GeomAdaptor_Surface
from OCP.GeomAPI import GeomAPI_ProjectPointOnSurf
from OCP.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Pnt2d, gp_Vec
from OCP.TopoDS import TopoDS
from OCP.StepGeom import (
    StepGeom_BSplineCurveWithKnotsAndRationalBSplineCurve,
    StepGeom_BSplineCurveForm,
    StepGeom_KnotType,
)
from OCP.StepData import StepData_Logical, StepData_Factors
from OCP.StepToGeom import StepToGeom
from OCP.TCollection import TCollection_HAsciiString


##############################
##    Converter classes     ##
##############################


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


def get_patch_knot_and_mult(
    ob, degree_u, degree_v, isclamped_u, isclamped_v, iscyclic_u, iscyclic_v
):
    # U
    umult_att = read_attribute_by_name(ob, "Multiplicity U")
    try:
        u_length = int(sum(np.asarray(umult_att) > 0))  # uncompatible with mirror
    except KeyError:  # weird
        u_length = int(sum(np.asarray(umult_att) > 0))
    uknots_att = list(read_attribute_by_name(ob, "Knot U", u_length))
    uknot, umult = knot_tcol_from_att(
        uknots_att, umult_att, degree_u, isclamped_u, iscyclic_u
    )

    # V
    vmult_att = read_attribute_by_name(ob, "Multiplicity V")
    try:
        v_length = int(sum(np.asarray(vmult_att) > 0))
    except Exception:
        v_length = int(sum(np.asarray(vmult_att) > 0))
    vknots_att = list(read_attribute_by_name(ob, "Knot V", v_length))
    vknot, vmult = knot_tcol_from_att(
        vknots_att, vmult_att, degree_v, isclamped_v, iscyclic_v
    )

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
