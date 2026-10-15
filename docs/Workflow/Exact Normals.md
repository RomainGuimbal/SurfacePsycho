# Exact Normals

By default SP doesn't calculate accurate normals on NURBS and Bezier patches because it has a significant performance cost. However you can switch it on per object, from the N panel or from the meshing modifier. Most of the difference is on the boundaries.
> For further quality you can enable [EEVEE high quality normals](https://docs.blender.org/manual/en/5.0/render/eevee/render_settings/performance.html#bpy-types-rendersettings-use-high-quality-normals)

## Enable them

### From the N-panel 
Applies to selected objects.

![panel toggle](../Images/exact-normals-n-panel.jpg)

### From Modifiers
Meshing modifier setting
![modifier toggle](<../Images/exact normals.jpg>)

## Comparison
|Default|Exact|Exact + High Quality|
|-|-|-|
| ![default normals](<../Images/normals default.jpg>) | ![exact normals](<../Images/normals exact.jpg>) | ![normals exact + high quality](<../Images/normals exact + high quality.jpg>) |