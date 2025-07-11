import bpy
from pathlib import Path


def delete_all_data():
    # Delete all data except scripts
    bpy.data.batch_remove(bpy.data.objects)
    bpy.data.batch_remove(bpy.data.collections)
    bpy.data.batch_remove(bpy.data.node_groups)
    bpy.data.batch_remove(bpy.data.meshes)
    bpy.data.batch_remove(bpy.data.curves)
    bpy.data.batch_remove(bpy.data.grease_pencils)
    bpy.data.batch_remove(bpy.data.fonts)
    bpy.data.batch_remove(bpy.data.materials)


# LINK = False parce que Link = True conserve pas les asset data


def append_objs_by_names(filepath, obj_names):
    print(f"Linking from {filepath}")
    # link all objects in the list
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = []
        for name in obj_names:
            if name in data_from.objects:
                data_to.objects.append(name)
            else:
                raise ValueError(f"{name} NOT found")

    # link object
    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)
            obj.location = (0, 0, 0)


def append_node_group_by_names(filepath, to_import_names):
    print(f"Linking from {filepath}")
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.node_groups = []
        for name in to_import_names:
            if name in data_from.node_groups:
                data_to.node_groups.append(name)
            else:
                raise ValueError(f"{name} NOT found")


def append_collections_by_names(filepath, collection_names):
    print(f"Linking from {filepath}")
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.collections = []
        for name in collection_names:
            if name in data_from.collections:
                data_to.collections.append(name)
            else:
                raise ValueError(f"{name} NOT found")

    # Link collections
    for collection in data_to.collections:
        if collection is not None:
            bpy.context.scene.collection.children.link(collection)


def assign_assets_to_catalog(asset_names, catalog_identifier, debug=False):
    folder = Path(bpy.data.filepath).parent

    catalog_uuid = None

    if debug:
        print(f"Looking for catalog: '{catalog_identifier}'")
        print("Parsing catalog file...")

    with (folder / "blender_assets.cats.txt").open() as f:
        for line_num, line in enumerate(f.readlines(), 1):
            if line.startswith(("#", "VERSION", "\n")) or line.strip() == "":
                continue

            # Debug: show raw line
            if debug:
                print(f"Line {line_num}: '{line.strip()}'")

            # Each line format: 'uuid:catalog_path:catalog_name'
            parts = line.strip().split(":")
            if debug:
                print(f"  Split into {len(parts)} parts: {parts}")

            if len(parts) >= 3:
                uuid = parts[0]
                catalog_path = parts[1]
                catalog_name = parts[2]

                if debug:
                    print(f"  UUID: '{uuid}'")
                    print(f"  Path: '{catalog_path}'")
                    print(f"  Name: '{catalog_name}'")
                    print(
                        f"  Checking if '{catalog_identifier}' == '{catalog_path}' or '{catalog_name}'"
                    )

                # Check if the identifier matches either the path or the name
                if (
                    catalog_identifier == catalog_path
                    or catalog_identifier == catalog_name
                ):
                    catalog_uuid = uuid
                    break
                elif debug:
                    print(f"  No match")

        if not catalog_uuid:
            print(
                f"Error: Catalog '{catalog_identifier}' not found in blender_assets.cats.txt"
            )
            return

    for a in asset_names:
        asset = None

        # Check different data types
        if a in bpy.data.objects.keys():
            asset = bpy.data.objects[a]
        elif a in bpy.data.node_groups.keys():
            asset = bpy.data.node_groups[a]
        elif a in bpy.data.collections.keys():
            asset = bpy.data.collections[a]
        elif a in bpy.data.materials.keys():
            asset = bpy.data.materials[a]
        elif a in bpy.data.meshes.keys():
            asset = bpy.data.meshes[a]
        else:
            print(f"Asset '{a}' not found in any data category")
            continue

        # Assign to catalog if it's an asset
        if asset.asset_data is not None:
            asset.asset_data.catalog_id = catalog_uuid
            asset.asset_data.author = "Romain Guimbal"
        else:
            print(f"'{a}' is not marked as an asset")


##############################################

# PROBE
filepath_probe = "//..\..\Principal curvature.blend"
obj_probe = {"SP - Curvatures Probe"}

# CURVE
filepath_curve_flat = "//..\..\SP - Curve and FlatPatch.blend"
obj_curve_flat = {
    "FlatPatch",
    "PsychoCurve",
}
gr_curve_flat = {
    "SP - Bezier Circlular Arc",
    "SP - Blend Curve",
#    "SP - Compose FlatPatch From Sides",
    "SP - Continuities between Segments",
    "SP - Convert Circles and Ellipses to Splines",
    "SP - Copy Curve or FlatPatch",
    "SP - Copy Flat Patch Side",
    "SP - Copy Mesh Face",
    "SP - Curve on Surface from UV",
    "SP - Distance Between Curves",
    "SP - Fillet Curve or FlatPatch",
    "SP - Fillet Polyline with Circles",
    "SP - Fit Curve",
    "SP - Inset FlatPatch",
    "SP - Intervale Curve",
    "SP - Make SVG Ready",
    "SP - Mirror Curve Control Points",
    "SP - Mirror Curve Locally",
    "SP - Mirror FlatPatch or Curve",
    "SP - Multi Split Curve",
    "SP - NURBS to Bezier Curve or FlatPatch",
    "SP - Oblong Wire",
    "SP - Project on Flat Patch",
    "SP - Radial Array FlatPatch",
    "SP - Raise or Lower Curve Degree",
    "SP - Raise or Lower Order of Selected Segment",
    "SP - Reorder Curve Index",
    "SP - Reorder Curve Selection",
    "SP - Reproject Ellipse Arcs Ends",
    "SP - Sample Curve Per Degree",
    "SP - Split Curve",
    "SP - Switch Curve Direction",
    "SP - Text to Curve or FlatPatch",
    "SP - Interpolate Wire",
    # "SP - Continuities Curve",
    # "SP - Curve Meshing",
    # "SP - Crop or Extend Curve",
    # "SP - Offset Curve",
}

# BEZIER SURF
filepath_surf = "//..\..\SP - Bezier surface.blend"
obj_surf = {
    "Bezier Patch",
    "Internal Curve For Patch",
}
gr_surf = {
    "SP - Auto Midpoints Linear",
    "SP - Blend Surfaces",
    "SP - Connect Bezier Patch",
    "SP - Convert Contour",
    "SP - Crop or Extend Patch",
    "SP - Crop Patch to Point",
    "SP - Curvature Analysis Bezier Patch",
    "SP - Displace Patch",
    "SP - Displace Precisely",
    "SP - Fillet Trim Contour",
    "SP - Fit Bezier Patch",
    "SP - Flatten Patch",
    "SP - Flatten Patch Side",
    "SP - Gradient Map",
    "SP - Interpolation Patch Grid",
    "SP - Loft",
    #    "SP - Loft from Internal Curves",
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
    "SP - Convert Flat Patch to Bezier Patch",
    # "SP - Sweep Linear Bicubic",
    # "SP - Sweep Bicubic",
    # "SP - Auto Snap Continuities",
    # "SP - Straighten Rows",
}


# NURBS
filepath_nurbs = "//..\..\SP - NURBS.blend"
obj_nurbs = {"NURBS Patch"}
gr_nurbs = {
    # "SP - NURBS Curve Meshing",
    "SP - NURBS Patch Meshing",
    "SP - NURBS Weighting",
    "SP - Set Knot NURBS Patch",
    "SP - NURBS to Bezier Patch [Naive slow]",
    "SP - Crop NURBS Patch",
    "SP - Insert Knot NURBS Patch",
    "SP - Curvature Analysis NURBS",
    "SP - Continuity Analysis",
}


# OTHER
filepath_other = "//..\..\SP - Other Primitives.blend"
# obj_other={""}
gr_other = {
    "SP - Cylindrical Meshing",
    "SP - Toroidal Meshing",
    "SP - Spherical Meshing",
    "SP - Conical Meshing",
    "SP - Surface of Extrusion Meshing",
    "SP - Surface of Revolution Meshing",
}

# SHAPES
filepath_preset = "//..\..\SP - Shapes presets.blend"
obj_preset = {"Quadaratic Dome", "Cubic Dome", "Torus", "Sphere", "Cone"}
coll_preset = {
    "Slab",
    "Cylinder",
    "Corner",
    "Step",
    "Thick Arch",
    "Tube",
    "Frame",
}


######  CATALOGS SETS  ######

full_set = (
    gr_surf
    | gr_curve_flat
    | gr_nurbs
    | gr_surf
    | gr_other
    | coll_preset
    | obj_probe
    | obj_curve_flat
    | obj_surf
    | obj_nurbs
    | obj_preset
    | {
        "SP - Connect Bezier Patch",
        "SP - Bezier Patch Meshing",
        # "SP - Auto Snap Continuities",
        "SP - Continuities Curve",
        "SP - Curve Meshing",
        "SP - Crop or Extend Curve",
        "SP - FlatPatch Meshing",
        "SP - Loft from Internal Curves",
    }
)

shape_set = obj_preset | coll_preset

bezier_patch_set = (
    (obj_surf
    | gr_surf
    | {"SP - Connect Bezier Patch", "SP - Bezier Patch Meshing"})
    - {
        "SP - Sew and Symmetrize",
        "SP - Displace Precisely",
        "Internal Curve For Patch",
        "SP - Convert Flat Patch to Bezier Patch",
        "SP - Select Patch Range",
        "SP - Project Curve on Bezier Patch",
        "SP - Curvature Analysis",
        "SP - Convert Contour",
        "SP - Copy Flat Patch as Trim Contour",
        "SP - Copy Segment",
        "SP - Nearest Curve on Bezier Patch",
        "SP - Flatten Patch",
        "SP - Patch Exact Normals",
        "SP - Ruled Surface from Mesh Loop",
        "SP - Flatten Patch Side",
    }
)

curve_flat_set = (
    (obj_curve_flat
    | gr_curve_flat
    | {
        "SP - Project Curve on Bezier Patch",
        "SP - Nearest Curve on Bezier Patch",
        "SP - Crop or Extend Curve",
        "SP - Curve Meshing",
        "SP - FlatPatch Meshing",
        "SP - Convert Flat Patch to Bezier Patch",
    })
    - {"SP - Project on Flat Patch"}
)

nurbs_set = obj_nurbs | gr_nurbs - {"SP - Continuity Analysis"}


def replace_duplicates():
    print("\n\n______________________________________________________\n")
    print("Manual deduplication..\n")
    
    #############################
    #         DANGER            #          
    # May remove different node #
    #   groups with same name   #
    #############################
    
    duplicated_list = []
    for ng in bpy.data.node_groups:
        if ng.name[-4] ==".":
            duplicated_list.append(ng.name[:-4])
    duplicated_groups = set(duplicated_list)
    
    replace_pairs = []
    for d in duplicated_groups :
        replace_pairs.append((d+".*",d))
    
    for p in replace_pairs : 
        bpy.ops.object.sp_replace_node_group(target_name = p[0], new_name = p[1])
        
        



def clear_unused_data():
    print("\n\n______________________________________________________\n")
    print("Clearing unused data..\n")
    # clear unused data. Do several times to fake recursive
    for ng in bpy.data.node_groups:
        if ng.asset_data == None:
            if ng.use_fake_user:
                ng.use_fake_user = False
            if ng.users == 0:
                bpy.data.node_groups.remove(ng)

    for ng in bpy.data.node_groups:
        if ng.users == 0 and ng.asset_data == None:
            bpy.data.node_groups.remove(ng)

    for ng in bpy.data.node_groups:
        if ng.users == 0 and ng.asset_data == None:
            bpy.data.node_groups.remove(ng)

    for ng in bpy.data.node_groups:
        if ng.users == 0 and ng.asset_data == None:
            bpy.data.node_groups.remove(ng)

    for ng in bpy.data.node_groups:
        if ng.users == 0 and ng.asset_data == None:
            bpy.data.node_groups.remove(ng)

    for ng in bpy.data.node_groups:
        if ng.users == 0 and ng.asset_data == None:
            bpy.data.node_groups.remove(ng)

    for ng in bpy.data.node_groups:
        if ng.users == 0 and ng.asset_data == None:
            bpy.data.node_groups.remove(ng)


if __name__ == "__main__":
    delete_all_data()

    print("\n\n\n\n______________________________________________________")
    print("______________________________________________________\n")
    print("\n\n______________________________________________________\n")
    print("Appending Groups..\n")

    append_node_group_by_names(filepath_curve_flat, gr_curve_flat)
    append_node_group_by_names(filepath_surf, gr_surf)
    append_node_group_by_names(filepath_nurbs, gr_nurbs)
    append_node_group_by_names(filepath_other, gr_other)

    print("\n\n______________________________________________________\n")
    print("Appending Objects..\n")
    append_objs_by_names(filepath_probe, obj_probe)
    append_objs_by_names(filepath_curve_flat, obj_curve_flat)
    append_objs_by_names(filepath_surf, obj_surf)
    append_objs_by_names(filepath_nurbs, obj_nurbs)
    append_objs_by_names(filepath_preset, obj_preset)

    print("\n\n______________________________________________________\n")
    print("Appending Collections..\n")
    append_collections_by_names(filepath_preset, coll_preset)

    print("\n\n______________________________________________________\n")
    print("Make Local..\n")
    bpy.ops.object.make_local(type="ALL")
    replace_duplicates()
    clear_unused_data()

    print("\n\n______________________________________________________\n")
    print("Assign to catalogs..\n")
    assign_assets_to_catalog(full_set, "SurfacePsycho/Common")
    assign_assets_to_catalog(nurbs_set, "SurfacePsycho/NURBS Patch")
    assign_assets_to_catalog(bezier_patch_set, "SurfacePsycho/Bezier Patch")
    assign_assets_to_catalog(curve_flat_set, "SurfacePsycho/Curve & FlatPatch")
    assign_assets_to_catalog(shape_set, "SurfacePsycho/Shape")
