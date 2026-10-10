from pathlib import Path
import sys
import os
from nav_buttons_generator import generate_nav_buttons
from modifiers_links_generator import generate_links

# PATHS
# ----------------------------------------------------------
PATH_TO_ASSET_ENUMS = (
    Path(__file__).parent.parent.parent.resolve() / "SurfacePsycho/common"
)
if not PATH_TO_ASSET_ENUMS.is_dir():
    print(f"Error: '{PATH_TO_ASSET_ENUMS}' is not a directory.")

sys.path.insert(1, str(PATH_TO_ASSET_ENUMS))
from asset_list import ASSET_NODE_GROUPS

wiki_dir = Path(__file__).parent.parent.resolve()
wiki_assets = wiki_dir / "gn-assets"
if not wiki_assets.is_dir():
    print(f"Error: '{wiki_assets}' is not a directory.")
# ----------------------------------------------------------

existing_files = [
    name[:-3]
    for root, dirs, files in os.walk(wiki_assets)
    for name in files
    if name.endswith((".md"))
]

for asset in ASSET_NODE_GROUPS:
    if asset not in existing_files:
        path = wiki_assets / f"{asset}.md"
        file = open(path, "w")



generate_links()


generate_nav_buttons()
# ideally, they would follow hierarchy :/