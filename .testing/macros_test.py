import bpy

bpy.ops.wm.open_mainfile(
    filepath="c:/Users/romai/Documents/Projets/26 - Bezier Quest/Testing/TEST - Macros.blend"
)

bpy.ops.node.sp_update_all_node_groups(force=True)

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

# Blend
selection_overwrite = "{('Bezier Patch.005', 3, (np.float32(-2.7637966), np.float32(-5.555288), np.float32(1.7750013))), ('Bezier Patch.004', 1, (np.float32(-0.761457), np.float32(-4.9268675), np.float32(1.962445)))}"
bpy.ops.view3d.sp_overwrite_segment_selection(select_string=selection_overwrite)
bpy.ops.object.sp_blend_surfaces()

# Blend to trim
selection_overwrite = "{('Bezier Patch.006', 10, (np.float32(7.7224364), np.float32(-5.020566), np.float32(2.143711))), ('Bezier Patch.006', 7, (np.float32(6.6942716), np.float32(-3.6591058), np.float32(2.1192327)))}"
bpy.ops.view3d.sp_overwrite_segment_selection(select_string=selection_overwrite)
bpy.ops.object.sp_blend_surfaces()

# Blend with flat
selection_overwrite = "{('Bezier Patch.006', 1, (np.float32(6.370086), np.float32(-3.2677135), np.float32(2.1362743))), ('FlatPatch', 3, (np.float32(4.7985315), np.float32(-2.9041471), np.float32(1.967834)))}"
bpy.ops.view3d.sp_overwrite_segment_selection(select_string=selection_overwrite)
bpy.ops.object.sp_blend_surfaces(
    invert=True, tension1=-1.0, continuity1="G3", continuity2="G0"
)

# Flip normal
for window in bpy.context.window_manager.windows:
    screen = window.screen
    for area in screen.areas:
        if area.type == "VIEW_3D":
            with bpy.context.temp_override(
                window=window,
                area=area,
                selected_objects=[
                    bpy.data.objects["Fill Patch"],
                    bpy.data.objects["Bezier Patch"],
                    bpy.data.objects["Bezier Patch.001"],
                    bpy.data.objects["Bezier Patch.002"],
                    bpy.data.objects["Bezier Patch.003"],
                    bpy.data.objects["Blend Patch.002"],
                ],
            ):
                bpy.ops.object.sp_flip_normals()
            break
    break


# Extract segment
selection_overwrite = "{('Bezier Patch.007', 5, (np.float32(1.9625154), np.float32(-9.481448), np.float32(2.18698))), ('FlatPatch.001', 5, (np.float32(7.602225), np.float32(-11.362125), np.float32(2.125318))), ('Bezier Patch.007', 11, (np.float32(2.9215267), np.float32(-9.758539), np.float32(2.461623))), ('Bezier Patch.008', 6, (np.float32(4.244667), np.float32(-11.782228), np.float32(1.735652)))}"
bpy.ops.view3d.sp_overwrite_segment_selection(select_string=selection_overwrite)
bpy.ops.object.sp_extract_segment()

# Isoparam
