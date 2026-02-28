import bpy
from pathlib import Path
import uuid
import sys
from ..common.enums import (
    ASSET_NODE_GROUPS_BEZIER_PATCH,
    ASSET_NODE_GROUPS_CURVE_AND_FLATPATCH,
    ASSET_NODE_GROUPS_NURBS_PATCH,
    ASSET_NODE_GROUPS_OTHER_SURFACES,
    ASSET_NODE_GROUPS_COMPOUND,
    ASSET_NODE_GROUPS_SHAPE_PRESETS,
)
from ..common.versioning import (
    set_nodes_version,
    replace_duplicates,
)

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

# BEZIER SURF
path_surf = "//..\..\SP - Bezier surface.blend"
obj_surf = {
    "Bezier Patch",
    "Internal Curve For Patch",
}

# NURBS
path_nurbs = "//..\..\SP - NURBS.blend"
obj_nurbs = {"NURBS Patch"}


# OTHER
path_other = "//..\..\SP - Other Primitives.blend"
# obj_other={""}

# COMPOUND
path_compound = "//..\..\SP - Compound.blend"

obj_compound = {"Compound", "Text Compound"}

# SHAPES
path_preset = "//..\..\SP - Shapes presets.blend"
obj_preset = {
    "Quadratic Dome",
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
    "Oblong Slab" "Revolution",
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
    append_by_name(
        path_curve_flat, ASSET_NODE_GROUPS_CURVE_AND_FLATPATCH, "node_groups"
    )
    append_by_name(path_surf, ASSET_NODE_GROUPS_BEZIER_PATCH, "node_groups")
    append_by_name(path_nurbs, ASSET_NODE_GROUPS_NURBS_PATCH, "node_groups")
    append_by_name(path_other, ASSET_NODE_GROUPS_OTHER_SURFACES, "node_groups")
    append_by_name(path_compound, ASSET_NODE_GROUPS_COMPOUND, "node_groups")
    append_by_name(path_preset, ASSET_NODE_GROUPS_SHAPE_PRESETS, "node_groups")

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

        set_nodes_version()

    #    profiler.disable()
    #    profiler.print_stats()

    bpy.ops.wm.save_mainfile()

    print("\nAssets successfully updated !")
