from bpy.types import GeometryNodeTree
from nodebpy import geometry as g, TreeBuilder
from nodebpy.builder import CustomGeometryGroup


class SPSetSegmentResolution(CustomGeometryGroup):
    _name = "SP - Set Segment Resolution"
    _color_tag = "ATTRIBUTE"
    _tree_properties = {"default_group_node_width": 180}

    def _build_group(self, tree: TreeBuilder[GeometryNodeTree]) -> None:
        tree.disable_arrange()

        segment_info = tree.inputs.bundle("Segment Info")
        resolution = tree.inputs.integer("Resolution", 0)
        bundle = tree.outputs.bundle("Bundle")

        separate_bundle = g.SeparateBundle(segment_info)
        type = separate_bundle.items.string("Type", structure_type="SINGLE")
        segment_type = separate_bundle.items.integer("Segment Type", structure_type="SINGLE")
        point_count = separate_bundle.items.integer("Point Count", structure_type="SINGLE")
        degree = separate_bundle.items.integer("Degree", structure_type="SINGLE")
        separate_bundle.items.integer("Resolution", structure_type="SINGLE")
        knot_support = separate_bundle.items.geometry("Knot Support", structure_type="SINGLE")
        knot = separate_bundle.items.float("Knot", structure_type="FIELD")
        unique_knot = separate_bundle.items.float("Unique Knot", structure_type="FIELD")
        multiplicity = separate_bundle.items.integer("Multiplicity", structure_type="FIELD")
        compact_knot_length = separate_bundle.items.integer("Compact Knot Length", structure_type="SINGLE")
        scaled_basis = separate_bundle.items.matrix("Scaled Basis", structure_type="SINGLE")
        min_parameter = separate_bundle.items.float("Min Parameter", structure_type="SINGLE")
        max_parameter = separate_bundle.items.float("Max Parameter", structure_type="SINGLE")
        rational = separate_bundle.items.boolean("Rational", structure_type="SINGLE")
        clamped = separate_bundle.items.boolean("Clamped", structure_type="SINGLE")
        cyclic = separate_bundle.items.boolean("Cyclic", structure_type="SINGLE")
        combine_bundle = g.CombineBundle()
        combine_bundle.items.string(type.output, "Type", structure_type="DYNAMIC")
        combine_bundle.items.integer(segment_type.output, "Segment Type", structure_type="SINGLE")
        combine_bundle.items.integer(point_count.output, "Point Count", structure_type="DYNAMIC")
        combine_bundle.items.integer(degree.output, "Degree", structure_type="SINGLE")
        combine_bundle.items.integer(resolution, "Resolution", structure_type="SINGLE")
        combine_bundle.items.geometry(knot_support.output, "Knot Support", structure_type="")
        combine_bundle.items.float(knot.output, "Knot", structure_type="FIELD")
        combine_bundle.items.float(unique_knot.output, "Unique Knot", structure_type="DYNAMIC")
        combine_bundle.items.integer(multiplicity.output, "Multiplicity", structure_type="DYNAMIC")
        combine_bundle.items.integer(compact_knot_length.output, "Compact Knot Length", structure_type="DYNAMIC")
        combine_bundle.items.matrix(scaled_basis.output, "Scaled Basis", structure_type="DYNAMIC")
        combine_bundle.items.float(min_parameter.output, "Min Parameter", structure_type="DYNAMIC")
        combine_bundle.items.float(max_parameter.output, "Max Parameter", structure_type="DYNAMIC")
        combine_bundle.items.boolean(rational.output, "Rational", structure_type="DYNAMIC")
        combine_bundle.items.boolean(clamped.output, "Clamped", structure_type="SINGLE")
        combine_bundle.items.boolean(cyclic.output, "Cyclic", structure_type="SINGLE")

        combine_bundle.o.bundle >> bundle

        # Restore authored node names and positions (matched by tree
        # structure — see TreeBuilder.layout_snapshot).
        tree.layout_snapshot = {
            "Combine Bundle.001": ("NodeCombineBundle", (87.77, -5.49), None, (("Clamped", "Separate Bundle.001", "Clamped"), ("Compact Knot Length", "Separate Bundle.001", "Compact Knot Length"), ("Cyclic", "Separate Bundle.001", "Cyclic"), ("Degree", "Separate Bundle.001", "Degree"), ("Knot", "Separate Bundle.001", "Knot"), ("Knot Support", "Separate Bundle.001", "Knot Support"), ("Max Parameter", "Separate Bundle.001", "Max Parameter"), ("Min Parameter", "Separate Bundle.001", "Min Parameter"), ("Multiplicity", "Separate Bundle.001", "Multiplicity"), ("Point Count", "Separate Bundle.001", "Point Count"), ("Rational", "Separate Bundle.001", "Rational"), ("Resolution", "Group Input", "Resolution"), ("Scaled Basis", "Separate Bundle.001", "Scaled Basis"), ("Segment Type", "Separate Bundle.001", "Segment Type"), ("Type", "Separate Bundle.001", "Type"), ("Unique Knot", "Separate Bundle.001", "Unique Knot"), )),
            "Group Input": ("NodeGroupInput", (-295.1, 0.0), None, ()),
            "Group Output": ("NodeGroupOutput", (287.77, 0.0), None, (("Bundle", "Combine Bundle.001", "Bundle"), )),
            "Separate Bundle.001": ("NodeSeparateBundle", (-95.1, -15.58), None, (("Bundle", "Group Input", "Segment Info"), )),
        }