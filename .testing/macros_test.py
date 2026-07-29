import bpy

bpy.ops.wm.open_mainfile(
    filepath="c:/Users/romai/Documents/Projets/26 - Bezier Quest/Testing/TEST - Macros.blend"
)

# Fill case 1: square
selection_overwrite = (
    '{("Bezier Patch", 1, (np.float32(-0.37130672), np.float32(3.1189058), np.float32(1.2833786))),'
    + '("Bezier Patch.002", 0, (np.float32(1.6607821), np.float32(1.8928198), np.float32(0.97165424))),'
    + '("Bezier Patch.003", 0, (np.float32(-2.8770835), np.float32(2.6169577), np.float32(1.1849936))),'
    + '("Bezier Patch.001", 3, (np.float32(-0.79149824), np.float32(1.6621662), np.float32(0.8193401)),)}'
)

bpy.ops.view3d.sp_overwrite_segment_selection(select_string=selection_overwrite)
bpy.ops.object.sp_fill()


# Fill case 2: rails ?
# TODO
