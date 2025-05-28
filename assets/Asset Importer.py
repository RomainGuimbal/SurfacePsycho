# Release instructions
# 1 : Execut script
# 2 : Make local

import bpy
import time
from pathlib import Path

#delete all objects
for o in bpy.data.objects:
    bpy.data.objects.remove(o)
    
for c in bpy.data.collections:
    bpy.data.collections.remove(c)
    
for n in bpy.data.node_groups:
    bpy.data.node_groups.remove(n)

for n in bpy.data.meshes:
    bpy.data.meshes.remove(n)
    
for n in bpy.data.curves:
    bpy.data.curves.remove(n)
    
for n in bpy.data.grease_pencils:
    bpy.data.grease_pencils.remove(n)

for n in bpy.data.fonts:
    bpy.data.fonts.remove(n)
    
for n in bpy.data.materials:
    bpy.data.materials.remove(n)



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


def append_collections_by_names(filepath, collection_names):
    # Load the specified collections from the file
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.collections = [name for name in data_from.collections if name in collection_names]
    
    # Link the loaded collections to the current scene
    for collection in data_to.collections:
        if collection is not None:
            bpy.context.scene.collection.children.link(collection)
            


def assign_assets_to_catalog(asset_names, catalog_name): #only works for objects
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
                    asset_data.catalog_id = uuid



##############################################

# PROBE
filepath_probe = "//..\..\Bezier-Quest\Principal curvature.blend"
obj_probe = ["SP - Curvatures Probe"]

# CURVE
filepath_curve_flat = "//..\..\Bezier-Quest\SP - Curve and FlatPatch.blend"
obj_curve_flat = ["FlatPatch", "PsychoCurve", "Internal Curve For Patch",]
gr_curve_flat = [
"SP - Bezier Circlular Arc",
"SP - Blend Curve",
"SP - Compose FlatPatch From Sides",
"SP - Continuities between Segments",
"SP - Convert Circles and Ellipses to Splines",
"SP - Loft from Internal Curves",
#"SP - Convert Flat Patch to Bezier Patch",
"SP - Copy Curve or FlatPatch",
"SP - Copy Flat Patch Side",
"SP - Copy Mesh Face",
"SP - Curve on Surface from UV",
"SP - Interpolation Curve",
"SP - Distance Between Curves",
"SP - Fillet Curve or FlatPatch",
"SP - Fit Curve",
"SP - Inset FlatPatch",
"SP - Internal Curve to PsychoCurve",
"SP - Intervale Curve",
"SP - Match SVG Compatible Degrees",
"SP - Mirror Curve Control Points",
"SP - Mirror Curve Locally",
"SP - Mirror FlatPatch or Curve",
"SP - Multi Split Curve",
"SP - NURBS to Bezier Curve or FlatPatch",
"SP - Oblong Wire",
"SP - Project on Flat Patch",
"SP - Raise or Lower Curve Degree",
"SP - Raise or Lower Order of Selected Segment",
"SP - Reorder Curve Index",
"SP - Reorder Curve Selection",
"SP - Sample Curve Degree + 1 Points",
"SP - Split Curve",
"SP - Switch Curve Direction",
"SP - Text to Curve or FlatPatch",
"SP - Radial Repeat FlatPatch",
"SP - Reproject Ellipse Arcs Ends",
#"SP - Continuities Curve",
#"SP - Curve Meshing",
#"SP - Crop or Extend Curve",
#"SP - Offset Curve",
]

# BEZIER SURF
filepath_surf = "//..\..\Bezier-Quest\SP - Bezier surface.blend"
obj_surf = ["Bezier Patch"]
gr_surf = [
"SP - Auto Midpoints Linear",
"SP - Blend Surfaces",
"SP - Connect Bezier Patch",
"SP - Convert Contour",
"SP - Crop or Extend Patch",
"SP - Crop Patch to Point",
"SP - Curvature Analysis",
"SP - Displace Patch",
"SP - Displace Precisely",
"SP - Fillet Trim Contour",
"SP - Flatten Patch",
"SP - Flatten Patch Side",
"SP - Gradient Map",
"SP - Interpolation Patch Grid",
"SP - Loft",
"SP - Mirror Patch Control Points",
"SP - Nearest Curve on Bezier Patch",
"SP - Patch Exact Normals",
"SP - Project Curve on Bezier Patch",
"SP - Raise or Lower Degree Bezier Patch",
"SP - Reorder Grid Index",
"SP - Ruled Surface from Mesh Loop",
"SP - Select Patch Range",
"SP - Sew and Symmetrize",
"SP - Copy Segment",
"SP - Copy Flat Patch as Trim Contour",
#"SP - Sweep Linear Bicubic",
#"SP - Sweep Bicubic",
#"SP - Auto Snap Continuities",
#"SP - Straighten Rows",
]



# NURBS
filepath_nurbs= "//..\..\Bezier-Quest\SP - NURBS.blend"
obj_nurbs=["NURBS Patch"]
gr_nurbs=[
#"SP - NURBS Curve Meshing",
"SP - NURBS Patch Meshing",
"SP - NURBS Weighting",
"SP - Set Knot NURBS Patch",
"SP - NURBS to Bezier Patch [Naive slow]",
"SP - Crop NURBS Patch",
"SP - Insert Knot NURBS Patch",
"SP - Curvature Analysis NURBS",
"SP - Continuity Analysis",
]


# OTHER
filepath_other= "//..\..\Bezier-Quest\SP - Other Primitives.blend"
#obj_other=[""]
gr_other=[
"SP - Cylindrical Meshing",
"SP - Toroidal Meshing",
"SP - Spherical Meshing",
"SP - Conical Meshing",
"SP - Surface of Extrusion Meshing",
"SP - Surface of Revolution Meshing",
]

# SHAPES
filepath_preset = "//..\..\Bezier-Quest\SP - Shapes presets.blend"
obj_preset = ["Disk", "Circle", "Quadaratic Dome", "Cubic Dome"]
coll_preset = ["Slab", "Cylinder", "Corner", "Step", "Thick Arch", "Tube", "Square Tube"]



# Append Groups
append_node_group_by_names(filepath_curve_flat, gr_curve_flat)
append_node_group_by_names(filepath_surf, gr_surf)
append_node_group_by_names(filepath_nurbs, gr_nurbs)
append_node_group_by_names(filepath_other, gr_other)

# Append Objects
append_objs_by_names(filepath_probe, obj_probe)
append_objs_by_names(filepath_curve_flat, obj_curve_flat)
append_objs_by_names(filepath_surf, obj_surf)
append_objs_by_names(filepath_nurbs, obj_nurbs)
append_objs_by_names(filepath_preset, obj_preset)
#append_objs_by_names(filepath_other, obj_other)

append_collections_by_names(filepath_preset, coll_preset)

#assign_assets_to_catalog(obj_preset, 'Shape')

bpy.ops.object.make_local(type='ALL')

full_list = gr_surf + gr_curve_flat + gr_nurbs + [
"SP - NURBS Curve Meshing",
"SP - Bezier Patch Continuities",
"SP - Auto Snap Continuities",
"SP - Continuities Bicubic",
"SP - Straighten Rows",
"SP - Continuities Curve",
"SP - Curve Meshing",
"SP - Crop or Extend Curve",
"SP - Bezier Patch Meshing",
]

#for ng in full_list:
#    bpy.ops.sp.replace_node_group(target_name=ng+".001", new_name=ng)
#    
#bpy.ops.sp.replace_node_group(target_name="SP - Bezier Patch Meshing.100", new_name = "SP - Bezier Patch Meshing")



# clear unused data. Do several times to fake recursive
for ng in bpy.data.node_groups :
    if ng.asset_data == None :
        if ng.use_fake_user:
            ng.use_fake_user = False
        if ng.users == 0 :
            bpy.data.node_groups.remove(ng)
           
for ng in bpy.data.node_groups :
   if ng.users == 0 and ng.asset_data == None :
       bpy.data.node_groups.remove(ng)
       
for ng in bpy.data.node_groups :
   if ng.users == 0 and ng.asset_data == None :
       bpy.data.node_groups.remove(ng)
       
for ng in bpy.data.node_groups :
   if ng.users == 0 and ng.asset_data == None :
       bpy.data.node_groups.remove(ng)
       
for ng in bpy.data.node_groups :
   if ng.users == 0 and ng.asset_data == None :
       bpy.data.node_groups.remove(ng)
       
for ng in bpy.data.node_groups :
   if ng.users == 0 and ng.asset_data == None :
       bpy.data.node_groups.remove(ng)
       
for ng in bpy.data.node_groups :
   if ng.users == 0 and ng.asset_data == None :
       bpy.data.node_groups.remove(ng)