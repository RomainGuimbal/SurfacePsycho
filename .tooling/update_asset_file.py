import sys
import uuid
from pathlib import Path

import bpy
from packaging.version import Version

# Paths ######################################################################

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent  # surfacepsycho/
QUEST_ROOT = REPO_ROOT.parent  # folder holding the source .blend files
ADDON_DIR = REPO_ROOT / "src" / "surfacepsycho"
FEATURES_TABLE_PATH = REPO_ROOT / "docs" / "features_table.yaml"
ASSET_LIST_PATH = ADDON_DIR / "common" / "asset_list.py"

FILE_PATH = Path(bpy.data.filepath).resolve()
ASSETS_DIR = FILE_PATH.parent  # folder holding assets.blend

# Blender resolves catalogs from the asset library root, so the source files and
# the destination file each need their own catalog definition file.
SOURCE_CATALOG_FILE = QUEST_ROOT / "blender_assets.cats.txt"
CATALOG_FILE = ASSETS_DIR / "blender_assets.cats.txt"

sys.path.insert(0, str(ADDON_DIR))

from common import enums, version_utils

VERSION = Version(enums.VERSION_STR)
set_nodes_version = version_utils.set_nodes_version
replace_duplicates = version_utils.replace_duplicates

RED = "\033[91m"
GREEN = "\033[32m"
BLUE = "\033[94m"
RESET = "\033[0m"

TABLE_ID_PREFIX = "- id: "
TABLE_FILE_KEY = "  file:"

# Node group .blend file holding each set of asset_list.py, in append order.
NODE_GROUP_FILES = {
    "SP Assets Level 0.blend": "ASSET_NODE_GROUPS_LEVEL_0",
    "SP Assets Level 1.blend": "ASSET_NODE_GROUPS_LEVEL_1",
    "SP Assets Level 2.blend": "ASSET_NODE_GROUPS_LEVEL_2",
    "SP - Curve and FlatPatch.blend": "ASSET_NODE_GROUPS_CURVE_AND_FLATPATCH",
    "SP - Bezier surface.blend": "ASSET_NODE_GROUPS_BEZIER_PATCH",
    "SP - NURBS.blend": "ASSET_NODE_GROUPS_NURBS_PATCH",
    "SP - Other Primitives.blend": "ASSET_NODE_GROUPS_OTHER_SURFACES",
    "SP - Compound.blend": "ASSET_NODE_GROUPS_COMPOUND",
}


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


def read_catalogs(catalog_file):
    """Map catalog UUIDs to their simple names."""
    catalogs = {}
    with open(catalog_file, "r") as f:
        for line in f:
            if line.startswith(("#", "VERSION", "\n")) or line.strip() == "":
                continue

            # Each line format: 'uuid:catalog_path:catalog_name'
            parts = line.strip().split(":")

            if len(parts) >= 3:
                catalogs[parts[0]] = parts[2]
    return catalogs


def clear_and_create_catalogs(cat_names):
    # Clear the catalog file (or create it if it doesn't exist)
    with open(CATALOG_FILE, "w") as f:
        f.write("# This is an Asset Catalog Definition file for Blender.\n")
        f.write("#\n")
        f.write("# Empty lines and lines starting with `#` will be ignored.\n")
        f.write("# The first non-ignored line should be the version indicator.\n")
        f.write(
            '# Other lines are of the format "UUID:catalog/path/for/assets:simple catalog name"\n\n'
        )
        f.write("VERSION 1\n\n")

    print(f"Cleared catalog file at: {CATALOG_FILE}")

    # Create new catalogs
    new_catalogs = []
    for c in cat_names:
        if c == "SurfacePsycho":
            new_catalogs.append((c, c))
        else:
            new_catalogs.append((c, "SurfacePsycho/" + c))

    # Append new catalogs to the file
    with open(CATALOG_FILE, "a") as f:
        for catalog_name, catalog_path in new_catalogs:
            catalog_uuid = str(uuid.uuid4())
            f.write(f"{catalog_uuid}:{catalog_path}:{catalog_name}\n")
            print(f"Created catalog: {catalog_name} ({catalog_path})")


def get_catalog_uuid(catalog_identifier):
    catalog_uuid = None

    with open(CATALOG_FILE, "r") as f:
        for line in f.readlines():
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
                f"Error: Catalog '{catalog_identifier}' not found in {CATALOG_FILE}"
            )
    return catalog_uuid


def assign_asset_to_catalog(asset_name, catalog_identifier):
    catalog_uuid = get_catalog_uuid(catalog_identifier)
    asset = None

    # Check different data types
    if asset_name in bpy.data.collections:
        asset = bpy.data.collections[asset_name]
    elif asset_name in bpy.data.objects:
        asset = bpy.data.objects[asset_name]
    elif asset_name in bpy.data.node_groups:
        asset = bpy.data.node_groups[asset_name]
    elif asset_name in bpy.data.materials:
        asset = bpy.data.materials[asset_name]
    elif asset_name in bpy.data.meshes:
        asset = bpy.data.meshes[asset_name]
    else:
        print(f"Asset '{asset_name}' not found in any data category")

    # Assign to catalog if it is an asset
    if asset.asset_data is not None:
        asset.asset_data.catalog_id = catalog_uuid
        asset.asset_data.license = "GPL 3.0"
        asset.asset_data.copyright = "2026 Romain Guimbal"
        asset.asset_data.author = "Romain Guimbal"
    else:
        raise ValueError(f"'{asset_name}' is not marked as an asset")


def append_by_name(filepath, asset_names, asset_type="node_groups"):
    # Determine which data block to access
    datablock_path = {
        "node_groups": "node_groups",
        "objects": "objects",
        "collections": "collections",
    }.get(asset_type, "node_groups")

    filepath = str(filepath)

    # link = False parce que link = True ne conserve pas les asset_data
    with bpy.data.libraries.load(filepath, link=False, assets_only=True) as (
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

    # Read catalog definition file of the source library
    catalogs_id_name_pairs = read_catalogs(SOURCE_CATALOG_FILE)

    # Assign to catalog
    for item in loaded_data:
        if item and item.asset_data:
            catalog_id = item.asset_data.catalog_id
            try:
                catalog_name = catalogs_id_name_pairs[catalog_id]
            except KeyError:
                print(f"{item.name} is not in a catalog")
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


def remove_fake_user_node_groups():
    for ng in bpy.data.node_groups:
        if ng.use_fake_user and ng.asset_data is None:
            ng.use_fake_user = False


def hide_manage_panel():
    for ng in bpy.data.node_groups:
        if ng.type == "GEOMETRY":
            ng.show_modifier_manage_panel = False

    for o in bpy.data.objects:
        for m in o.modifiers:
            if m.type == "NODES":
                m.show_manage_panel = False


def read_features_table():
    """Map each node group .blend file to the assets the table files under it.

    The `file:` column of docs/features_table.yaml is the reference: an asset is
    appended from the file it names there. Assets filed under no known file are
    returned separately.
    """
    entries = []
    name = None
    file_name = None
    for line in FEATURES_TABLE_PATH.read_bytes().decode("utf-8").splitlines():
        if line.startswith(TABLE_ID_PREFIX):
            if name is not None:
                entries.append((name, file_name))
            name = line[len(TABLE_ID_PREFIX) :].strip()
            file_name = None
        elif line.startswith(TABLE_FILE_KEY):
            file_name = line[len(TABLE_FILE_KEY) :].strip()

    if name is not None:
        entries.append((name, file_name))

    sources = {file_name: set() for file_name in NODE_GROUP_FILES}
    for name, file_name in entries:
        if file_name in sources:
            sources[file_name].add(name)

    return sources, [name for name, file_name in entries if file_name not in sources]


def write_asset_list(sources):
    """Regenerate asset_list.py from the features table."""
    text = ASSET_LIST_PATH.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in text else "\n"

    lines = []
    for file_name, set_name in NODE_GROUP_FILES.items():
        lines.append(f"{set_name} = {{")
        lines.extend(f'    "{name}",' for name in sorted(sources[file_name]))
        lines.append("}")
        lines.append("")

    set_names = list(NODE_GROUP_FILES.values())
    lines.append("ASSET_NODE_GROUPS = (")
    lines.append(f"    {set_names[0]}")
    lines.extend(f"    | {set_name}" for set_name in set_names[1:])
    lines.append(")")

    ASSET_LIST_PATH.write_bytes((eol.join(lines) + eol).encode("utf-8"))
    return sum(len(names) for names in sources.values())


############################################################################################
############################################################################################
############################################################################################


################################
#                              #
#          TO IMPORT           #
#                              #
################################

# PROBE
path_probe = QUEST_ROOT / "Principal curvature.blend"
obj_probe = {"SP - Curvatures Probe"}

# CURVE
path_curve_flat = QUEST_ROOT / "SP - Curve and FlatPatch.blend"
obj_curve_flat = {
    "FlatPatch",
    "PsychoCurve",
}

# BEZIER SURF
path_surf = QUEST_ROOT / "SP - Bezier surface.blend"
obj_surf = {
    "Bezier Patch",
    "Internal Curve For Patch",
}

# NURBS
path_nurbs = QUEST_ROOT / "SP - NURBS.blend"
obj_nurbs = {"NURBS Patch"}

# SHAPES
path_preset = QUEST_ROOT / "SP - Shapes presets.blend"
obj_preset = {
    "Compound",
    "Text Compound",
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
    "Oblong Slab",
    "Revolution",
    "Cable",
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
    sources, unlocated = read_features_table()

    print("\n______________________________________________________\n")
    print(f"Appending Groups..{RED}")
    for file_name in NODE_GROUP_FILES:
        append_by_name(QUEST_ROOT / file_name, sources[file_name], "node_groups")

    print(f"{RESET}\n______________________________________________________\n")
    print("Appending Objects..")
    append_by_name(path_probe, obj_probe, "objects")
    append_by_name(path_curve_flat, obj_curve_flat, "objects")
    append_by_name(path_surf, obj_surf, "objects")
    append_by_name(path_nurbs, obj_nurbs, "objects")
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

        hide_manage_panel()

    #    profiler.disable()
    #    profiler.print_stats()

    print("\n______________________________________________________\n")
    print("Update asset list..")
    count = write_asset_list(sources)
    print(f"{count} node groups written to {ASSET_LIST_PATH}")
    for name in unlocated:
        print(f'- "{name}" is filed under no known file')

    missing = []
    present = bpy.data.node_groups.keys()
    for names in sources.values():
        for ng in sorted(names):
            if ng not in present:
                missing.append(ng)

    # Blender refuses to overwrite a file that is currently loaded as a library.
    # Workaround: save to a temp path (copy=True keeps the session filepath unchanged),
    # then replace the real file with the temp file via Python.
    import shutil

    tmp_path = str(FILE_PATH) + ".saving_tmp"
    bpy.ops.wm.save_as_mainfile(filepath=tmp_path, copy=True)
    shutil.move(tmp_path, str(FILE_PATH))

    # Print Final status
    if len(missing) == 0:
        # Print Success
        print("\n" + GREEN + "=" * 50)
        print("\n         Assets successfully updated !\n")
        print("=" * 50 + RESET)
    else:
        print("\n" + RED + "=" * 50)
        print("\n         Missing node_groups\n")
        for m in missing:
            print(f'- "{m}"')
        print("=" * 50 + RESET)

# TODO missing objects
