import bpy
from mathutils import Matrix

for o in bpy.data.objects:
    bpy.data.objects.remove(o)

bpy.ops.object.sp_cad_import(filepath="C:\\Users\\romai\\Desktop\\Torus.step")
bpy.ops.object.sp_cad_import(filepath="C:\\Users\\romai\\Desktop\\Cylinder.step")
bpy.ops.object.sp_cad_import(filepath="C:\\Users\\romai\\Desktop\\cone.step")
bpy.ops.object.sp_cad_import(filepath="C:\\Users\\romai\\Desktop\\sphere.step")


# Get the current 3D view context
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
                break
