#!/usr/bin/env python3
"""
Generator for creating modifier links in 3.-Modifers-and-Tools.md
Scans the gn-assets folder and generates markdown links for all files.
"""

# import os
import re
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.parent


def format_url_name(filename):
    """Convert filename to URL format by replacing spaces with dashes and removing .md extension."""
    # Remove .md extension
    name = filename.replace(".md", "")
    # Replace spaces with dashes
    url_name = name.replace(" ", "-")
    return url_name


def get_all_modifier_doc_files():
    """Get all .md files from gn-assets folder, including subfolders."""
    workspace_root = WORKSPACE_ROOT
    gn_assets_path = workspace_root / "gn-assets"

    if not gn_assets_path.exists():
        print(f"Error: gn-assets folder not found at {gn_assets_path}")
        return []

    files = []
    for file in sorted(gn_assets_path.rglob("*.md")):
        if file.is_file():
            files.append(file)

    return files


def get_category_parts(file_path, gn_assets_path):
    """Return the list of folder names for a file path."""
    try:
        relative_parent = file_path.parent.relative_to(gn_assets_path)
    except ValueError:
        return ["Uncategorized"]
    if relative_parent.parts:
        return list(relative_parent.parts)
    return ["Uncategorized"]


def add_nested_link(group, categories, link):
    """Add a link to a nested category group structure."""
    node = group.setdefault(categories[0], {"links": [], "children": {}})
    if len(categories) == 1:
        node["links"].append(link)
    else:
        add_nested_link(node["children"], categories[1:], link)


def count_links(group):
    """Count links stored in a nested category group."""
    total = 0
    for node in group.values():
        total += len(node["links"])
        total += count_links(node["children"])
    return total


def render_grouped_links(group, heading_level=2):
    """Render grouped links as nested markdown headings."""
    output = ""
    for category in sorted(group.keys(), key=str.casefold):
        node = group[category]
        output += f"{'#' * heading_level} {category}\n"
        for _, link in sorted(node["links"], key=lambda item: item[0].lower()):
            output += f"{link}\n"
        if node["children"]:
            output += "\n" + render_grouped_links(node["children"], heading_level + 1)
        output += "\n"
    return output


def generate_modifier_links():
    """Generate markdown links for all modifiers grouped by category."""
    workspace_root = WORKSPACE_ROOT
    gn_assets_path = workspace_root / "gn-assets"
    files = get_all_modifier_doc_files()

    if not files:
        print("No .md files found in gn-assets folder")
        return {}

    grouped_links = {}
    for file_path in files:
        categories = get_category_parts(file_path, gn_assets_path)
        display_name = file_path.stem
        url_name = format_url_name(display_name)
        link = f"* [`{display_name}`](https://github.com/RomainGuimbal/SurfacePsycho/wiki/{url_name})"
        add_nested_link(grouped_links, categories, (display_name, link))

    return grouped_links


def update_modifiers_tools_file():
    """Update the 3.-Modifers-and-Tools.md file with generated links."""
    workspace_root = WORKSPACE_ROOT
    md_file = workspace_root / "3.-Modifers-and-Tools.md"

    if not md_file.exists():
        print(f"Error: {md_file} not found")
        return False

    grouped_links = generate_modifier_links()
    if not grouped_links:
        print("No links generated")
        return False

    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    generated_individual = "# Individual Modifiers, Node groups and Tools\n\n"
    generated_individual += render_grouped_links(grouped_links, heading_level=2)
    generated_individual = generated_individual.rstrip()

    # Replace entire Individual Modifiers block up to the next major section
    individual_pattern = r"# Individual Modifiers, Node groups and Tools\n(.*?)(?=\n<!-- Section end -->)"
    content = re.sub(individual_pattern, generated_individual, content, flags=re.DOTALL)

    with open(md_file, "w", encoding="utf-8") as f:
        f.write(content)

    total_links = count_links(grouped_links)
    print(f"✓ Successfully updated {md_file}")
    print(f"✓ Generated {total_links} modifier links")
    return True


def generate_links():
    print("Modifier Links Generator")
    print("-" * 50)

    grouped_links = generate_modifier_links()
    total = count_links(grouped_links)
    print(f"\nFound {total} modifier files in gn-assets/\n")
    print("Sample links:")
    sample_count = 0
    for category in sorted(grouped_links.keys(), key=str.casefold):
        node = grouped_links[category]
        for _, link in sorted(node["links"], key=lambda item: item[0].lower()):
            if sample_count >= 3:
                break
            print(link)
            sample_count += 1
        if sample_count >= 3:
            break
        if node["children"]:
            # Only print first few links of nested section if samples remain
            for sub_link in render_grouped_links(
                node["children"], heading_level=0
            ).splitlines():
                if sample_count >= 3:
                    break
                if sub_link.startswith("* "):
                    print(sub_link)
                    sample_count += 1
            if sample_count >= 3:
                break
    if total > 3:
        print(f"... and {total - 3} more\n")

    # Update the file
    success = update_modifiers_tools_file()

    if success:
        print("\n✓ Generation complete!")
    else:
        print("\n✗ Generation failed!")


if __name__ == "__main__":
    generate_links()
