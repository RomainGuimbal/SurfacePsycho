from pathlib import Path
import os
import re
from pathlib import Path
from ..common.asset_list import ASSET_NODE_GROUPS

# PATHS
DOC_ROOT = Path(__file__).parent
PATH_TO_ASSET_ENUMS = DOC_ROOT.parent.resolve() / "common"
MODIFIERS_PATH = DOC_ROOT / "Modifiers"

existing_files = [
    name[:-3]
    for root, dirs, files in os.walk(MODIFIERS_PATH)
    for name in files
    if name.endswith((".md"))
]

for asset in ASSET_NODE_GROUPS:
    if asset not in existing_files:
        path = MODIFIERS_PATH / f"{asset}.md"
        file = open(path, "w")

def get_all_modifier_doc_files():
    """Get all .md files from gn-assets folder, including subfolders."""
    gn_assets_path = MODIFIERS_PATH

    if not gn_assets_path.exists():
        print(f"Error: gn-assets folder not found at {gn_assets_path}")
        return []

    files = []
    for file in sorted(gn_assets_path.rglob("*.md")):
        if file.is_file():
            files.append(file)

    return files
