import bpy
#read_step_file()

class SP_OT_Import_step(bpy.types.Operator):
    bl_idname = "object.import_step"
    bl_label = "import_step"

    def execute(self, context):
        return {'FINISHED'}
