"""Fill the `file:` column of docs/features_table.yaml.

Every .blend file at the top level of the quest folder is opened to record the
node groups it owns locally (node groups linked from another file are ignored).
Each asset of the table then gets the name of the file it lives in, or `null`
when no file owns it.

Run with:
    blender --background --factory-startup --disable-autoexec \
        --python update_features_table.py
"""

from pathlib import Path

import bpy

# Paths ######################################################################

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent  # surfacepsycho/
QUEST_ROOT = REPO_ROOT.parent  # folder holding the source .blend files
TABLE_PATH = REPO_ROOT / "docs" / "features_table.yaml"

ID_PREFIX = "- id: "
FILE_KEY = "  file:"


def scan_files():
    """Map a node group name to the files owning it locally.

    Returns ({name: {file name: is marked as an asset}}, names only seen linked).
    """
    owners = {}
    linked = set()

    for blend_path in sorted(QUEST_ROOT.glob("*.blend")):
        try:
            bpy.ops.wm.open_mainfile(filepath=str(blend_path), load_ui=False)
        except RuntimeError as error:
            print(f"  ! {blend_path.name}: cannot open ({error})")
            continue

        local_count = 0
        for node_group in bpy.data.node_groups:
            if node_group.library is not None:  # linked from another file
                linked.add(node_group.name)
                continue
            local_count += 1
            owners.setdefault(node_group.name, {})[blend_path.name] = (
                node_group.asset_data is not None
            )
        print(f"  {blend_path.name}: {local_count} local node groups")

    return owners, linked


def pick_file(asset_id, candidates, current):
    """Choose the file that owns the asset.

    Prefers the file already recorded in the table, then a curated file (the
    experiments and tests also hold copies of the assets but are not where they
    belong), then a file where the node group is marked as an asset.
    """
    if not candidates:
        return None
    best = sorted(
        candidates,
        key=lambda name: (
            name != current,
            not name.startswith("SP"),
            not candidates[name],
            name,
        ),
    )
    if len(best) > 1:
        print(f"  ? {asset_id}: found in {best}, took {best[0]}")
    return best[0]


def split_entries(lines):
    """Return [asset id, first line index, last line index + 1] per entry."""
    entries = []
    for index, line in enumerate(lines):
        if line.startswith(ID_PREFIX):
            if entries:
                entries[-1][2] = index
            entries.append([line[len(ID_PREFIX) :].strip(), index, len(lines)])
    return entries


def yaml_value(text):
    if text is None:
        return "null"
    needs_quotes = any(char in text for char in '#:[]{},"\'') or text[0] in '-?!&*|>%@` '
    if needs_quotes:
        return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return text


def update_table(owners):
    text = TABLE_PATH.read_bytes().decode("utf-8")
    eol = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(eol)

    found = 0
    missing = []

    # Bottom to top so the indices of the remaining entries stay valid.
    for asset_id, first, last in reversed(split_entries(lines)):
        key_index = next(
            (
                index
                for index in range(first + 1, last)
                if lines[index].startswith(FILE_KEY)
            ),
            None,
        )
        current = None
        if key_index is not None:
            current = lines[key_index][len(FILE_KEY) :].strip().strip('"')
            if current == "null":
                current = None

        file_name = pick_file(asset_id, owners.get(asset_id, {}), current)
        if file_name is None:
            missing.append(asset_id)
        else:
            found += 1
        new_line = f"{FILE_KEY} {yaml_value(file_name)}"

        if key_index is not None:
            lines[key_index] = new_line
        else:
            insert_at = last
            while insert_at > first + 1 and lines[insert_at - 1].strip() == "":
                insert_at -= 1
            lines.insert(insert_at, new_line)

    TABLE_PATH.write_bytes(eol.join(lines).encode("utf-8"))
    return found, sorted(missing)


################################
#                              #
#            MAIN              #
#                              #
################################

if __name__ == "__main__":
    print(f"Scanning {QUEST_ROOT}")
    owners, linked = scan_files()

    found, missing = update_table(owners)

    print(f"\nWrote {TABLE_PATH}")
    print(f"{found} assets located")
    if missing:
        print(f"{len(missing)} assets without a file:")
        for asset_id in missing:
            reason = "only linked" if asset_id in linked else "in no file"
            print(f'- "{asset_id}" ({reason})')
