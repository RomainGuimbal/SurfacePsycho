import bpy

def print_all_assets():
    """Print all assets marked in the current Blender file"""
    
    print("\n" + "="*50)
    print("ASSETS IN CURRENT FILE")
    print("="*50 + "\n")
    
    asset_count = 0
    
    # Check all data blocks that can be assets
    data_categories = [
        ("Objects", bpy.data.objects),
        ("Materials", bpy.data.materials),
        ("Node Groups", bpy.data.node_groups),
        ("Collections", bpy.data.collections),
        ("Meshes", bpy.data.meshes),
        ("Images", bpy.data.images),
        ("Textures", bpy.data.textures),
        ("Brushes", bpy.data.brushes),
        ("Worlds", bpy.data.worlds),
        ("Actions", bpy.data.actions),
    ]
    
    for category_name, data_collection in data_categories:
        assets_in_category = []
        
        for item in data_collection:
            if hasattr(item, 'asset_data') and item.asset_data is not None:
                assets_in_category.append(item.name)
                asset_count += 1
        
        if assets_in_category:
            print(f"{category_name}:")
            for asset_name in assets_in_category:
                print(asset_name)
            print()
    
    print("="*50)
    print(f"Total assets found: {asset_count}")
    print("="*50 + "\n")

# Run the function
print_all_assets()