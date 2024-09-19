# Release instructions
# 1 : Delete all objects
# 2 : Clear all assets (of current file)
# 3 : Clean up recursive unused data blocks
# 4 : Execut script
# 5 : make local

import bpy
import time
from pathlib import Path
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


def append_collections_by_names(filepath, collection_names):
    # Load the specified collections from the file
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.collections = [name for name in data_from.collections if name in collection_names]
    
    # Link the loaded collections to the current scene
    for collection in data_to.collections:
        if collection is not None:
            bpy.context.scene.collection.children.link(collection)
            

"""def assign_assets_to_catalog(asset_names, catalog_name): #only works for objects
    folder = Path(bpy.data.filepath).parent
    
    for a in asset_names :
        with (folder / "blender_assets.cats.txt").open() as f:
            for line in f.readlines():
                if line.startswith(("#", "VERSION", "\n")):
                    continue
                # Each line contains : 'uuid:catalog_tree:catalog_name' + eol ('\n')
                name = line.split(":")[2].split("\n")[0]
                if name == catalog_name:
                    uuid = line.split(":")[0]
                    obj = bpy.data.objects[a]
                    asset_data = obj.asset_data
                    asset_data.catalog_id = uuid"""


# PROBE
filepath_probe = "//..\..\Bezier-Quest\Principal curvature.blend"
obj_probe = ["SP - Curvatures Probe"]

# SHAPES
filepath_preset = "//..\..\Bezier-Quest\SP - Shapes presets.blend"
obj_preset = ["Disk", "Circle"]
coll_preset = ["Slab", "Cylinder", "Corner", "Step", "Thick Arch", "Tube", "Square Tube"]

# To copy :    "",

# BEZIER
filepath_surf = "//..\..\Bezier-Quest\Bezier_surface.blend"
obj_surf = ["Bezier Patch"]
gr_surf = [
"SP - Angle Side Bicubic",
"SP - Bezier Patch Continuities with Curve",
"SP - Bezier Patch Continuities with Flat Patch",
"SP - Auto Midpoints Linear",
"SP - Blend Flat Patches",
"SP - Blend Surface",
"SP - Connect Patch to Trim Contour",
"SP - Crop or Extend Patch",
"SP - Displace Patch",
"SP - Displace Precisely",
"SP - Fillet Trim Contour",
"SP - Flatten Patch",
"SP - Flatten Patch Side",
"SP - Gradient Map",
"SP - Loft",
"SP - Mirror Patch Control Points",
"SP - Patch Normals",
"SP - Raise Order Bezier Patch",
"SP - Reorder Grid Index",
"SP - Select Patch Range",
"SP - Sew and Symmetrize",
"SP - Sweep Linear Bicubic",
"SP - Sweep Bicubic",
#"SP - Bezier Patch Continuities",
#"SP - Auto Snap Continuities",
#"SP - Continuities Bicubic",
#"SP - Straighten Rows",
]

# CURVE
filepath_curve_flat = "//..\..\Bezier-Quest\SP - Curve and FlatPatch.blend"
obj_curve_flat = ["FlatPatch", "PsychoCurve", "Internal Curve For Patch",]
gr_curve_flat = [
"SP - Bezier Circle or Disk",
"SP - Blend Curve",
"SP - Circlular Arc",
"SP - Compose FlatPatch From Sides",
"SP - Continuities between Segments",
"SP - Control Grid from Internal Curves",
"SP - Convert Flat Patch to Bezier Patch",
"SP - Copy Curve or FlatPatch",
"SP - Copy Flat Patch Side",
"SP - Copy Mesh Face",
"SP - Copy Patch Side",
"SP - Curve on Surface from UV",
"SP - Curve Through Points",
"SP - Displace Chain Handles",
"SP - Fillet Curve or FlatPatch",
"SP - Inset FlatPatch",
"SP - Internal Curve to PsychoCurve",
"SP - Intervale Curve",
"SP - Mirror Curve Control Points",
"SP - Project on Flat Patch",
"SP - Raise or Lower Curve Order",
"SP - Reorder Curve Index",
"SP - Split Curve",
"SP - Switch Curve Direction",
#"SP - Continuities Curve",
#"SP - Curve Meshing",
#"SP - Crop or Extend Curve",
#"SP - Offset Curve",
]

# NURBS
filepath_nurbs= "//..\..\Bezier-Quest\SP - NURBS.blend"
obj_nurbs=["NURBS Patch"]
gr_nurbs=[
#"SP - NURBS Curve Meshing",
"SP - NURBS Patch Meshing",
"SP - NURBS Weighting",
"SP - Set Knot NURBS Patch",
]

# Append Groups
append_node_group_by_names(filepath_surf, gr_surf)
append_node_group_by_names(filepath_curve_flat, gr_curve_flat)
append_node_group_by_names(filepath_nurbs, gr_nurbs)

# Append Objects
append_objs_by_names(filepath_surf, obj_surf)
append_objs_by_names(filepath_probe, obj_probe)
append_objs_by_names(filepath_curve_flat, obj_curve_flat)
append_objs_by_names(filepath_preset, obj_preset)
append_objs_by_names(filepath_nurbs, obj_nurbs)

append_collections_by_names(filepath_preset, coll_preset)

#assign_assets_to_catalog(obj_preset, 'Shape')


#bpy.ops.object.make_local(type='ALL')

#full_list = gr_surf + gr_curve_flat + gr_nurbs + [
#"SP - NURBS Curve Meshing",
#"SP - Bezier Patch Continuities",
#"SP - Auto Snap Continuities",
#"SP - Continuities Bicubic",
#"SP - Straighten Rows",
#"SP - Continuities Curve",
#"SP - Curve Meshing",
#"SP - Crop or Extend Curve",
#]

#for ng in full_list:
#    bpy.ops.sp.replace_node_group(target_name=ng+".001", new_name=ng)
