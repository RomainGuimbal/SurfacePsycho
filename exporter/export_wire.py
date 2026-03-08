from ..common.enums import SP_segment_type
from mathutils import Vector, Matrix
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeWire
from OCP.TopoDS import TopoDS
from .export_edge import (
    SP_Segment,
    SP_Segment_on_plane,
    SP_Segment_2d,
    geom_curve_to_edge_on_surface,
    geom_curve_to_topods_edge,
    sp_segment_to_geom_curve,
)


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
        segment_list = [
            SP_Segment(
                type=SP_segment_type(self.segs_type_seg_aligned[i]),
                vec_cp=vec_cp_per_seg[i],
                weight=weight[i],
                degree=edges_degrees[i],
                is_clamped=self.isclamped_per_seg[i],
                is_periodic=self.isperiodic_per_seg[i],
                knot=self.knot[i] if len(self.knot) > 1 else None,
                mult=self.mult[i] if len(self.mult) > 1 else None,
            )
            for i in range(self.seg_count)
        ]

        if self.geom_plane:
            segment_list = map(
                lambda segment: SP_Segment_on_plane(
                    plane=self.geom_plane, **segment.__dict__
                ),
                segment_list,
            )

        if self.geom_surf:
            segment_list = map(
                lambda segment: SP_Segment_2d(**segment.__dict__),
                segment_list,
            )

        geom_segment = map(sp_segment_to_geom_curve, segment_list)
        
        if self.geom_surf:
            edges_list = map(lambda segment : geom_curve_to_edge_on_surface(segment, self.geom_surf), geom_segment)
        else :
            edges_list = map(geom_curve_to_topods_edge, geom_segment)

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
