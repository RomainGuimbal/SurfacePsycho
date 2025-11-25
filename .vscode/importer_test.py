import bpy
from mathutils import Matrix, Vector

for o in bpy.data.objects:
    bpy.data.objects.remove(o)

# bpy.context.preferences.view.show_splash = False

# Set view
for area in bpy.context.screen.areas:
    if area.type == "VIEW_3D":
        for space in area.spaces:
            if space.type == "VIEW_3D":
                region_3d = space.region_3d
                
                region_3d.view_matrix = Matrix(
                    (
                        (0.3132, 0.9497, 0.0000, 0.0000),
                        (-0.4464, 0.1472, 0.8826, 0.0000),
                        (0.8382, -0.2764, 0.4701, -0.1176),
                        (0.0000, 0.0000, 0.0000, 1.0000),
                    )
                )

                region_3d.view_location = Vector((0.0, 0.0, 0.0))
                region_3d.view_distance = 1.2
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


bpy.ops.object.sp_cad_import(filepath="..\\STEP samples\\Torus.step")
bpy.ops.object.sp_cad_import(filepath="..\\STEP samples\\Cylinder.step")
bpy.ops.object.sp_cad_import(filepath="..\\STEP samples\\cone.step")
bpy.ops.object.sp_cad_import(filepath="..\\STEP samples\\sphere.step")
bpy.ops.object.sp_cad_import(filepath="..\\STEP samples\\extrusion calibration1.step")
bpy.ops.object.sp_cad_import(filepath="..\\STEP samples\\revolution.step")

