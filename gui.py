##############################
##            GUI           ##
##############################
import bpy
import platform

os = platform.system()
from .tools import macros
from .importer import import_operator
from .exporter import export_operator
from .importer.import_operator import SP_OT_ImportCAD
from .exporter.export_operator import (
    SP_OT_ExportStep,
    SP_OT_ExportIges,
    SP_OT_ExportSvg,
)

# from .macros import SP_Props_Group
from .importer.import_process_pipeline import *
from .importer.import_shape_to_blender_object import *


class SP_PT_MainPanel(bpy.types.Panel):
    bl_idname = "SP_PT_MainPanel"
    bl_label = "Surface Psycho"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw(self, context):
        if context.mode == "OBJECT":
            row = self.layout.row()
            row.scale_y = 2.0
            row.operator(
                "object.sp_quick_export", text="Quick .STEP Export", icon="EXPORT"
            )

            # Toggle control geom
            row = self.layout.row()
            row.operator(
                "object.sp_toggle_control_geom",
                text="Toggle Control Geometry",
                icon="OUTLINER_DATA_LATTICE",
            )

        # Combs
        self.layout.use_property_split = True
        self.layout.use_property_decorate = False
        heading = self.layout.column(align=True, heading="Combs")
        row = heading.row(align=True)
        row.prop(context.scene.sp_properties, "combs_on", text="")
        sub = row.row()
        sub.active = context.scene.sp_properties.combs_on
        sub.prop(context.scene.sp_properties, "combs_scale", text="")

        if context.mode == "OBJECT":
            # Select all
            row = self.layout.row()
            row.label(text="Select Visible")
            sub = row.row(align=True)
            sub.operator(
                "object.sp_select_visible_curves",
                text="Curves",
                icon="OUTLINER_OB_CURVE",
            )
            sub.operator(
                "object.sp_select_visible_surfaces",
                text="Surfaces",
                icon="OUTLINER_OB_SURFACE",
            )

            # Replace node group
            row = self.layout.row()
            row.operator(
                "object.sp_replace_node_group",
                text="Replace Node Group",
                icon="UV_SYNC_SELECT",
            )


class SP_PT_EditPanel(bpy.types.Panel):
    bl_idname = "SP_PT_EditPanel"
    bl_parent_id = "SP_PT_MainPanel"
    bl_label = "Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Surface Psycho"

    def draw(self, context):
        if context.mode == "OBJECT" or context.mode == "EDIT_MESH":
            row = self.layout.row()
            row.operator(
                "object.sp_add_trim_contour",
                text="Add Trim Contour",
                icon="MOD_MESHDEFORM",
            )

        if context.mode == "EDIT_MESH":
            # Endpoints
            row = self.layout.row()
            row.label(text="Endpoints")
            sub = row.row(align=True)
            sub.operator("object.sp_toggle_endpoints", text="Toggle")
            sub.operator("object.sp_select_endpoints", text="Select")

            # Type
            row = self.layout.row()
            row.operator(
                "object.sp_set_segment_type", text="Spline", icon="MOD_CURVE"
            ).type = "spline"

            row = self.layout.row()
            sub = row.row(align=True)
            sub.operator(
                "object.sp_set_segment_type", text="Circle", icon="MESH_CIRCLE"
            ).type = "circle"
            sub.operator(
                "object.sp_set_segment_type", text="Arc", icon="SPHERECURVE"
            ).type = "circle_arc"

            row = self.layout.row()
            sub = row.row(align=True)
            sub.operator(
                "object.sp_set_segment_type", text="Ellipse", icon="MESH_CAPSULE"
            ).type = "ellipse"
            sub.operator(
                "object.sp_set_segment_type", text="Arc", icon="INVERSESQUARECURVE"
            ).type = "ellipse_arc"

            # Segment Degree
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            col = self.layout.column()
            col.prop(
                context.scene.sp_properties,
                "active_segment_degree",
                text="NURBS Degree",
            )

            # Weight
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            col = self.layout.column()
            col.prop(context.scene.sp_properties, "active_vert_weight", text="Weight")


class SP_MT_PIE_SegmentEdit(bpy.types.Menu):
    bl_label = "SP Segment Type"

    def draw(self, context):
        if context.mode == "EDIT_MESH":
            layout = self.layout
            pie = layout.menu_pie()
            # Pie order: west, east, south, north, north-west, north-east, south-west, south-east
            pie.operator(
                "object.sp_set_segment_type", text="Circle", icon="MESH_CIRCLE"
            ).type = "circle"  # West
            pie.operator(
                "object.sp_set_segment_type", text="Ellipse", icon="MESH_CAPSULE"
            ).type = "ellipse"  # East
            pie.operator("object.sp_toggle_endpoints", text="Toggle Endpoints")  # South
            pie.operator(
                "object.sp_set_spline", text="Spline", icon="RNDCURVE"
            )  # North
            pie.operator(
                "object.sp_set_segment_type", text="Circle Arc", icon="SPHERECURVE"
            ).type = "circle_arc"  # North-west
            pie.operator(
                "object.sp_set_segment_type",
                text="Ellipse Arc",
                icon="INVERSESQUARECURVE",
            ).type = "ellipse_arc"  # North-east
            # pie.separator() #South-west
            # pie.separator() #South-east


def menu_surface(self, context):
    self.layout.separator()
    if context.mode == "OBJECT":
        self.layout.operator(
            "object.sp_add_bezier_patch",
            text="Bezier PsychoPatch",
            icon="SURFACE_NSURFACE",
        )
        self.layout.operator(
            "object.sp_add_nurbs_patch",
            text="NURBS PsychoPatch",
            icon="SURFACE_NSURFACE",
        )
        self.layout.operator(
            "object.sp_add_flat_patch", text="Flat patch", icon="SURFACE_NCURVE"
        )
        # self.layout.operator("object.sp_add_cylinder", text="Cylinder", icon="SURFACE_NCYLINDER")


def menu_curve(self, context):
    self.layout.separator()
    if context.mode == "OBJECT":
        self.layout.operator(
            "object.sp_add_curve", text="PsychoCurve", icon="CURVE_NCURVE"
        )


def menu_convert(self, context):
    self.layout.separator()
    self.layout.label(text="SurfacePsycho")
    # if context.mode == "OBJECT":
    # if context.active_object.type == "SURFACE":
    self.layout.operator(
        "object.sp_bl_nurbs_to_psychopatch",
        text="Internal NURBS to PsychoPatch",
        icon="SURFACE_NSURFACE",
    )
    # if context.active_object.type == "MESH":
    self.layout.operator(
        "object.sp_psychopatch_to_bl_nurbs",
        text="PsychoPatch to internal NURBS",
        icon="SURFACE_NSURFACE",
    )


def menu_export_step(self, context):
    self.layout.operator(SP_OT_ExportStep.bl_idname, text="SurfacePsycho STEP (.step)")


def menu_export_iges(self, context):
    self.layout.operator(SP_OT_ExportIges.bl_idname, text="SurfacePsycho IGES (.iges)")


def menu_export_svg(self, context):
    self.layout.operator(SP_OT_ExportSvg.bl_idname, text="SurfacePsycho SVG (.svg)")


def menu_func_import(self, context):
    self.layout.operator(
        SP_OT_ImportCAD.bl_idname, text="SurfacePsycho CAD (.step, .iges)"
    )


# topbar menu (fails)
def menu_segment_edit(self, context):
    self.layout.menu("SP_MT_SegmentEdit")


addon_keymaps = []


def hotkeys_add(addon_keymaps):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")

        kmi = km.keymap_items.new(
            "object.sp_toggle_endpoints", "F", "PRESS", shift=True, alt=True
        )
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("wm.call_menu_pie", "F", "PRESS", shift=True)
        kmi.properties.name = "SP_MT_PIE_SegmentEdit"
        addon_keymaps.append((km, kmi))


def hotkeys_remove(addon_keymaps):
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


classes = [
    SP_PT_MainPanel,
    SP_PT_EditPanel,
    SP_MT_PIE_SegmentEdit,
]


def register():
    macros.register()
    import_operator.register()
    export_operator.register()

    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_surface_add.append(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.append(menu_curve)
    bpy.types.VIEW3D_MT_object_convert.append(menu_convert)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_step)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_iges)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_svg)
    # bpy.types.TOPBAR_MT_editor_menus.append(menu_segment_edit)

    hotkeys_add(addon_keymaps)


def unregister():
    hotkeys_remove(addon_keymaps)

    # bpy.types.TOPBAR_MT_editor_menus.remove(menu_segment_edit)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_svg)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_iges)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_step)
    bpy.types.VIEW3D_MT_object_convert.remove(menu_convert)
    bpy.types.VIEW3D_MT_curve_add.remove(menu_curve)
    bpy.types.VIEW3D_MT_surface_add.remove(menu_surface)

    for c in classes[::-1]:
        bpy.utils.unregister_class(c)

    macros.unregister()
    export_operator.unregister()
    import_operator.unregister()
