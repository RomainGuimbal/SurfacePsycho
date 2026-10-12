from pathlib import Path
import os
import re
from pathlib import Path
from urllib.parse import quote
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
    """Print links to all files in the docs folder that have less than 4 lines written.

    Each line contains an OSC 8 hyperlink (Ctrl+click in the VS Code terminal)
    opening the file in the editor, followed by its line count.
    """
    root = Path(root)

    if not root.exists():
        print(f"Error: docs folder not found at {root}")
        return

    # Enable ANSI/VT escape processing on Windows consoles so OSC 8 works.
    if os.name == "nt":
        os.system("")

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
            abs_path = path.resolve()
            # vscode:// URI opens the file directly in VS Code (spaces are encoded).
            uri = "vscode://file/" + quote(str(abs_path).replace("\\", "/"), safe=":/")
            print(
                "\x1b]8;;"
                + uri
                + "\x1b\\"
                + path.name
                + "\x1b]8;;\x1b\\"
                + f" ({line_count} lines)"
            )



def derive_title_from_filename(path):
    """Derive a human-readable title from a markdown file name.

    Strips the extension and any leading numbering like '10-' or '80-',
    then replaces '-' and '_' separators with spaces.
    '80-Compatibility and Upgrade.md' -> 'Compatibility and Upgrade'
    """
    stem = Path(path).stem
    stem = re.sub(r"^\d+[-_.\s]+", "", stem)  # leading numbering ('10-', '80_', ...)
    title = re.sub(r"[-_]+", " ", stem).strip()
    return title


def add_missing_titles(root=DOC_ROOT):
    """Add a '# Title' heading to markdown files that don't already start with one.

    Only .md files are considered, and a file is left untouched if its first
    non-empty line is already a level-1 heading ('# ...'). Otherwise a title
    derived from the file name is inserted at the top of the file.

    Returns the list of modified file paths.
    """
    root = Path(root)

    if not root.exists():
        print(f"Error: docs folder not found at {root}")
        return []

    modified = []
    for path in sorted(root.rglob("*.md")):
        if not path.is_file():
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as e:
            print(f"Error: could not read {path}: {e}")
            continue

        # Find the first non-empty line.
        lines = content.splitlines()
        first_line = next((line.strip() for line in lines if line.strip()), "")

        if first_line.startswith("# "):
            continue  # Already has a title.

        title = derive_title_from_filename(path)
        if not title:
            continue

        if content and not content.startswith("\n"):
            content = f"# {title}\n\n{content}"
        else:
            content = f"# {title}\n{content}"

        try:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
        except OSError as e:
            print(f"Error: could not write {path}: {e}")
            continue

        modified.append(path)
        print(f"Added title '# {title}' to {path}")

    if not modified:
        print("No markdown files were missing a title.")

    return modified


# print_files_with_fewer_than_4_lines()
add_missing_titles()
