import bpy
from mathutils import Matrix, Vector

for o in bpy.data.objects:
    bpy.data.objects.remove(o)

# Set view
for area in bpy.context.screen.areas:
    if area.type == "VIEW_3D":
        for space in area.spaces:
            if space.type == "VIEW_3D":
                region_3d = space.region_3d
                
                region_3d.view_matrix = Matrix(
                    (
                        ( 0.9006,  0.4346, -0.0000, -0.0130),
                        (-0.1390,  0.2881,  0.9474, -0.0212),
                        ( 0.4118, -0.8533,  0.3199, -0.6166),
                        ( 0.0000,  0.0000,  0.0000,  1.0000)
                    )
                )

                region_3d.view_location = Vector((0.0, 0.0, 0.0))
                region_3d.view_distance = 0.7
                break
# import bpy
# from mathutils import Vector

# for area in bpy.context.screen.areas:
#     if area.type == "VIEW_3D":
#         for space in area.spaces:
#             if space.type == "VIEW_3D":
#                 region_3d = space.region_3d
#                 print(region_3d.view_matrix)
#                 print(region_3d.view_location)
#                 break

names =  [
    # "jante.stp",
    # "Audi_R8_Wheel.stp",
    # "plancher G5.step",
    # "Darts_tip_remover_ASM.stp",
    # "Assy meca standard.stp",
    "Taycan.igs",
]

for n in names : 
    bpy.ops.object.sp_cad_import(filepath="..\\STEP samples\\" + n)

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.view3d.view_selected()
        bpy.ops.mesh.select_all(action='DESELECT')