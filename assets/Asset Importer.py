# Release instructions
# 1 : Delete all objects
# 2 : Clear all assets (of current file)
# 3 : Clean up recursive unused data blocks
# 4 : Execut script

import bpy

#bpy.ops.object.select_all(action='SELECT')
#bpy.ops.object.delete(use_global=False)
#bpy.ops.asset.clear(set_fake_user=False)
#bpy.ops.outliner.orphans_purge(num_deleted=115, do_local_ids=True, #do_linked_ids=True, do_recursive=True)

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


filepath1 = "//..\..\Bezier Quest\Bezier_surface.blend"
obj_names1 = ["PsychoPatch", "PsychoPatch Quadratic", "PsychoCurve"]

filepath2 = "//..\..\Bezier Quest\Principal curvature.blend"
obj_names2 = ["SP - Curvatures Probe"]

filepath3 = "//..\..\Bezier Quest\Flat surfaces.blend"
obj_names3 = ["FlatPatch"]


gr_names = [
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
gr_names2 = [
"SP - Connect to Flat patch"
]


append_node_group_by_names(filepath1, gr_names)
append_node_group_by_names(filepath2, gr_names2)
append_objs_by_names(filepath1, obj_names1)
append_objs_by_names(filepath2, obj_names2)
append_objs_by_names(filepath3, obj_names3)



       

