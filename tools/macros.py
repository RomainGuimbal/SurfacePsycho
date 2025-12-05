import bpy
import bmesh
from ..common.utils import *
from ..common.compound_utils import *
from mathutils import Vector

from os.path import dirname, abspath, join
import platform
from ..exporter.export_process_svg import *

os = platform.system()

from ..importer.import_shape_to_blender_object import *
from ..exporter.export_process_cad import *


class SP_OT_add_library(bpy.types.Operator):
    bl_idname = "object.sp_add_library"
    bl_label = "SP - Add Library"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # create lib
        asset_lib_path = join(dirname(dirname(abspath(__file__))), "assets")
        paths = [a.path for a in context.preferences.filepaths.asset_libraries]
        if asset_lib_path not in paths:
            bpy.ops.preferences.asset_library_add(directory=asset_lib_path)

        # Rename lib
        asset_library = context.preferences.filepaths.asset_libraries.get("assets")
        if asset_library:
            asset_library.name = "SurfacePsycho"

        return {"FINISHED"}


class SP_OT_toggle_control_geom(bpy.types.Operator):
    bl_idname = "object.sp_toggle_control_geom"
    bl_label = "SP - Toggle Control Geom"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Toggle the control geometry of selected object. The active object determines whether to show or hide"

    def execute(self, context):
        objects = [ob for ob in context.selected_objects]
        first_obj_found = False
        for o in objects:
            for m in o.modifiers:
                if m.type == "NODES" and m.node_group.name[:5] == "SP - ":
                    for it in m.node_group.interface.items_tree:
                        if (
                            it.name
                            in [
                                "Control Polygon",
                                "Control Geometry",
                                "Control Grid",
                                "Control Edges",
                            ]
                            and it.socket_type == "NodeSocketBool"
                        ):
                            input_id = it.identifier
                            if not first_obj_found:
                                first_obj_found = True
                                toggle_side = not m[input_id]
                            m[input_id] = toggle_side
                    m.node_group.interface_update(context)
        return {"FINISHED"}


class SP_OT_select_all(bpy.types.Operator):
    bl_idname = "object.sp_select_all"
    bl_label = "SP - Select All Visible"
    bl_description = "Select all visible SP objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objects = [ob for ob in context.visible_objects]
        for o in objects:
            if sp_type_of_object(o) != None:
                o.select_set(True)
        return {"FINISHED"}


class SP_OT_select_visible_curves(bpy.types.Operator):
    bl_idname = "object.sp_select_visible_curves"
    bl_label = "SP - Select Visible Curves"
    bl_description = "Select Visible Curves"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objects = [ob for ob in context.visible_objects]
        for o in objects:
            if sp_type_of_object(o) == SP_obj_type.CURVE:
                o.select_set(True)
        return {"FINISHED"}


class SP_OT_select_visible_surfaces(bpy.types.Operator):
    bl_idname = "object.sp_select_visible_surfaces"
    bl_label = "SP - Select Visible Surfaces"
    bl_description = "Select Visible Surfaces"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objects = [ob for ob in context.visible_objects]
        for o in objects:
            if sp_type_of_object(o) in [
                SP_obj_type.PLANE,
                SP_obj_type.CYLINDER,
                SP_obj_type.CONE,
                SP_obj_type.SPHERE,
                SP_obj_type.TORUS,
                SP_obj_type.BEZIER_SURFACE,
                SP_obj_type.BSPLINE_SURFACE,
                SP_obj_type.SURFACE_OF_REVOLUTION,
                SP_obj_type.SURFACE_OF_EXTRUSION,
                SP_obj_type.OTHER_SURFACE,
            ]:
                o.select_set(True)

        return {"FINISHED"}


class SP_OT_update_modifiers(bpy.types.Operator):
    bl_idname = "object.sp_update_modifiers"
    bl_label = "SP - Update Modifiers"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        old_new_pairs = {}
        for node_group in bpy.data.node_groups:
            if node_group.type == "GEOMETRY" and node_group.name[:5] == "SP - ":
                print(node_group.name)
                if node_group not in old_new_pairs.keys():
                    old_new_pairs[node_group] = None
        print("\n")
        names = []
        for p in old_new_pairs.keys():
            names.append(p.name)
            print(p.name)

        new_ng = append_multiple_node_groups(names)

        self.report({"INFO"}, "Not Implemented")

        return {"FINISHED"}


class SP_OT_replace_node_group(bpy.types.Operator):
    bl_idname = "object.sp_replace_node_group"
    bl_label = "SP - Replace Node Group"
    bl_description = (
        "For updating old assets. Replaces all instance of a modifier with another"
    )
    bl_options = {"REGISTER", "UNDO"}

    target_name: bpy.props.StringProperty(name="Target", description="", default="")
    new_name: bpy.props.StringProperty(name="New", description="", default="")

    def execute(self, context):
        target_node_group_name = self.target_name
        new_node_group_name = self.new_name

        r = replace_all_instances_of_node_group(
            target_node_group_name, new_node_group_name
        )
        if r >= 1:
            self.report({"INFO"}, f"{r} node groups successfully replaced")
        elif r == 0:
            self.report({"INFO"}, f"{new_node_group_name} does not exist")
        elif r == -1:
            self.report({"INFO"}, f"{target_node_group_name} does not exist")
        return {"FINISHED"}

    # Display panel
    def invoke(self, context, event):
        # call itself and run
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class SP_OT_psychopatch_to_bl_nurbs(bpy.types.Operator):
    bl_idname = "object.sp_psychopatch_to_bl_nurbs"
    bl_label = "SP - Convert Psychopatches to internal NURBS"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        spline_index = -1
        for o in context.selected_objects:
            sp_type = sp_type_of_object(o)
            ob = o.evaluated_get(context.evaluated_depsgraph_get())
            match sp_type:
                case SP_obj_type.BEZIER_SURFACE:
                    u_count = int(ob.data.ge.attributes["CP_count"].data[0].value)
                    v_count = int(ob.data.ge.attributes["CP_count"].data[1].value)
                    cp = read_attribute_by_name(
                        ob, "CP_any_order_surf", u_count * v_count
                    )
                    if spline_index == -1:
                        bpy.ops.surface.primitive_nurbs_surface_surface_add(
                            enter_editmode=True,
                            align="WORLD",
                            location=(0, 0, 0),
                            scale=(1, 1, 1),
                        )
                        bpy.ops.curve.delete(type="VERT")
                    spline_index += 1
                    splines = context.active_object.data.splines
                    for v in range(v_count):
                        spline = splines.new("NURBS")
                        spline.points.add(u_count - 1)
                        spline.use_endpoint_u = True
                        spline.use_endpoint_v = True
                        spline.use_bezier_u = True
                        spline.use_bezier_v = True
                        # set CP of spline
                        for j, p in enumerate(spline.points):
                            p.co = (
                                cp[j + v * u_count][0],
                                cp[j + v * u_count][1],
                                cp[j + v * u_count][2],
                                1,
                            )

                    for s in splines[spline_index : spline_index + v_count]:
                        for p in s.points:
                            p.select = True
                    bpy.ops.object.mode_set(mode="EDIT")
                    bpy.ops.curve.make_segment()
                    splines[spline_index].order_u = min(v_count, 6)
                    splines[spline_index].order_v = min(u_count, 6)

                case SP_obj_type.BSPLINE_SURFACE:
                    u_count = int(ob.data.ge.attributes["CP_count"].data[0].value)
                    v_count = int(ob.data.ge.attributes["CP_count"].data[1].value)
                    cp = read_attribute_by_name(ob, "CP_nurbs_surf", u_count * v_count)
                    if spline_index == -1:
                        bpy.ops.surface.primitive_nurbs_surface_surface_add(
                            enter_editmode=True,
                            align="WORLD",
                            location=(0, 0, 0),
                            scale=(1, 1, 1),
                        )
                        bpy.ops.curve.delete(type="VERT")
                    spline_index += 1
                    splines = context.active_object.data.splines
                    for v in range(v_count):
                        spline = splines.new("NURBS")
                        spline.points.add(u_count - 1)
                        spline.use_endpoint_u = True
                        spline.use_endpoint_v = True
                        spline.use_bezier_u = False
                        spline.use_bezier_v = False
                        # set CP of spline
                        for j, p in enumerate(spline.points):
                            p.co = (
                                cp[j + v * u_count][0],
                                cp[j + v * u_count][1],
                                cp[j + v * u_count][2],
                                1,
                            )

                    for s in splines[spline_index : spline_index + v_count]:
                        for p in s.points:
                            p.select = True
                    bpy.ops.object.mode_set(mode="EDIT")
                    bpy.ops.curve.make_segment()
                    splines[spline_index].order_u = min(v_count, 6)
                    splines[spline_index].order_v = min(u_count, 6)

                case SP_obj_type.CURVE:
                    cp_count = int(ob.data.ge.attributes["CP_count"].data[0].value)
                    cp = read_attribute_by_name(ob, "CP_any_order_curve", cp_count)
                    if spline_index == -1:
                        bpy.ops.surface.primitive_nurbs_surface_surface_add(
                            enter_editmode=True,
                            align="WORLD",
                            location=(0, 0, 0),
                            scale=(1, 1, 1),
                        )
                        bpy.ops.curve.delete(type="VERT")
                    spline_index += 1
                    spline = context.active_object.data.splines.new("NURBS")
                    spline.points.add(cp_count - 1)
                    spline.use_endpoint_u = True
                    spline.use_endpoint_v = True
                    spline.use_bezier_u = True
                    spline.use_bezier_v = True
                    spline.order_u = min(cp_count, 6)
                    spline.order_v = min(cp_count, 6)

                    # set CP of spline
                    for j, p in enumerate(spline.points):
                        p.co = (cp[j][0], cp[j][1], cp[j][2], 1)

                case _:
                    self.report({"WARNING"}, "Conversion unsupported")

        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}


class SP_OT_bl_nurbs_to_psychopatch(bpy.types.Operator):
    bl_idname = "object.sp_bl_nurbs_to_psychopatch"
    bl_label = "SP - Convert internal NURBS to Psychopatches"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj_to_convert = context.selected_objects
        first_bezier_patch_flag = True
        first_bspline_patch_flag = True

        for o in obj_to_convert:
            if o.type == "SURFACE":
                for s in o.data.splines:
                    if s.use_bezier_u and s.use_bezier_v:
                        if first_bezier_patch_flag:
                            append_object_by_name("Bezier Patch", context)
                            first_bezier_patch_flag = False
                            first_sp_bezier_patch = context.selected_objects[0]
                            first_sp_bezier_patch.location = o.location
                            sp_patch = first_sp_bezier_patch
                        else:
                            sp_patch = first_sp_bezier_patch.copy()
                            sp_patch.animation_data_clear()
                            sp_patch.matrix_world = o.matrix_world
                            context.collection.objects.link(sp_patch)
                    else:
                        if first_bspline_patch_flag:
                            append_object_by_name("NURBS Patch", context)
                            first_bspline_patch_flag = False
                            first_sp_bspline_patch = context.selected_objects[0]
                            first_sp_bspline_patch.location = o.location
                            sp_patch = first_sp_bspline_patch
                        else:
                            sp_patch = first_sp_bspline_patch.copy()
                            sp_patch.animation_data_clear()
                            sp_patch.matrix_world = o.matrix_world
                            context.collection.objects.link(sp_patch)

                    spline_cp = [Vector(p.co[0:3]) for p in s.points]

                    # create mesh grid
                    u_count = s.order_u
                    v_count = s.order_v

                    # TODO change modifier options for clamped U and V

                    faces = [
                        (
                            v * u_count + u,
                            (v + 1) * u_count + u,
                            (v + 1) * u_count + 1 + u,
                            v * u_count + 1 + u,
                        )
                        for v in range(v_count - 1)
                        for u in range(u_count - 1)
                    ]
                    mesh = bpy.data.meshes.new("Grid")
                    mesh.from_pydata(spline_cp, [], faces)
                    sp_patch.data = mesh
                    bpy.ops.object.shade_smooth()
        return {"FINISHED"}


class SP_OT_toggle_endpoints(bpy.types.Operator):
    """Mark or unmark selected vertices as endpoint depending on the active vertex"""

    bl_idname = "mesh.sp_toggle_endpoints"
    bl_label = "SP - Toggle Endpoints"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        att_name = "Endpoints"
        objs = context.objects_in_mode
        bpy.ops.object.mode_set(mode="OBJECT")
        for o in objs:
            if att_name in o.data.attributes:
                if not toggle_bool_attribute(o, att_name):
                    if not toggle_pseudo_bool_attribute(o, att_name):
                        o.data.attributes.new(
                            name=att_name, type="BOOLEAN", domain="POINT"
                        )
                        o.data.update()

            # Vertex group (LEGACY)
            elif att_name in o.vertex_groups:
                toggle_pseudo_bool_vertex_group(o, att_name)
            else:
                o.data.attributes.new(name=att_name, type="BOOLEAN", domain="POINT")
                o.data.update()

        bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}


class SP_OT_select_endpoints(bpy.types.Operator):
    """Select vertices marked as segment ends"""

    bl_idname = "mesh.sp_select_endpoints"
    bl_label = "SP - Select Endpoints"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objects = context.objects_in_mode
        bpy.ops.object.mode_set(mode="OBJECT")
        select_by_attriute("Endpoints", objects)
        bpy.ops.object.mode_set(mode="EDIT")

        return {"FINISHED"}


class SP_OT_set_segment_type(bpy.types.Operator):
    """Mark segment type for selection"""

    bl_idname = "mesh.sp_set_segment_type"
    bl_label = "SP - Set Segment Type"
    bl_options = {"REGISTER", "UNDO"}

    type: bpy.props.EnumProperty(
        name="Type",
        default=0,
        items=[
            ("spline", "Spline", ""),
            ("circle_arc", "Circle Arc", ""),
            ("circle", "Circle", ""),
            ("ellipse_arc", "Ellipse Arc", ""),
            ("ellipse", "Ellipse", ""),
        ],
    )

    def execute(self, context):
        type_index = 0
        match self.type:
            case "spline":
                type_index = 0
            case "circle_arc":
                type_index = 2
            case "circle":
                type_index = 3
            case "ellipse_arc":
                type_index = 4
            case "ellipse":
                type_index = 5

        set_segment_type(context, type_index)
        return {"FINISHED"}


class SP_OT_assign_as_ellipse(bpy.types.Operator):
    bl_idname = "object.sp_assign_as_ellipse"
    bl_label = "SP - Assign as Ellipse"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = context.objects_in_mode

        for o in objs:
            # Switch to object mode to modify vertex groups
            bpy.ops.object.mode_set(mode="OBJECT")
            # Ensure "Ellipses" vertex group exists
            if "Ellipse" not in o.vertex_groups:
                o.vertex_groups.new(name="Ellipse")

            vg = o.vertex_groups["Ellipse"]

            # Add selected vertices to the vertex group
            for v in o.data.vertices:
                if v.select:
                    vg.add([v.index], 1.0, "REPLACE")
            bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}


class SP_OT_remove_from_ellipses(bpy.types.Operator):
    bl_idname = "object.sp_remove_from_ellipses"
    bl_label = "SP - Remove from Ellipses"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = context.objects_in_mode
        for o in objs:
            bpy.ops.object.mode_set(mode="OBJECT")
            # Ensure "Endpoints" vertex group exists
            if "Ellipse" in o.vertex_groups:
                vg = o.vertex_groups["Ellipse"]

                # Remove selected vertices to the vertex group
                for v in o.data.vertices:
                    if v.select:
                        vg.remove([v.index])
            bpy.ops.object.mode_set(mode="EDIT")
        return {"FINISHED"}


class SP_OT_add_trim_contour(bpy.types.Operator):
    bl_idname = "mesh.sp_add_trim_contour"
    bl_label = "SP - Add Trim Contour"
    bl_description = "Add a trim contour to selected patch"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # set mode
        original_mode = context.mode
        if original_mode == "EDIT_MESH":
            selected_objects = context.objects_in_mode
        else:
            selected_objects = context.selected_objects

        # loop through selection
        for o in selected_objects:
            # check if supported object
            is_patch = False
            if original_mode == "EDIT_MESH":
                bpy.ops.object.mode_set(mode="OBJECT")

            for m in o.modifiers:
                if m.type == "NODES" and m.node_group.name[:5] == "SP - ":
                    is_patch = True
                    break

            # add contour
            if o.type == "MESH" and is_patch:
                self.add_square_inside_mesh(context, o)

        # Restore the original mode
        if original_mode == "EDIT_MESH":
            original_mode = "EDIT"
        bpy.ops.object.mode_set(mode=original_mode)

        return {"FINISHED"}

    def add_square_inside_mesh(self, context, obj):

        # Ensure the object is active and enter Edit mode
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode="EDIT")

        # Create bmesh from the object
        bm = bmesh.from_edit_mesh(obj.data)

        # Create vertices of the square
        verts = [
            bm.verts.new(Vector((0, 0, 0))),
            bm.verts.new(Vector((1, 0, 0))),
            bm.verts.new(Vector((1, 1, 0))),
            bm.verts.new(Vector((0, 1, 0))),
        ]

        # Create edges
        bm.edges.new(verts[0:2])
        bm.edges.new(verts[1:3])
        bm.edges.new(verts[2:])
        bm.edges.new([verts[3], verts[0]])

        # Update the mesh
        bmesh.update_edit_mesh(obj.data)

        # Ensure the new vertices are selected
        for vert in verts:
            vert.select = True

        # Assign to Trim contour groups

        # Switch to object mode to modify vertex groups
        bpy.ops.object.mode_set(mode="OBJECT")

        # Add attributes
        add_bool_attribute(
            obj, "Trim Contour", [False] * (len(obj.data.vertices) - 4) + [True] * 4
        )
        add_bool_attribute(
            obj, "Endpoints", [False] * (len(obj.data.vertices) - 4) + [True] * 4
        )


class SP_OT_toggle_trim_contour_belonging(bpy.types.Operator):
    bl_idname = "mesh.sp_toggle_trim_contour_belonging"
    bl_label = "SP - Toggle Trim Contour Belonging"
    bl_description = "Toggle selection as part of the patch trim contour"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        att_name = "Trim Contour"
        objs = context.objects_in_mode
        bpy.ops.object.mode_set(mode="OBJECT")
        for o in objs:
            if att_name in o.data.attributes:
                if not toggle_bool_attribute(o, att_name):
                    if not toggle_pseudo_bool_attribute(o, att_name):
                        o.data.attributes.new(
                            name=att_name, type="BOOLEAN", domain="POINT"
                        )
                        o.data.update()

            # Vertex group (LEGACY)
            elif att_name in o.vertex_groups:
                toggle_pseudo_bool_vertex_group(o, att_name)
            else:
                o.data.attributes.new(name=att_name, type="BOOLEAN", domain="POINT")
                o.data.update()
        bpy.ops.object.mode_set(mode="EDIT")

        return {"FINISHED"}


class SP_OT_select_trim_contour(bpy.types.Operator):
    """Select vertices marked as segment ends"""

    bl_idname = "mesh.sp_select_trim_contour"
    bl_label = "SP - Select Trim Contour"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objects = context.objects_in_mode
        bpy.ops.object.mode_set(mode="OBJECT")
        select_by_attriute("Trim Contour", objects)
        bpy.ops.object.mode_set(mode="EDIT")

        return {"FINISHED"}


def show_combs(self, context):
    objects = [ob for ob in context.selected_objects]
    for o in objects:
        for m in o.modifiers:
            if m.type == "NODES" and m.node_group.name[:5] == "SP - ":
                if "Combs" in m.node_group.interface.items_tree.keys():
                    for it in m.node_group.interface.items_tree[
                        "Combs"
                    ].interface_items:
                        if (
                            it.name in ["Combs", "U", "V"]
                            and it.socket_type == "NodeSocketBool"
                        ):
                            input_id = it.identifier
                            m[input_id] = self.combs_on
                    m.node_group.interface_update(context)
                    break


def scale_combs(self, context):
    objects = [ob for ob in context.selected_objects]
    for o in objects:
        for m in o.modifiers:
            if m.type == "NODES" and m.node_group.name[:5] == "SP - ":
                if "Combs" in m.node_group.interface.items_tree.keys():
                    for it in m.node_group.interface.items_tree[
                        "Combs"
                    ].interface_items:
                        if it.name == "Scale" and it.socket_type == "NodeSocketFloat":
                            input_id = it.identifier
                            m[input_id] = self.combs_scale
                    m.node_group.interface_update(context)
                    break


def set_seg_degree_from_active_prop(self, context):
    set_seg_degree(min(self.active_segment_degree, 20), context)


def set_seg_degree(degree: int, context):
    objs = context.objects_in_mode
    for o in objs:
        # Switch to object mode to modify vertex groups
        bpy.ops.object.mode_set(mode="OBJECT")

        # Ensure "Degree" exists
        if "Degree" not in o.data.attributes:
            o.data.attributes.new(name="Degree", type="INT", domain="POINT")

        # Get existing values
        att = o.data.attributes["Degree"]
        values = [0] * len(o.data.vertices)
        att.data.foreach_get("value", values)

        # Update values
        for i, v in enumerate(o.data.vertices):
            if v.select:
                values[i] = max(degree, 0)
                # To improve one day to change all verts between endpoints

        # Set new
        att.data.foreach_set("value", values)
        bpy.ops.object.mode_set(mode="EDIT")


def set_vert_weight_from_active_prop(self, context):
    set_vert_weight(self.active_vert_weight, context)


def set_vert_weight(weight: float, context):
    objs = context.objects_in_mode
    for o in objs:
        bpy.ops.object.mode_set(mode="OBJECT")
        p_count = len(o.data.vertices)

        val = [1.0] * p_count
        if "Weight" not in o.data.attributes:
            o.data.attributes.new(name="Weight", type="FLOAT", domain="POINT")
        else:
            o.data.attributes["Weight"].data.foreach_get("value", val)

        for i, v in enumerate(o.data.vertices):
            if v.select:
                val[i] = weight

        o.data.attributes["Weight"].data.foreach_set("value", val)
        bpy.ops.object.mode_set(mode="EDIT")


class SP_Props_Group(bpy.types.PropertyGroup):

    combs_scale: bpy.props.FloatProperty(
        name="Combs Scale",
        description="Curvature Combs Scale",
        default=0.1,
        min=0,
        update=scale_combs,
        precision=7,
    )

    combs_on: bpy.props.BoolProperty(
        name="Combs on",
        description="Curvature Combs Scale",
        default=False,
        update=show_combs,
    )

    active_segment_degree: bpy.props.IntProperty(
        name="Degree",
        description="Segment Degree. Change it by selecting the first point of the segment (try both ends to know which one is the first)",
        default=3,
        min=0,
        max=10,
        update=set_seg_degree_from_active_prop,
    )

    active_vert_weight: bpy.props.FloatProperty(
        name="Weight",
        description="Control point weight of rational spline",
        default=1.0,
        min=0,
        update=set_vert_weight_from_active_prop,
    )


class SP_OT_set_segment_degree(bpy.types.Operator):
    bl_idname = "object.sp_set_segment_degree"
    bl_label = "SP - Set Segment Degree"
    bl_options = {"REGISTER", "UNDO"}

    # Properties to store the current value
    degree: bpy.props.IntProperty(
        name="Degree", default=2, description="Degree attribute assigned to selection"
    )

    def modal(self, context, event):
        # Handle scroll wheel events
        if event.type == "WHEELDOWNMOUSE":
            self.degree += 1
            set_seg_degree(self.degree, context)
            context.area.header_text_set(f"Degree: {self.degree}")
            context.view_layer.update()
            return {"RUNNING_MODAL"}

        elif event.type == "WHEELUPMOUSE":
            if self.degree > 0:
                self.degree -= 1
                set_seg_degree(self.degree, context)
                context.area.header_text_set(f"Degree: {self.degree}")
                context.view_layer.update()
                return {"RUNNING_MODAL"}

        # Exit conditions
        elif event.type in {"RIGHTMOUSE", "ESC"}:
            return {"CANCELLED"}

        elif event.type == "LEFTMOUSE":
            return {"FINISHED"}

        # Pass through other events
        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        if context.object is None or context.object.type != "MESH":
            return {"CANCELLED"}

        # Add modal handler
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}


class SP_OT_set_spline(bpy.types.Operator):
    bl_idname = "mesh.sp_set_spline"
    bl_label = "SP - Set Spline"
    bl_options = {"REGISTER", "UNDO"}

    degree: bpy.props.IntProperty(
        name="Degree",
        default=2,
        min=0,
        description="Degree attribute assigned to selection",
    )
    weight: bpy.props.FloatProperty(
        name="Weight",
        default=1.0,
        min=0.0,
        description="Weight attribute assigned to selection",
    )

    def modal(self, context, event):
        # Handle scroll wheel events
        if event.type == "WHEELUPMOUSE":
            self.degree += 1
            set_seg_degree(self.degree, context)
            context.area.header_text_set(f"Degree: {self.degree}")
            context.view_layer.update()
            return {"RUNNING_MODAL"}
        elif event.type == "WHEELDOWNMOUSE":
            if self.degree > 0:
                self.degree -= 1
                set_seg_degree(self.degree, context)
                context.area.header_text_set(f"Degree: {self.degree}")
                context.view_layer.update()
                return {"RUNNING_MODAL"}

        # Exit conditions
        elif event.type in {"RIGHTMOUSE", "ESC"}:
            return {"CANCELLED"}

        elif event.type == "LEFTMOUSE":
            return {"FINISHED"}

        # Pass through other events
        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        if context.object is None or context.object.type != "MESH":
            return {"CANCELLED"}

        set_segment_type(context, 0)
        self.initial_mouse_x = event.mouse_x
        self.initial_mouse_y = event.mouse_y

        # Add modal handler
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def execute(self, context):
        set_seg_degree(self.degree, context)
        set_vert_weight(self.weight, context)
        return {"FINISHED"}


class SP_OT_add_oriented_empty(bpy.types.Operator):
    bl_idname = "object.sp_add_oriented_empty"
    bl_label = "SP - Add Oriented Empty"
    bl_description = "Add oriented empty from 3 vertices"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if context.mode == "EDIT_MESH":
            obj = context.objects_in_mode[0]
            bm = bmesh.from_edit_mesh(obj.data)

            # Get selected vertices
            selected_verts = [v for v in bm.verts if v.select]

            if len(selected_verts) < 3:
                self.report({"INFO"}, "Select 3 vertices")
                return {"CANCELLED"}

            # Get the first three selected vertices
            v1, v2, v3 = selected_verts[:3]

            # For display later
            longest_length = (
                max(
                    max((v1.co - v2.co).length, (v2.co - v3.co).length),
                    (v3.co - v1.co).length,
                )
            ) / 1.9

            # Calculate the centroid of the triangle
            centroid = (v1.co + v2.co + v3.co) / 3

            # Calculate the normal of the triangle
            normal = (v2.co - v1.co).cross(v3.co - v1.co).normalized()

            # Calculate the rotation matrix to align the empty's Z-axis with the normal
            z_axis = normal
            x_axis = (v2.co - v1.co).normalized()
            y_axis = z_axis.cross(x_axis).normalized()

            rotation_matrix = Matrix((x_axis, y_axis, z_axis)).transposed()

            # Create the empty
            bpy.ops.object.mode_set(mode="OBJECT")
            empty = bpy.data.objects.new("OrientedEmpty", None)
            context.collection.objects.link(empty)

            # Set the empty's location and rotation
            empty.location = centroid
            empty.rotation_mode = "QUATERNION"
            empty.rotation_quaternion = rotation_matrix.to_quaternion()

            # Force update the object's transformation matrices
            context.view_layer.update()
            empty.matrix_world = obj.matrix_world @ empty.matrix_world

            # Empty display
            empty.empty_display_type = "CUBE"
            empty.empty_display_size = longest_length
            empty.scale = Vector((1.0, 1.0, 0.01))

        return {"FINISHED"}


class SP_OT_blend_surfaces(bpy.types.Operator):
    bl_idname = "object.sp_blend_surfaces"
    bl_label = "SP - Blend Surfaces"
    bl_description = "Add a blend surface between the selected surfaces"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Add a check if SP surfaces ?

        if len(context.selected_objects) < 2:
            self.report({"INFO"}, "Select 2 surfaces")
            return {"CANCELLED"}
        else:
            surf1 = context.selected_objects[0]
            surf2 = context.selected_objects[1]
            loc = surf1.location / 2 + surf2.location / 2

            mesh = bpy.data.meshes.new("Blend Patch")
            blend_surf = bpy.data.objects.new("Blend Patch", mesh)
            blend_surf.location = loc
            context.collection.objects.link(blend_surf)

            # Add blend modifier
            add_sp_modifier(
                blend_surf,
                "SP - Blend Surfaces",
                {
                    "Target 1": surf1,
                    "Target 2": surf2,
                    "Auto": True,
                    "Continuity": 3,
                },
                append=True,
            )

            # Add meshing modifier
            add_sp_modifier(
                blend_surf,
                "SP - Bezier Patch Meshing",
                append=True,
            )

        return {"FINISHED"}


class SP_OT_flip_normals(bpy.types.Operator):
    bl_idname = "object.sp_flip_normals"
    bl_label = "SP - Flip Normals"
    bl_description = "Flip normals of selected surfaces"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        for o in context.selected_objects:
            flip_node_socket_bool(o, ["Flip Normal", "Flip Normals"], context)
        return {"FINISHED"}


class SP_OT_enable_exact_normals(bpy.types.Operator):
    bl_idname = "object.sp_enable_exact_normals"
    bl_label = "SP - Enable Exact Normals"
    bl_description = "Enable exact normals on selected surfaces"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        for o in context.selected_objects:
            change_node_socket_value(
                o, True, ["Exact Normals", "Exact Normal"], "NodeSocketBool", context
            )
        return {"FINISHED"}


class SP_OT_disable_exact_normals(bpy.types.Operator):
    bl_idname = "object.sp_disable_exact_normals"
    bl_label = "SP - Disable Exact Normals"
    bl_description = "Disable exact normals on selected surfaces"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        for o in context.selected_objects:
            change_node_socket_value(
                o, False, ["Exact Normals", "Exact Normal"], "NodeSocketBool", context
            )
        return {"FINISHED"}


class SP_OT_explode_compound(bpy.types.Operator):
    bl_idname = "object.sp_explode_compound"
    bl_label = "SP - Explode Compound"
    bl_description = "Convert selected compounds to individual patches"
    bl_options = {"REGISTER", "UNDO"}

    keep_original: bpy.props.BoolProperty(name="Keep Original", default=True)

    def execute(self, context):
        for o in context.selected_objects:
            if sp_type_of_object(o) == SP_obj_type.COMPOUND:
                new_objects = convert_compound_to_patches(o, context, resolution=16)

                # Create collection
                collection = bpy.data.collections.new(f"{o.name} Exploded")
                context.scene.collection.children.link(collection)
                
                # Create objects from extracted data
                for o_new in new_objects:
                    collection.objects.link(o_new)

                new_objects.clear()

        if not self.keep_original:
            bpy.ops.object.delete(use_global=False)

        return {"FINISHED"}


class SP_OT_mesh_to_compound(bpy.types.Operator):
    bl_idname = "object.sp_mesh_to_compound"
    bl_label = "SP - Mesh to Compound"
    bl_description = (
        "Convert selected mesh objects to SP compounds. Each polygon becomes a patch."
    )
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        for o in context.selected_objects:
            if o.type == "MESH" and sp_type_of_object(o) == None:
                add_sp_modifier(o, "SP - Poly to Compound", append=True)
                add_sp_modifier(o, "SP - Compound Meshing", pin=True, append=True)
        return {"FINISHED"}

    def invoke(self, context, event):
        for o in context.selected_objects:
            if o.type == "MESH" and sp_type_of_object(o) == None:
                ob = o.evaluated_get(context.evaluated_depsgraph_get())
                if len(ob.data.polygons) > 5000:
                    return context.window_manager.invoke_props_dialog(self)
        return self.execute(context)

    def draw(self, context):
        layout = self.layout
        layout.label(text="More than 5000 polygons will each become an SP patch.") 
        layout.label(text="Proceed anyway ?")


class SP_OT_add_curvature_analysis(bpy.types.Operator):
    bl_idname = "object.sp_add_curvature_analysis"
    bl_label = "SP - Add Curvature Analysis"
    bl_description = "Add curvature analysis modifier to selected surfaces"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        for o in context.selected_objects:
            if o.type == 'MESH':
                sp_surf = False
                for m in o.modifiers:
                    if m.node_group.name in [MESHER_NAMES[SP_obj_type.BSPLINE_SURFACE], MESHER_NAMES[SP_obj_type.BEZIER_SURFACE]]:
                        sp_surf = True
                        break

                if not sp_surf:
                    continue

                pinned_mods = []
                for m in o.modifiers:
                    if m.use_pin_to_last :
                        m.use_pin_to_last = False
                        pinned_mods.append(m)


                add_sp_modifier(o, "SP - Curvature Analysis", append=True, pin=True)

                for m in pinned_mods:
                    m.use_pin_to_last = True
                
                if "Color" not in o.data.color_attributes:
                    o.data.color_attributes.new(
                        name="Color",
                        type='BYTE_COLOR',  # or 'FLOAT_COLOR'
                        domain='POINT'      # or 'CORNER'
                    )
            
        bpy.context.space_data.shading.color_type = 'VERTEX'


        return {"FINISHED"}


classes = [
    SP_OT_add_curvature_analysis,
    SP_OT_add_library,
    SP_OT_add_oriented_empty,
    SP_OT_add_trim_contour,
    SP_OT_assign_as_ellipse,
    SP_OT_bl_nurbs_to_psychopatch,
    SP_OT_blend_surfaces,
    SP_OT_explode_compound,
    SP_OT_flip_normals,
    SP_OT_psychopatch_to_bl_nurbs,
    SP_OT_remove_from_ellipses,
    SP_OT_replace_node_group,
    SP_OT_select_all,
    SP_OT_select_endpoints,
    SP_OT_select_trim_contour,
    SP_OT_select_visible_curves,
    SP_OT_select_visible_surfaces,
    SP_OT_set_segment_degree,
    SP_OT_set_segment_type,
    SP_OT_set_spline,
    SP_OT_toggle_control_geom,
    SP_OT_toggle_endpoints,
    SP_OT_toggle_trim_contour_belonging,
    SP_OT_update_modifiers,
    SP_Props_Group,
    SP_OT_disable_exact_normals,
    SP_OT_enable_exact_normals,
    SP_OT_mesh_to_compound,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.sp_properties = bpy.props.PointerProperty(type=SP_Props_Group)


def unregister():
    del bpy.types.Scene.sp_properties
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
