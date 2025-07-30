import bpy
import bmesh
from ..utils import *
from mathutils import Vector

from pathlib import Path
from os.path import dirname, abspath, join
import platform
from ..exporter.export_process_svg import *

os = platform.system()

from ..importer.import_shape_to_blender_object import *
from ..exporter.export_process_cad import *

class SP_OT_add_NURBS_patch(bpy.types.Operator):
    bl_idname = "object.sp_add_nurbs_patch"
    bl_label = "Add NURBS PsychoPatch"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        append_object_by_name("NURBS Patch", context)
        return {"FINISHED"}


class SP_OT_add_bezier_patch(bpy.types.Operator):
    bl_idname = "object.sp_add_bezier_patch"
    bl_label = "Add Bezier Patch"
    bl_options = {"REGISTER", "UNDO"}

    degree_u: bpy.props.IntProperty(
        name="Degree U",
        description="Number of control points in U direction -1",
        default=1,
        min=1,
    )

    degree_v: bpy.props.IntProperty(
        name="Degree V",
        description="Number of control points in V direction -1",
        default=1,
        min=1,
    )

    def execute(self, context):
        mesh = bpy.data.meshes.new(name="Grid")
        self.obj = bpy.data.objects.new("Bezier Patch", mesh)

        # Create a new bmesh
        self.bm = bmesh.new()

        # divide grid
        step_x = 2 / self.degree_v
        step_y = 2 / self.degree_u

        # Create vertices
        for i in range(self.degree_u + 1):
            for j in range(self.degree_v + 1):
                x = j * step_x - 1  # Subtract 1 to center
                y = i * step_y - 1  # Subtract 1 to center
                self.bm.verts.new((x, y, 0))

        self.bm.verts.ensure_lookup_table()

        # Create faces
        for i in range(self.degree_u):
            for j in range(self.degree_v):
                v1 = self.bm.verts[i * (self.degree_v + 1) + j]
                v2 = self.bm.verts[i * (self.degree_v + 1) + j + 1]
                v3 = self.bm.verts[(i + 1) * (self.degree_v + 1) + j + 1]
                v4 = self.bm.verts[(i + 1) * (self.degree_v + 1) + j]
                self.bm.faces.new((v1, v2, v3, v4))

        # Update bmesh
        self.bm.to_mesh(mesh)
        self.bm.free()

        # # set smooth
        values = [True] * len(mesh.polygons)
        mesh.polygons.foreach_set("use_smooth", values)

        # Update mesh
        mesh.update()

        # Link the object to the scene
        bpy.context.collection.objects.link(self.obj)

        add_sp_modifier(self.obj, "SP - Reorder Grid Index", add_mode=True)
        add_sp_modifier(
            self.obj,
            "SP - Connect Bezier Patch",
            {"Continuity Level": 3},
            add_mode=True,
        )
        add_sp_modifier(self.obj, "SP - Bezier Patch Meshing", pin=True, add_mode=True)

        # Set object location to 3D cursor
        self.obj.location = bpy.context.scene.cursor.location

        # Select the new object and make it active
        bpy.ops.object.select_all(action="DESELECT")
        self.obj.select_set(True)
        bpy.context.view_layer.objects.active = self.obj

        return {"FINISHED"}


class SP_OT_add_flat_patch(bpy.types.Operator):
    bl_idname = "object.sp_add_flat_patch"
    bl_label = "Add flat PsychoPatch"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        append_object_by_name("FlatPatch", context)
        return {"FINISHED"}


class SP_OT_add_curve(bpy.types.Operator):
    bl_idname = "object.sp_add_curve"
    bl_label = "Add PsychoCurve"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        append_object_by_name("PsychoCurve", context)
        return {"FINISHED"}


class SP_OT_add_library(bpy.types.Operator):
    bl_idname = "object.sp_add_library"
    bl_label = "Add Library"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # create lib
        asset_lib_path = join(dirname(dirname(abspath(__file__))), "assets")
        paths = [a.path for a in bpy.context.preferences.filepaths.asset_libraries]
        if asset_lib_path not in paths:
            bpy.ops.preferences.asset_library_add(directory=asset_lib_path)

        # Rename lib
        asset_library = bpy.context.preferences.filepaths.asset_libraries.get("assets")
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


class SP_OT_select_visible_curves(bpy.types.Operator):
    bl_idname = "object.sp_select_visible_curves"
    bl_label = "SP - Select Visible Curves"
    bl_description = "Select Visible Curves"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objects = [ob for ob in context.visible_objects]
        for o in objects:
            for m in o.modifiers:
                if (
                    m.type == "NODES"
                    and m.node_group is not None
                    and m.node_group.name[:-4]
                    in [
                        "SP - Mesh Bezier Chain",
                        "SP - Bezier Curve Any Order",
                        "SP - Mesh Bezier Chain",
                        "SP - Bezier Curve Any Order",
                        "SP - Curve Meshing",
                        "SP - Mesh Bezier C",
                        "SP - Bezier Curve Any O",
                        "SP - Mesh Bezier C",
                        "SP - Bezier Curve Any O",
                        "SP - Curve Mes",
                    ]
                ):
                    o.select_set(True)
                    break
        return {"FINISHED"}


class SP_OT_select_visible_surfaces(bpy.types.Operator):
    bl_idname = "object.sp_select_visible_surfaces"
    bl_label = "SP - Select Visible Surfaces"
    bl_description = "Select Visible Surfaces"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objects = [ob for ob in context.visible_objects]
        for o in objects:
            for m in o.modifiers:
                if (
                    m.type == "NODES"
                    and m.node_group is not None
                    and m.node_group.name[:-4]
                    in [
                        "SP - Bezier Patch Meshing",
                        "SP - Any Order Patch Meshing",
                        "SP - Bicubic Patch Meshing",
                        "SP - Mesh Flat patch",
                        "SP - Patch meshing",
                        "SP - FlatPatch Meshing" "SP - Bezier Patch Mes",
                        "SP - Any Order Patch Mes",
                        "SP - Bicubic Patch Mes",
                        "SP - Mesh Flat p",
                        "SP - Patch mes",
                        "SP - FlatPatch Mes",
                    ]
                ):
                    o.select_set(True)
                    break
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
    bl_description = "For updating old assets. Replaces all instance of a modifier with another"
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
    bl_label = "Convert Psychopatches to internal NURBS"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object.type == "MESH"

    def execute(self, context):
        spline_index = -1
        for o in context.selected_objects:
            sp_type = sp_type_of_object(o, context)
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


def append_object_from_assets(object_name: str, context: bpy.types.Context):
    """
    Find the 'assets/assets.blend' file relative to the root of this addon
    and import an object by name.
    """
    try:
        addon_root_path = Path(__file__).parent.parent
    except NameError:
        if bpy.data.filepath:
            addon_root_path = Path(bpy.data.filepath).parent
        else:
            print("Error: The script path cannot be determined. Please save the .blend file or install the add-on.")
            return None

    filepath = addon_root_path / "assets" / "assets.blend"

    if not filepath.exists():
        print(f"Asset Error: File not found in expected path: {filepath}")
        return None

    with bpy.data.libraries.load(str(filepath), link=False) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects = [object_name]
        else:
            print(f"Asset Error: The object '{object_name}' does not exist in {filepath}")
            return None

    if data_to.objects:
        imported_obj = data_to.objects[0]
        context.collection.objects.link(imported_obj)
        return imported_obj

    return None

class SP_OT_bl_nurbs_to_psychopatch(bpy.types.Operator):
    """
    Convert NURBS surfaces to Psychopatches using templates
    with Geometry Nodes from an external asset file.
    """
    bl_idname = "object.sp_bl_nurbs_to_psychopatch"
    bl_label = "Convert NURBS to Psychopatch"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if not context.active_object:
            return False
        return any(o.type == 'SURFACE' for o in context.selected_objects)

    def execute(self, context):
        obj_to_convert = [o for o in context.selected_objects if o.type == "SURFACE"]
        if not obj_to_convert:
            self.report({'WARNING'}, "No selected surface objects (NURBS) were found.")
            return {'CANCELLED'}
        
        collection = context.collection or context.scene.collection

        def get_or_create_template(name):
            if name in bpy.data.objects:
                return bpy.data.objects[name], False

            template_obj = append_object_from_assets(name, context)
            if template_obj:
                template_obj.hide_viewport = True
                template_obj.hide_render = True
                template_obj.select_set(False)
                return template_obj, True
            return None, False
        
        bezier_template, created_bezier = get_or_create_template("Bezier Patch")
        bspline_template, created_bspline = get_or_create_template("NURBS Patch")

        if not bezier_template or not bspline_template:
            self.report({'ERROR'}, "The templates could not be loaded from assets.blend. Check the console.")
            if created_bezier and bezier_template: bpy.data.objects.remove(bezier_template)
            if created_bspline and bspline_template: bpy.data.objects.remove(bspline_template)
            return {'CANCELLED'}

        new_patches = []
        bpy.ops.object.select_all(action='DESELECT')

        for obj in obj_to_convert:
            for spline in obj.data.splines:
                is_bezier = spline.use_bezier_u and spline.use_bezier_v
                control_points = []
                
                if is_bezier:
                    for bp in spline.bezier_points:
                        control_points.extend([bp.handle_left, bp.co, bp.handle_right])
                else:
                    for p in spline.points:
                        control_points.append(Vector(p.co[0:3]))
                
                u_count = spline.order_u
                v_count = len(control_points) // u_count
                
                faces = [
                    (v * u_count + u, (v + 1) * u_count + u, (v + 1) * u_count + u + 1, v * u_count + u + 1)
                    for v in range(v_count - 1) for u in range(u_count - 1)
                ]

                mesh = bpy.data.meshes.new(name="Psychopatch_Mesh")
                if control_points and faces:
                    mesh.from_pydata(control_points, [], faces)
                    mesh.update()

                template_to_use = bezier_template if is_bezier else bspline_template
                new_obj = template_to_use.copy()
                new_obj.data = mesh
                new_obj.animation_data_clear()
                new_obj.matrix_world = obj.matrix_world
                collection.objects.link(new_obj)

                new_obj.hide_viewport = False
                new_obj.hide_render = False
                new_obj.select_set(True)
                new_patches.append(new_obj)
        
        if new_patches:
            context.view_layer.objects.active = new_patches[-1]

        if created_bezier and bezier_template.name in bpy.data.objects:
            bpy.data.objects.remove(bezier_template)
        if created_bspline and bspline_template.name in bpy.data.objects:
            bpy.data.objects.remove(bspline_template)

        self.report({'INFO'}, f" {len(new_patches)} patches were converted.")
        return {'FINISHED'}




class SP_OT_toggle_endpoints(bpy.types.Operator):
    """Mark or unmark selected vertices as endpoint depending on the active vertex"""

    bl_idname = "mesh.sp_toggle_endpoints"
    bl_label = "Toggle Endpoints"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        att_name = "Endpoints"
        objs = context.objects_in_mode
        bpy.ops.object.mode_set(mode="OBJECT")
        for o in objs:
            if att_name in o.data.attributes:
                if not toggle_bool_attribute(o, att_name):
                    if not toggle_pseudo_bool_attribute(o, att_name) :
                        o.data.attributes.new(name=att_name, type="BOOLEAN", domain="POINT")
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
    bl_label = "Select Endpoints"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = context.objects_in_mode
        bpy.ops.object.mode_set(mode="OBJECT")
        for o in objs:
            # Attribute
            if "Endpoints" in o.data.attributes:
                att_type = o.data.attributes["Endpoints"].data_type
                if att_type == "FLOAT":
                    weights = read_attribute_by_name(o, "Endpoints")
                    for v in o.data.vertices:
                        weight = weights[v.index]
                        v.select = weight > 0.6
                elif att_type == "BOOLEAN":
                    weights = read_attribute_by_name(o, "Endpoints")
                    for v in o.data.vertices:
                        v.select = weights[v.index]

            # Vertex group
            elif "Endpoints" in o.vertex_groups:
                vertex_group = o.vertex_groups["Endpoints"]
                for v in o.data.vertices:
                    try:
                        weight = vertex_group.weight(v.index)
                        v.select = weight > 0.6
                    except RuntimeError:
                        # Vertex is not in the group, skip it
                        pass
                    
            bpy.ops.object.mode_set(mode="EDIT")

        return {"FINISHED"}


class SP_OT_set_segment_type(bpy.types.Operator):
    """Mark segment type for selection"""

    bl_idname = "mesh.sp_set_segment_type"
    bl_label = "Set Segment Type"
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
    bl_label = "Assign as Ellipse"
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
    bl_label = "Remove from Ellipses"
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
    bl_idname = "object.sp_add_trim_contour"
    bl_label = "Add Trim Contour"
    bl_description = "Add a trim contour to selected patch"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # set mode
        original_mode = bpy.context.mode
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
        bpy.context.view_layer.objects.active = obj
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
        add_bool_attribute(obj, "Trim Contour", [False] * (len(obj.data.vertices) - 4) + [True]*4)
        add_bool_attribute(obj, "Endpoints", [False] * (len(obj.data.vertices) - 4) + [True]*4)


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
                            it.name in ["Enable", "U", "V"]
                            and it.socket_type == "NodeSocketBool"
                        ):
                            input_id = it.identifier
                            m[input_id] = self.combs_on
                    m.node_group.interface_update(context)


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
    bl_label = "Set Segment Degree"
    bl_options = {"REGISTER", "UNDO"}

    # Properties to store the current value
    degree: bpy.props.IntProperty(
        name="Degree", default=2, description="Degree attribute assigned to selection"
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

        # Add modal handler
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}


class SP_OT_set_spline(bpy.types.Operator):
    bl_idname = "mesh.sp_set_spline"
    bl_label = "Set Spline"
    bl_options = {"REGISTER", "UNDO"}

    degree: bpy.props.IntProperty(
        name="Degree", default=2, min=0, description="Degree attribute assigned to selection"
    )
    weight: bpy.props.FloatProperty(
        name="Weight", default=1.0, min = 0.0, description="Weight attribute assigned to selection"
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
    bl_label = "Add Oriented Empty"
    bl_description = "Add oriented empty from 3 vertices"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if bpy.context.mode == "EDIT_MESH":
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
            bpy.context.collection.objects.link(empty)

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


classes = [
    SP_OT_add_NURBS_patch,
    SP_OT_add_bezier_patch,
    SP_OT_add_curve,
    SP_OT_add_flat_patch,
    SP_OT_add_library,
    SP_OT_add_oriented_empty,
    SP_OT_add_trim_contour,
    SP_OT_set_segment_type,
    SP_OT_assign_as_ellipse,
    SP_OT_toggle_endpoints,
    SP_OT_bl_nurbs_to_psychopatch,
    SP_OT_psychopatch_to_bl_nurbs,
    SP_OT_remove_from_ellipses,
    SP_OT_select_visible_curves,
    SP_OT_select_visible_surfaces,
    SP_OT_toggle_control_geom,
    SP_OT_select_endpoints,
    SP_OT_update_modifiers,
    SP_OT_replace_node_group,
    SP_Props_Group,
    SP_OT_set_segment_degree,
    SP_OT_set_spline,
]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.sp_properties = bpy.props.PointerProperty(type=SP_Props_Group)


def unregister():
    del bpy.types.Scene.sp_properties
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
