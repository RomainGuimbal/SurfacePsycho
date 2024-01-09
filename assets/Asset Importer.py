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
obj_surf = ["PsychoPatch", "PsychoPatch Quadratic"]

filepath_probe = "//..\..\Bezier Quest\Principal curvature.blend"
obj_probe = ["SP - Curvatures Probe"]

filepath_flat = "//..\..\Bezier Quest\Flat surfaces.blend"
obj_flat = ["FlatPatch"]

filepath_curve = "//..\..\Bezier Quest\Curves.blend"
obj_curve = ["PsychoCurve Any Order"]#"Psycho Cubic Chain",

gr_surf = [
"SP - Auto mid points linear",
#"SP - Continuities",
"SP - Angle side (do not preserve surface)",
"SP - Connect side to curve",
#"SP - Quadratic to Cubic Control grid",
"SP - Sew and Symetrise",
"SP - Sweep Linear",
#"SP - Trim 4 sides",
"SP - Patch Combs",
"SP - Continuities (Auto Snap)",
"SP - Sew and Symmetrize",
"SP - Straighten Rows"
]
gr_flat = [
"SP - Connect to Flat patch"
]
gr_curve = [
"SP - Raise Order",
"SP - Bezier Curve Curvature combs",
#"SP - Trim Range Any Order Curve",
]

append_objs_by_names(filepath_surf, obj_surf)
append_objs_by_names(filepath_probe, obj_probe)
append_objs_by_names(filepath_flat, obj_flat)
append_objs_by_names(filepath_curve, obj_curve)

append_node_group_by_names(filepath_surf, gr_surf)
append_node_group_by_names(filepath_flat, gr_flat)
append_node_group_by_names(filepath_curve, gr_curve)

