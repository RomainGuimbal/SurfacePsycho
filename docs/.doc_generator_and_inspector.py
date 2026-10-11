from pathlib import Path
import os
import re
from pathlib import Path
# from ..common.asset_list import ASSET_NODE_GROUPS

# PATHS
DOC_ROOT = Path(__file__).parent
PATH_TO_ASSET_ENUMS = DOC_ROOT.parent.resolve() / "common"
MODIFIERS_PATH = DOC_ROOT / "Modifiers"


# existing_files = [
#     name[:-3]
#     for root, dirs, files in os.walk(MODIFIERS_PATH)
#     for name in files
#     if name.endswith((".md"))
# ]

# for asset in ASSET_NODE_GROUPS:
#     if asset not in existing_files:
#         path = MODIFIERS_PATH / f"{asset}.md"
#         file = open(path, "w")

# def get_all_modifier_doc_files():
#     """Get all .md files from gn-assets folder, including subfolders."""
#     gn_assets_path = MODIFIERS_PATH

#     if not gn_assets_path.exists():
#         print(f"Error: gn-assets folder not found at {gn_assets_path}")
#         return []

#     files = []
#     for file in sorted(gn_assets_path.rglob("*.md")):
#         if file.is_file():
#             files.append(file)

#     return files


def print_files_with_fewer_than_4_lines(root=DOC_ROOT, min_lines=4):
    """Print the names of all files in the docs folder that have less than 4 lines written."""
    root = Path(root)

    if not root.exists():
        print(f"Error: docs folder not found at {root}")
        return

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                line_count = sum(1 for _ in f)
        except OSError as e:
            print(f"Error: could not read {path}: {e}")
            continue

        if line_count < min_lines:
            print(f"{path.name} ({line_count} lines)")
