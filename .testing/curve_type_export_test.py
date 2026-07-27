import bpy
from bpy import context

bpy.ops.wm.open_mainfile(
    filepath="c:/Users/romai/Documents/Projets/26 - Bezier Quest/Testing/TEST - curve types export.blend"
)

# bpy.ops.object.select_all(action='DESELECT')

# # Select all objects (or filter as needed)
# for o in context.scene.objects:
#     o.select_set(True)

# bpy.ops.wm.sp_quick_export()

for window in context.window_manager.windows:
    screen = window.screen
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            with context.temp_override(window=window, area=area, selected_objects=list(context.scene.objects)):
                bpy.ops.wm.sp_quick_export()
            break
    break
