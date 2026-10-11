By default SP doesn't calculate accurate normals on NURBS and Bezier patches because it has a significant performance cost. However you can switch it on per object, from the N panel or from the meshing modifier. Most the difference is on boundaries.
> For further quality you can enable [EEVEE high quality normals](https://docs.blender.org/manual/en/5.0/render/eevee/render_settings/performance.html#bpy-types-rendersettings-use-high-quality-normals)

### N-panel toggle (applies to selected object)
<img width="250" height="auto" alt="image" src="https://github.com/user-attachments/assets/30bfa8d6-22c3-430b-933c-5bab2893f9cc" />

### Modifier toggle
<img width="250" height="auto" alt="image" src="https://github.com/user-attachments/assets/20d3da10-ccaa-4239-b578-a20d4c75e87a" />

# Comparison

|Default|Exact|Exact + High Quality|
|-|-|-|
|<img width="100%" height="auto" alt="normals default" src="https://github.com/user-attachments/assets/97f30f9a-bf19-483f-9c78-251a7a782a1c" />|<img width="100%" height="auto" alt="normals exact" src="https://github.com/user-attachments/assets/37176a2f-61bc-4e2f-af62-125c7f26a0f8" />|<img width="100%" height="auto" alt="normals exact + high quality" src="https://github.com/user-attachments/assets/002deff9-5aff-4a83-9eb9-a72fcb622fee" />|
