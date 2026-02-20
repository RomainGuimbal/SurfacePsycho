
from mathutils import Vector
from collections import Counter
from ..common.utils import (
    read_attribute_by_name,
    dict_to_list_missing_index_filled,
    split_by_index_dict,
    rebound_UV,
)
from .export_wire import SP_Wire_export

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