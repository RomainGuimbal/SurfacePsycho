# Release instructions
# 1 : Delete all objects
# 2 : Clear all assets (of current file)
# 3 : Clean up recursive unused data blocks
# 4 : Execut script

import bpy
import time
"""
#delete all objects
for o in bpy.context.scene.objects:
    o.select_set(True)
bpy.ops.object.delete()

bpy.context.view_layer.update()


#clear all assets
for a in bpy.context.screen.areas :
    if a.ui_type == 'ASSETS':
        area = a
        break

with bpy.context.temp_override(area=area):
    bpy.ops.file.select_all(action='SELECT')
    bpy.ops.asset.clear(set_fake_user = False)
    
    #if sa != None and len(bpy.context.selected_assets)>0 :
        #bpy.ops.asset.clear(set_fake_user = False)

#purge data blocks
bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)"""


##############################################

""" Avoid duplication : 
    link = True
    select all
    make local
    set location
"""


def is_asset(obj):
    return obj.asset_data is not None

def append_objs_by_names(filepath,obj_names):
    # link all objects in the list
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects if name in obj_names]
    # link object to current scene
    for obj in data_to.objects:
        if obj is not None:
           bpy.context.collection.objects.link(obj)
           obj.location = (0,0,0)


def append_node_group_by_names(filepath, gr_names):
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.node_groups = [name for name in data_from.node_groups if name in gr_names]
#        data_to.node_groups = [name for name in data_from.node_groups if data_from.node_groups(name).asset_data is not None]


filepath_surf = "//..\..\Bezier Quest\Bezier_surface.blend"
obj_surf = ["PsychoPatch", "PsychoPatch Quadratic", "PsychoPatch Any Order"]

filepath_probe = "//..\..\Bezier Quest\Principal curvature.blend"
obj_probe = ["SP - Curvatures Probe"]

filepath_flat = "//..\..\Bezier Quest\Flat surfaces.blend"
obj_flat = ["FlatPatch"]

filepath_curve = "//..\..\Bezier Quest\Curves.blend"
obj_curve = ["PsychoCurve Any Order", "Psycho Cubic Chain"]

gr_surf = [
"SP - Angle side",
#"SP - AOP Continuities",
"SP - Auto Midpoints Linear",
#"SP - Auto Snap Continuities",
"SP - Blend Surface",
"SP - Connect AOP to Curve",
"SP - Connect to Chain",
#"SP - Continuities",
"SP - Displace Bicubic Patch",
"SP - Gradient Maps",
"SP - Mirror Control Points",
"SP - Mirror Control Points AOP",
"SP - Patch Combs",
#"SP - Quadratic to Cubic Control grid",
"SP - Reorder Index",
"SP - Sew and Symmetrize",
#"SP - Straighten Rows",
"SP - Sweep",
"SP - Sweep Linear",
#"SP - Trim 4 sides",
"SP - Patch Normals",

]

gr_flat = [
"SP - Connect to Flat Patch",
"SP - Copy Mesh Face",
"SP - Flat Patch Circle",
"SP - Project on Flat Patch",
]

gr_curve = [
"SP - Raise or Lower Order",
"SP - Straight Curve On Surface",
#"SP - Trim Range Any Order Curve",
"SP - Blend Curve",
"SP - Bezier Chain Circle",
#"SP - Align Handles",
"SP - Chain to Chain Continuities",
"SP - Straighten Segment",
"SP - Displace Chain Handles",
#"SP - Trim Chain",
#"SP - Continuities Any Order Curve",
"SP - Copy Patch Side",
]

append_objs_by_names(filepath_surf, obj_surf)
append_objs_by_names(filepath_probe, obj_probe)
append_objs_by_names(filepath_flat, obj_flat)
append_objs_by_names(filepath_curve, obj_curve)

append_node_group_by_names(filepath_surf, gr_surf)
append_node_group_by_names(filepath_flat, gr_flat)
append_node_group_by_names(filepath_curve, gr_curve)

