import bpy
from pathlib import Path
import re
import uuid
import sys

FILE_PATH = Path(bpy.data.filepath)


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


def clear_and_create_catalogs(cat_names):
    catalog_file = FILE_PATH.parent / "blender_assets.cats.txt"

    # Clear the catalog file (or create it if it doesn't exist)
    with open(catalog_file, "w") as f:
        f.write("# This is an Asset Catalog Definition file for Blender.\n")
        f.write("#\n")
        f.write("# Empty lines and lines starting with `#` will be ignored.\n")
        f.write("# The first non-ignored line should be the version indicator.\n")
        f.write(
            '# Other lines are of the format "UUID:catalog/path/for/assets:simple catalog name"\n\n'
        )
        f.write("VERSION 1\n\n")

    print(f"Cleared catalog file at: {catalog_file}")

    # Create new catalogs
    new_catalogs = []
    for c in cat_names:
        if c == "SurfacePsycho":
            new_catalogs.append((c, c))
        else:
            new_catalogs.append((c, "SurfacePsycho/" + c))

    # Append new catalogs to the file
    with open(catalog_file, "a") as f:
        for catalog_name, catalog_path in new_catalogs:
            catalog_uuid = str(uuid.uuid4())
            f.write(f"{catalog_uuid}:{catalog_path}:{catalog_name}\n")
            print(f"Created catalog: {catalog_name} ({catalog_path})")


def get_catalog_uuid(catalog_identifier, folder):
    catalog_uuid = None

    with (folder / "blender_assets.cats.txt").open() as f:
        for line_num, line in enumerate(f.readlines(), 1):
            if line.startswith(("#", "VERSION", "\n")) or line.strip() == "":
                continue

            # Each line format: 'uuid:catalog_path:catalog_name'
            parts = line.strip().split(":")

            if len(parts) >= 3:
                uuid = parts[0]
                catalog_path = parts[1]
                catalog_name = parts[2]

                # Check if the identifier matches either the path or the name
                if (
                    catalog_identifier == catalog_path
                    or catalog_identifier == catalog_name
                ):
                    catalog_uuid = uuid
                    break

        if not catalog_uuid:
            raise ValueError(
                f"Error: Catalog '{catalog_identifier}' not found in blender_assets.cats.txt"
            )
    return catalog_uuid


def assign_asset_to_catalog(asset_name, catalog_identifier):
    folder = FILE_PATH.parent

    catalog_uuid = get_catalog_uuid(catalog_identifier, folder)

    asset = None

    # Check different data types
    if asset_name in bpy.data.collections.keys():
        asset = bpy.data.collections[asset_name]
    elif asset_name in bpy.data.objects.keys():
        asset = bpy.data.objects[asset_name]
    elif asset_name in bpy.data.node_groups.keys():
        asset = bpy.data.node_groups[asset_name]
    elif asset_name in bpy.data.materials.keys():
        asset = bpy.data.materials[asset_name]
    elif asset_name in bpy.data.meshes.keys():
        asset = bpy.data.meshes[asset_name]
    else:
        print(f"Asset '{asset_name}' not found in any data category")

    # Assign to catalog if it's an asset
    if asset.asset_data is not None:
        asset.asset_data.catalog_id = catalog_uuid
        asset.asset_data.author = "Romain Guimbal"
    else:
        raise ValueError(f"'{asset_name}' is not marked as an asset")


def replace_all_instances_of_node_group(target_node_group_name, new_node_group_name):
    # Get the target node group
    prefix, suffix = target_node_group_name[:-2], target_node_group_name[-2:]

    if suffix == ".*":
        pattern = rf"^{re.escape(prefix)}\.(\d{{3}}|\d{{3}}\.\d{{3}})$"
        target_node_groups = [
            ng for ng in bpy.data.node_groups if re.match(pattern, ng.name)
        ]
    else:
        target_node_groups = [bpy.data.node_groups.get(target_node_group_name)]

    # Get the new node group
    new_node_group = bpy.data.node_groups.get(new_node_group_name)
    if not new_node_group:
        return 0  # New node group not found

    if len(target_node_groups) > 0:
        for t in target_node_groups:
            if t and t != new_node_group:
                # Replace the node group data
                t.user_remap(new_node_group)

                # Remove the old node group
                bpy.data.node_groups.remove(t)

        return len(target_node_groups)
    else:
        return -1


def append_by_name(path, asset_names, asset_type="node_groups"):
    # Determine which data block to access
    datablock_path = {
        "node_groups": "node_groups",
        "objects": "objects",
        "collections": "collections",
    }.get(asset_type, "node_groups")

    # link = False parce que link = True ne conserve pas les asset_data
    with bpy.data.libraries.load(path, link=False, assets_only=True) as (
        data_from,
        data_to,
    ):
        # Get all available names from the file
        available = getattr(data_from, datablock_path)

        # Load only the assets we need
        for name in asset_names:
            if name in available:
                getattr(data_to, datablock_path).append(name)

    # Access the loaded assets and get their catalog IDs
    loaded_data = getattr(data_to, datablock_path)

    # Read catalog definition file
    catalogs_id_name_pairs = {}
    for item in loaded_data:
        if item and item.asset_data:
            catalog_id = item.asset_data.catalog_id
            catalog_file = (FILE_PATH.parent.parent.parent).joinpath(
                "blender_assets.cats.txt"
            )
            with open(catalog_file, "r") as f:
                for line in f:
                    if line.startswith(("#", "VERSION", "\n")) or line.strip() == "":
                        continue

                    # Each line format: 'uuid:catalog_path:catalog_name'
                    parts = line.strip().split(":")

                    if len(parts) >= 3 and parts[0] == str(catalog_id):
                        catalogs_id_name_pairs[catalog_id] = parts[2]

    # Assign to catalog
    for item in loaded_data:
        if item and item.asset_data:
            catalog_id = item.asset_data.catalog_id
            try:
                catalog_name = catalogs_id_name_pairs[catalog_id]
            except KeyError:
                print(f"{item.name} has invalid catalog id {str(catalog_id)}")
                continue
            assign_asset_to_catalog(item.name, catalog_name)

    # link object
    if asset_type == "objects":
        for obj in data_to.objects:
            if obj is not None:
                bpy.context.collection.objects.link(obj)
                obj.location = (0, 0, 0)

    # Link collections
    elif asset_type == "collections":
        for collection in data_to.collections:
            if collection is not None:
                bpy.context.scene.collection.children.link(collection)

    return


def replace_duplicates():

    #############################
    #         DANGER            #
    # May remove different node #
    #   groups with same name   #
    #############################

    duplicated_list = []
    for ng in bpy.data.node_groups:
        if ng.name[-4] == ".":
            duplicated_list.append(ng.name[:-4])
            # print(ng.name)
    duplicated_groups = set(duplicated_list)

    for d in duplicated_groups:
        replaced = replace_all_instances_of_node_group(d + ".*", d)
        if replaced <= 0:
            print(f"No instances of {d}.* found")


def remove_fake_user_node_groups():
    for ng in bpy.data.node_groups:
        if ng.use_fake_user and ng.asset_data is None:
            ng.use_fake_user = False


############################################################################################
############################################################################################
############################################################################################


################################
#                              #
#          TO IMPORT           #
#                              #
################################

# PROBE
path_probe = "//..\..\Principal curvature.blend"
obj_probe = {"SP - Curvatures Probe"}

# CURVE
path_curve_flat = "//..\..\SP - Curve and FlatPatch.blend"
obj_curve_flat = {
    "FlatPatch",
    "PsychoCurve",
}
gr_curve_flat = {
    # "SP - Bezier Circlular Arc",
    "SP - Blend Curve",
    #    "SP - Compose FlatPatch From Sides",
    "SP - Continuities between Segments",
    "SP - Convert Circles and Ellipses to Splines",
    "SP - Copy Mesh Face",
    # "SP - Curve on Surface from UV",
    "SP - Distance Between Curves",
    "SP - Fillet Curve or FlatPatch",
    "SP - Fillet Polyline with Circles",
    "SP - Fit Curve",
    "SP - Inset FlatPatch",
    "SP - Intervale Curve",
    "SP - Make SVG Ready",
    "SP - Mirror Curve Control Points",
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
    "SP - Interpolate Curve or FlatPatch",
    "SP - Crown Curve",
    "SP - Connect Curve",
    "SP - Curve Meshing",
    "SP - Crop or Extend Curve",
    "SP - Offset Curve",
    "SP - FlatPatch Meshing",
}

# BEZIER SURF
path_surf = "//..\..\SP - Bezier surface.blend"
obj_surf = {
    "Bezier Patch",
    "Internal Curve For Patch",
}
gr_surf = {
    "SP - Bezier Patch Meshing",
    "SP - Auto Midpoints Linear",
    "SP - Blend Surfaces",
    "SP - Connect Bezier Patch",
    "SP - Convert Contour",
    "SP - Crop Patch to Point",
    "SP - Displace Bezier Patch Control Grid",
    "SP - Offset Precisely",
    "SP - Fillet Trim Contour",
    "SP - Flatten Patch",
    "SP - Flatten Patch Side",
    "SP - Gradient Map",
    "SP - Loft",
    "SP - Loft from Internal Curves",
    "SP - Mirror Patch Control Points",
    "SP - Nearest Curve on Bezier Patch",
    "SP - Patch Exact Normals",
    "SP - Project Curve on Bezier Patch",
    "SP - Raise or Lower Degree Bezier Patch",
    "SP - Reorder Grid Index",
    "SP - Ruled Surface from Mesh Loop",
    "SP - Select Patch Range",
    "SP - Convert Flat Patch to Bezier Patch",
    "SP - Trim Bezier Surface from Projected Wires",
}


# NURBS
path_nurbs = "//..\..\SP - NURBS.blend"
obj_nurbs = {"NURBS Patch"}
gr_nurbs = {
    "SP - NURBS Patch Meshing",
    "SP - NURBS Weighting",
    "SP - Set Knot NURBS Patch",
    "SP - Crop or Extend Patch",
    "SP - Insert Knot NURBS Patch",
    "SP - Curvature Analysis",
    "SP - Continuity Analysis",
    "SP - Fit Patch",
    "SP - Interpolate Patch",
    "SP_Curvature",
}


# OTHER
path_other = "//..\..\SP - Other Primitives.blend"
# obj_other={""}
gr_other = {
    "SP - Cylindrical Meshing",
    "SP - Toroidal Meshing",
    "SP - Spherical Meshing",
    "SP - Conical Meshing",
    "SP - Surface of Extrusion Meshing",
    "SP - Surface of Revolution Meshing",
    "SP - Plot Distance from Mesh",
    "SP - Copy Geometry",
}

# COMPOUND
path_compound = "//..\..\SP - Compound.blend"
gr_compound = {
    "SP - Compound Meshing",
    "SP - SubD to Compound",
    "SP - Poly to Compound",
    "SP - Text to Compound",
    "SP - Set Patch Intance Type",
    "SP - Split to Patches",
    "SP - Intersect Bezier Patches",
    "SP - Extrude FlatPatch",
    "SP - Interval Curves",
    "SP - NURBS to Bezier Patches",
}
obj_compound = {"Compound", "Text Compound"}

# SHAPES
path_preset = "//..\..\SP - Shapes presets.blend"
gr_preset = {"SP - Cylinder Compound",
             "SP - Disc CP",
             "SP - Frame Coumpound",
             "SP - Oblong Extrusion Compound",
             "SP - Slab Coumpound",
             "SP - Tubes Compound"}
obj_preset = {
    "Quadaratic Dome",
    "Cubic Dome",
    "Torus",
    "Sphere",
    "Cone",
    "Cube",
    "Cylinder",
    "Tube",
    "Slab",
    "Frame",
    "Oblong Tube",
    "Oblong Slab",
}
coll_preset = {
    "Corner",
    "Step",
    "Thick Arch",
}

################################
#                              #
#            MAIN              #
#                              #
################################

if __name__ == "__main__":
    isfast = False
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1 :]
        isfast = "--fast" in argv
    else:
        argv = []
        print("No command line arguments provided")

    #    import cProfile
    #    profiler = cProfile.Profile()
    #    profiler.enable()

    print("\n\n______________________________________________________")
    print("______________________________________________________\n")
    print("Deleting Data..")

    print("\n______________________________________________________\n")
    print("Create Catalogs..")
    delete_all_data()
    clear_and_create_catalogs(
        [
            "SurfacePsycho",
            "Analyse",
            "Convert",
            "Deform",
            "Edit",
            "Generate",
            "Meshing",
            "Shape",
            "Utility",
        ]
    )
    print("\n______________________________________________________\n")
    print("Appending Groups..")
    append_by_name(path_curve_flat, gr_curve_flat, "node_groups")
    append_by_name(path_surf, gr_surf, "node_groups")
    append_by_name(path_nurbs, gr_nurbs, "node_groups")
    append_by_name(path_other, gr_other, "node_groups")
    append_by_name(path_compound, gr_compound, "node_groups")
    append_by_name(path_preset, gr_preset, "node_groups")
    
    print("\n______________________________________________________\n")
    print("Appending Objects..")
    append_by_name(path_probe, obj_probe, "objects")
    append_by_name(path_curve_flat, obj_curve_flat, "objects")
    append_by_name(path_surf, obj_surf, "objects")
    append_by_name(path_nurbs, obj_nurbs, "objects")
    append_by_name(path_compound, obj_compound, "objects")
    append_by_name(path_preset, obj_preset, "objects")

    print("\n______________________________________________________\n")
    print("Appending Collections..")
    append_by_name(path_preset, coll_preset, "collections")

    if not isfast:
        print("\n______________________________________________________\n")
        print("Make Local..\n")

        bpy.ops.object.make_local(type="ALL")

        print("\n______________________________________________________\n")
        print("Replace duplicates..")

        replace_duplicates()

        print("\n______________________________________________________\n")
        print("Clear unused data..")

        remove_fake_user_node_groups()
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True, do_linked_ids=False, do_recursive=True
        )

    #    profiler.disable()
    #    profiler.print_stats()

    bpy.ops.wm.save_mainfile()

    print("\nAssets successfully updated !")
