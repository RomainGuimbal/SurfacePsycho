##############################
##            GUI           ##
##############################
import bpy
import platform
os = platform.system()
from . import macros
from concurrent.futures import ThreadPoolExecutor
# from .macros import SP_Props_Group


from .importer import prepare_import, ShapeHierarchy, import_face_nodegroups, process_topods_face, create_blender_object
from .utils import append_node_group
from .exporter_cad import export_step, export_iges
from .exporter_svg import export_svg

from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy_extras.io_utils import ExportHelper, ImportHelper, orientation_helper, axis_conversion


@orientation_helper(axis_forward='Y', axis_up='Z')
class SP_OT_ExportStep(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.step_export"
    bl_label = "Export STEP"
    filename_ext = ".step"
    filter_glob: StringProperty(default="*.step", options={'HIDDEN'}, maxlen=255)
    use_selection: BoolProperty(name="Selected Only", description="Selected only", default=True)
    # axis_up: EnumProperty(default='Z')
    # axis_forward: EnumProperty(default='Y')
    scale: FloatProperty(name="Scale", default=1000, min=0)
    sew_tolerance_exponent : IntProperty(name= "Sewing Tolerance Exponent", description="In millimeter, after scale have been applied (-1 = 0.1mm)", default = -1, soft_min = -10, soft_max=0)

    def execute(self, context):
        export_isdone = export_step(context, self.filepath, self.use_selection, self.scale, 10**self.sew_tolerance_exponent, 'Z', 'Y', )
        
        if export_isdone:
            pass
            # self.report({'INFO'}, f"Step file exported as {self.filepath}.step")
        else :
            self.report({'INFO'}, 'No SurfacePsycho Objects selected')
        return {'FINISHED'}


@orientation_helper(axis_forward='Y', axis_up='Z')
class SP_OT_ExportIges(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.iges_export"
    bl_label = "Export IGES"
    filename_ext = ".iges"
    filter_glob: StringProperty(default="*.iges", options={'HIDDEN'}, maxlen=255)
    use_selection: BoolProperty(name="Selected Only", description="Selected only", default=True)
    # axis_up: EnumProperty(default='Z')
    # axis_forward: EnumProperty(default='Y')
    scale: FloatProperty(name="Scale", default=1000, min=0)
    sew_tolerance_exponent : IntProperty(name= "Sewing Tolerance Exponent", description="In millimeter, after scale have been applied (-1 = 0.1mm)", default = -1, soft_min = -10, soft_max=0)


    def execute(self, context):
        export_iges(context, self.filepath, self.use_selection, self.scale, 10**self.sew_tolerance_exponent, 'Z', 'Y')
        return {'FINISHED'}

@orientation_helper(axis_forward='Y', axis_up='Z')
class SP_OT_ImportCAD(bpy.types.Operator, ImportHelper):
    bl_idname = "sp.cad_import"
    bl_label = "Import CAD"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".step;.stp;.iges;.igs"
    filter_glob: StringProperty(default="*.step;*.stp;*.iges;*.igs", options={'HIDDEN'}, maxlen=255)
    faces: BoolProperty(name="Faces", description="Import Faces", default=True)
    trim_contours: BoolProperty(name="Trim Contours", description="Import faces with their trim contours", default=True)
    curves: BoolProperty(name="Curves", description="Import Curves", default=True)
    scale: FloatProperty(name="Scale", default=.001, precision=3)
    resolution : IntProperty(name="Resolution", default=16, soft_min = 6, soft_max=256)

    executor = None
    io_futures = []
    batches = []
    current_batch = 0
    face_processed = 0

    executor_curve = None
    io_futures_curve = []
    batches_curve = []
    current_batch_curve = 0
    curve_processed = 0

    def execute(self, context):
        # Initialize your CAD import generator
        shape, self.doc, container_name = prepare_import(self.filepath)
        
        # Create hierarchy and collections
        shape_hierarchy = ShapeHierarchy(shape, container_name)
        shape_count= len(shape_hierarchy.faces) + len(shape_hierarchy.edges)

        # Faces
        if self.faces:
            import_face_nodegroups(shape_hierarchy)
            batch_size = 500
            faces = shape_hierarchy.faces
            self.batches = [faces[i:i+batch_size] for i in range(0, len(faces), batch_size)]
            self.current_batch = 0
            self.face_processed = 0

            # Create thread pool (4 workers - adjust based on your I/O capacity)
            self.executor = ThreadPoolExecutor(max_workers=16)
            
            # Start processing first batch
            self._submit_io_batch()

        # # Curves
        # if self.curves:
        #     curves = shape_hierarchy.curves
        #     self.batches_curve = [curves[i:i+batch_size] for i in range(0, len(curves), batch_size)]
        #     self.current_batch_curve = 0
        #     self.curve_processed = 0

        #     # Create thread pool (4 workers - adjust based on your I/O capacity)
        #     self.executor_curve = ThreadPoolExecutor(max_workers=4)
            
        #     # Start processing first batch
        #     self._submit_io_batch_curve()

                    
        # Setup progress bar
        wm = context.window_manager
        wm.modal_handler_add(self)
        wm.progress_begin(0, shape_count)

        return {'RUNNING_MODAL'}


    def _submit_io_batch(self):
        """Submit I/O work for current batch to thread pool"""
        batch = self.batches[self.current_batch]
        self.io_futures = [
            self.executor.submit(
                process_topods_face,
                f,
                self.doc,
                col,
                self.trim_contours, 
                self.scale, 
                self.resolution
            )
            for f, col in batch
        ]
    

    # TO FINISH
    # def _submit_io_batch_curve(self):
    #     """Submit I/O work for current batch to thread pool"""
    #     batch = self.batches[self.current_batch]
    #     self.io_futures = [
    #         self.executor.submit(
    #             process_topods_face,
    #             f,
    #             self.doc,
    #             col,
    #             self.trim_contours, 
    #             self.scale, 
    #             self.resolution
    #         )
    #         for f, col in batch
    #     ]
        

    def modal(self, context, event):
        if event.type == 'ESC':
            self.cancel(context)
            return {'CANCELLED'}

        if self.current_batch < len(self.batches):
            # Check if current batch's I/O is complete
            if all(f.done() for f in self.io_futures):
                # Get I/O results
                io_data = [f.result() for f in self.io_futures]
                
                # Create Blender objects in main thread
                for object_data in io_data:
                    create_blender_object(object_data)
                    self.face_processed += 1
                    
                    # Update progress
                    context.window_manager.progress_update(self.face_processed)

                # Update UI
                context.area.tag_redraw()
                
                # Prepare next batch
                self.current_batch += 1
                if self.current_batch < len(self.batches):
                    self._submit_io_batch()
                else:
                    context.window_manager.progress_end()
                    self.executor.shutdown()
                    return {'FINISHED'}
        

        return {'RUNNING_MODAL'}
        # return {'PASS_THROUGH'}, only for timer ?

    def cancel(self, context):
        if self.executor:
            self.executor.shutdown(wait=False)
        context.area.tag_redraw()



class SP_OT_ExportSvg(bpy.types.Operator, ExportHelper):
    bl_idname = "sp.svg_export"
    bl_label = "Export SVG"

    filename_ext = ".svg"
    filter_glob: StringProperty(default="*.svg", options={'HIDDEN'}, maxlen=255)
    use_selection: BoolProperty(name="Selected Only", description="Selected only", default=True)
    plane: EnumProperty(name="Projection Plane", default='XY', items=[('XY', "XY", "XY Plane"), ('YZ', "YZ", "YZ Plane"), ('XZ', "XZ", "XZ Plane")])
    origin_mode: EnumProperty(name="Origin Mode", default='auto', items=[('auto', "Auto", "Fits exported entities"), 
                                                                         ('world', "World", "Place entities relative to Scene origin. Thay may be out of canvas")])
    scale: FloatProperty(name="Scale", default=100, min=0, description="In pixel per Blender unit")
    color_mode: EnumProperty(name="Color", default='material', items=[('material', "From Material", "Color svg paths according to material in object first slot", 'MATERIAL', 1),
                                                                      ('object', "From Object", "Color svg paths according to object color property", 'OBJECT_DATAMODE', 2)])
    def execute(self, context):
        export_svg(context, self.filepath, self.use_selection, self.plane, self.origin_mode, self.scale, self.color_mode)
        return {'FINISHED'}


class SP_PT_MainPanel(bpy.types.Panel):
    bl_idname = "SP_PT_MainPanel"
    bl_label = "Surface Psycho"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    
    def draw(self, context):
        if context.mode == 'OBJECT':
            row = self.layout.row()
            row.scale_y = 2.0
            row.operator("sp.quick_export", text="Quick export as .STEP", icon="EXPORT")
        
            row = self.layout.row()
            row.operator("sp.replace_node_group", text="Replace Node Group", icon="UV_SYNC_SELECT")
            

class SP_PT_ViewPanel(bpy.types.Panel):
    bl_idname = "SP_PT_ViewPanel"
    bl_parent_id = "SP_PT_MainPanel"
    bl_label = "View"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Surface Psycho"
    
    def draw(self, context):
        row = self.layout.row()
        row.operator("sp.toggle_control_geom", text="Toggle Control Geometry", icon="OUTLINER_DATA_LATTICE")
        row = self.layout.row()
        row.operator("sp.toggle_combs", text="Toggle Combs", icon="PARTICLEMODE")

        self.layout.use_property_split = True
        self.layout.use_property_decorate = False
        col = self.layout.column()
        col.prop(context.scene.sp_properties, "combs_scale", text="Combs Scale")

        row = self.layout.row()
        row.operator("sp.add_curvatures_probe", text="Add Curvatures Probe", icon="CURSOR")


class SP_PT_SelectPanel(bpy.types.Panel):
    bl_idname = "SP_PT_SelectPanel"
    bl_parent_id = "SP_PT_MainPanel"
    bl_label = "Select"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Surface Psycho"
    
    def draw(self, context):
        if context.mode == 'OBJECT':
            layout = self.layout
            split = layout.split(factor=0.5, align=True)
            col1 = split.column(align=True)
            col2 = split.column(align=True)

            col1.operator("sp.select_visible_curves", text="Curves", icon="OUTLINER_OB_CURVE")
            col2.operator("sp.select_visible_surfaces", text="Surfaces", icon="OUTLINER_OB_SURFACE")


class SP_PT_EditPanel(bpy.types.Panel):
    bl_idname = "SP_PT_EditPanel"
    bl_parent_id = "SP_PT_MainPanel"
    bl_label = "Edit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Surface Psycho"
    
    def draw(self, context):
        if context.mode == 'OBJECT' or context.mode == 'EDIT_MESH' :
            row = self.layout.row()
            row.operator("sp.add_trim_contour", text="Add Trim Contour", icon="MOD_MESHDEFORM")

        if context.mode == 'EDIT_MESH':
            # Endpoints
            row = self.layout.row()
            row.label(text="Endpoints")
            sub = row.row(align=True)
            sub.operator("sp.assign_as_endpoint", text="Assign")
            sub.operator("sp.remove_from_endpoints", text="Remove")
            sub = row.row()
            sub.operator("sp.select_endpoints", text="Select")

            # Type
            row = self.layout.row()
            sub = row.row(align=True)
            sub.operator("sp.set_segment_type", text="Circle", icon = "MESH_CIRCLE").type = 3
            sub.operator("sp.set_segment_type", text="Arc", icon = "SPHERECURVE").type = 2
            
            row = self.layout.row()
            sub = row.row(align=True)
            sub.operator("sp.set_segment_type", text="Ellipse", icon = "MESH_CAPSULE").type = 5
            sub.operator("sp.set_segment_type", text="Arc", icon = "INVERSESQUARECURVE").type = 4

            # Segment Degree
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            col = self.layout.column()
            col.prop(context.scene.sp_properties, "active_segment_degree", text="NURBS Degree")
            
            # Weight
            self.layout.use_property_split = True
            self.layout.use_property_decorate = False
            col = self.layout.column()
            col.prop(context.scene.sp_properties, "active_vert_weight", text="Weight")


def menu_surface(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.add_bezier_patch", text="Bezier PsychoPatch", icon="SURFACE_NSURFACE")
        self.layout.operator("sp.add_nurbs_patch", text="NURBS PsychoPatch", icon="SURFACE_NSURFACE")
        self.layout.operator("sp.add_flat_patch", text="Flat patch", icon="SURFACE_NCURVE")
        # self.layout.operator("sp.add_cylinder", text="Cylinder", icon="SURFACE_NCYLINDER")
        

def menu_curve(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        self.layout.operator("sp.add_curve", text="PsychoCurve", icon="CURVE_NCURVE")

def menu_convert(self, context):
    self.layout.separator()
    if context.mode == 'OBJECT':
        if context.active_object.type == 'SURFACE':
            self.layout.operator("sp.bl_nurbs_to_psychopatch", text="Internal NURBS to PsychoPatch", icon="SURFACE_NSURFACE")
        if context.active_object.type == 'MESH':
            self.layout.operator("sp.psychopatch_to_bl_nurbs", text="PsychoPatch to internal NURBS", icon="SURFACE_NSURFACE")


def menu_export_step(self, context):
    self.layout.operator("sp.step_export", text="SurfacePsycho CAD (.step)")

def menu_export_iges(self, context):
    self.layout.operator("sp.iges_export", text="SurfacePsycho CAD (.iges)")

def menu_func_import(self, context):
    self.layout.operator(SP_OT_ImportCAD.bl_idname, text="SurfacePsycho CAD (.step, .iges)")

def menu_export_svg(self, context):
    self.layout.operator("sp.svg_export", text="SurfacePsycho SVG (.svg)")


classes = [
    SP_PT_MainPanel,
    SP_PT_ViewPanel,
    SP_PT_SelectPanel,
    SP_PT_EditPanel,
    SP_OT_ExportSvg,        
    SP_OT_ExportStep,
    SP_OT_ExportIges,
    SP_OT_ImportCAD,
]



def register():
    macros.register()
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_surface_add.append(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.append(menu_curve)
    bpy.types.VIEW3D_MT_object_convert.append(menu_convert)
    # bpy.types.VIEW3D_MT_object_context_menu_convert.append(menu_convert)

    bpy.types.TOPBAR_MT_file_export.append(menu_export_step)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_iges)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_export_svg)

    #TODO
    # # Add hotkey
    # wm = bpy.context.window_manager
    # kc = wm.keyconfigs.addon
    # if kc:
    #     km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    #     kmi = km.keymap_items.new(OBJECT_OT_CustomOp.bl_idname, type='W', value='PRESS', ctrl=True)
    #     addon_keymaps.append((km, kmi))
    
def unregister():  
    #TODO
    # # # Remove hotkey
    # for km, kmi in addon_keymaps:
    #     km.keymap_items.remove(kmi)
    # addon_keymaps.clear()

    bpy.types.TOPBAR_MT_file_export.remove(menu_export_svg)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_step)
    bpy.types.TOPBAR_MT_file_export.remove(menu_export_iges)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.VIEW3D_MT_surface_add.remove(menu_surface)
    bpy.types.VIEW3D_MT_curve_add.remove(menu_curve)
    bpy.types.VIEW3D_MT_object_convert.remove(menu_convert)
    # bpy.types.VIEW3D_MT_object_context_menu_convert.remove(menu_convert)
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
    macros.unregister()

if __name__ == "__main__":
    bpy.ops.sp.cad_import()