# Known Problems in the Blender Model

## Stale SP Type Attributes on Plain Mesh Objects

### Problem

The scene contains plain Blender mesh objects (`Cube`, `Cube.004`, `Cube.008`, `Cube.012`) that carry a SurfacePsycho type attribute (`SP_type = BEZIER_SURFACE`) but have no SurfacePsycho geometry nodes modifier and no SP-specific mesh attributes (`CP_count`, `CP_any_order_surf`, etc.).

During STEP export, SurfacePsycho identifies these objects as Bezier surfaces and attempts to convert them. The conversion fails immediately because the expected attributes are absent. In the current patched code these objects are safely skipped with a warning, but they are not exported.

### How to Identify

In the terminal output after export, look for lines of the form:

```
[SP] Skipping 'Cube' (type=SP_obj_type.BEZIER_SURFACE): "'CP_count' attribute missing ...
```

### Recommended Fix

In Blender, locate and delete these objects:

1. Open the Outliner (top-right panel)
2. Search for objects named `Cube`, `Cube.004`, `Cube.008`, `Cube.012`
3. Verify they are plain mesh cubes with no SurfacePsycho modifiers
4. Delete them (X key or right-click → Delete)

If any of these cubes are needed in the scene for reference or other purposes, the SP type attribute can be cleared instead. With the SurfacePsycho addon enabled, the attribute can be removed via the object's custom properties panel, or by running the following in the Blender Python console:

```python
import bpy
for name in ["Cube", "Cube.004", "Cube.008", "Cube.012"]:
    obj = bpy.data.objects.get(name)
    if obj and "SP_type" in obj.data.attributes:
        obj.data.attributes.remove(obj.data.attributes["SP_type"])
```

### Why This Happens

SurfacePsycho stores the surface type as a mesh attribute (`SP_type`) on the object's data. If a plain Blender primitive (such as the default cube added when creating a new scene) is present in the same collection as SP objects, it can accidentally inherit or acquire this attribute — for example through a copy/paste operation, a join, or a geometry nodes modifier that was later removed without clearing its outputs.
