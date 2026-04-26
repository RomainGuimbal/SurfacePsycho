# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## What This Repo Is

This is **KS_SurfacePsycho** — a personal fork of the [SurfacePsycho](https://github.com/RomainGuimbal/SurfacePsycho) Blender add-on. The fork lives on the `ExportFixes` branch and exists to fix STEP/IGES export crashes in the upstream project. Changes are documented in `fixes.md` and `problems.md`.

SurfacePsycho is a Blender 5.1+ extension for NURBS/CAD surface modeling. All geometry lives in **Blender Geometry Nodes modifiers** (stored in `assets/assets.blend`). The Python code handles only I/O (STEP/IGES/SVG export, CAD import) and UI (panels, operators, overlays). There are no standalone Python tests.

---

## Build and Install

### Build the extension zip

This must be run on a Mac (the only wheel available is `macos-arm64`):

```bash
blender --command extension build --source-dir . --output-dir .
```

The sandbox (Linux) cannot run this. As a workaround, patch the existing zip by replacing modified files:

```python
import zipfile, os

src = 'surfacepsycho-0.10.0.zip'
out = '/tmp/surfacepsycho-0.10.0.zip'
modified = {'common/utils.py': 'common/utils.py', ...}  # map zip path → disk path

with zipfile.ZipFile(src, 'r') as zin:
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename in modified:
                zout.write(modified[item.filename], item.filename)
            else:
                zout.writestr(item, zin.read(item.filename))
```

Then copy the result back over the original zip.

### Install in Blender

1. Edit → Preferences → Add-ons → Install from Disk → select `surfacepsycho-0.10.0.zip`
2. Enable the add-on in the list (search "Surface Psycho")
3. The `user_default` version must be active — ignore any `blender_org` not-found warning (stale reference)

### Run Blender with terminal output (macOS)

```bash
/Applications/Blender_5.1.1.app/Contents/MacOS/Blender > /tmp/blender_startup.txt 2>&1
```

Use `faulthandler` in `export_process_cad.py` to get Python stack traces on hard crashes (SIGSEGV). It is already enabled there.

---

## Repo Layout

```
__init__.py              # Entry point: registers macros + gui
config.py                # bl_info dict
blender_manifest.toml    # Extension metadata, platform, wheel declarations
assets/assets.blend      # All GN node groups (not Python — do not edit here)
wheels/                  # cadquery_ocp_novtk wheel (OCC Python bindings)

common/
  enums.py               # SP_obj_type, SP_segment_type, MESHER_NAMES, asset group lists
  utils.py               # Core math/data utilities: knot splitting, shape building
  compound_utils.py      # Compound object → individual patch conversion
  asset_append.py        # Appends GN node groups from assets.blend into the scene
  gui.py                 # All Blender panels, menus, and hotkeys

exporter/
  export_operator.py     # Blender operators: SP_OT_ExportStep, ExportIges, ExportSvg, QuickExport
  export_process_cad.py  # Top-level STEP/IGES export: calls gather_export_shapes → write_step_file
  export_final_shapes.py # Core export logic: walks scene objects, converts each to OCC TopoDS shape
  export_wire.py         # SP_Wire_export: splits wire CPs/knots per segment → list of SP_Edge_export
  export_edge.py         # SP_Edge_export: converts one curve segment to OCC Geom edge
  export_contour.py      # SP_Contour_export: trim contour wires for trimmed surfaces
  export_process_svg.py  # SVG export pipeline
  export_ellipse.py      # gp_Elips helpers

importer/
  import_operator.py     # Blender operator: SP_OT_ImportCAD
  import_reader.py       # STEP/IGES → OCC shapes
  import_shape_to_blender_object.py  # OCC shapes → Blender mesh objects with SP attributes

tools/
  macros.py              # Mesh edit operators (segment type, endpoints, trim contour, etc.)
  add_objects.py         # "Add" menu operators (add patch, curve, compound, etc.)
  toolbar_tools.py       # 3D view toolbar operators
  overlay_endpoints.py   # GPU overlay for curve endpoints
  overlay_segment_selection.py  # GPU overlay for segment highlight
```

---

## STEP Export Pipeline

Understanding this end-to-end is essential for export work:

```
export_operator.py  SP_OT_ExportStep.execute()
  └─ export_process_cad.py  export_step()
       └─ export_final_shapes.py  gather_export_shapes()
            └─ ShapeHierarchy_export  (collects SP objects from scene)
            └─ make_shapes_from_objects()
                 ├─ compound objects → compound_to_topods()
                 │    └─ compound_utils.convert_compound_to_patches()  (GN → temp mesh objects)
                 │    └─ blender_object_to_topods_shapes() per patch
                 ├─ other SP objects → blender_object_to_topods_shapes()
                 │    └─ bezier_face_to_topods / NURBS_face_to_topods / curve_to_topods / etc.
                 └─ sew_shapes() + shells_to_solids()
       └─ write_step_file()  (STEPControl_Writer)
```

**Object type detection**: `sp_type_of_object()` reads the `SP_type` mesh attribute (an integer matching `SP_obj_type` enum). Plain Blender meshes can accidentally carry stale `SP_type` attributes and will be picked up — see `problems.md`.

**Knot data flow** (critical for NURBS curves):
- Blender stores knot values in a flat `Knot` attribute and segment assignments in `knot_segment` (1-based integer per knot)
- `split_by_index()` in `utils.py` groups them by segment index
- The grouped lists are passed as `seg_aligned_attrs["knot"]` and `["mult"]` to `SP_Wire_export`
- `SP_Wire_export` indexes into these per-segment lists when constructing each `SP_Edge_export`
- `knot_tcol_from_att()` strips zero-padding and enforces monotonicity before handing to OCC

**OCC geometry creation**: `SP_Edge_export.bspline()` uses `StepGeom_BSplineCurveWithKnotsAndRationalBSplineCurve` + `StepToGeom.MakeBSplineCurve_s` (not `Geom_BSplineCurve` directly). If `MakeBSplineCurve_s` returns `None`, the curve definition is invalid — check degree, p_count, and knot/mult consistency.

---

## Key Conventions

**SP object attributes** are Blender mesh attributes (not custom properties). They are written by GN modifiers at evaluation time. Reading them requires the *evaluated* object: `obj.evaluated_get(depsgraph)`.

**Modifier loops** must guard against non-GN modifiers (e.g. `MirrorModifier`) before accessing GN-specific attributes:
```python
if not hasattr(m, 'node_group') or m.node_group is None:
    continue
if not hasattr(m, 'node_warnings'):
    continue
```

**Null OCC shapes**: `BRepBuilderAPI_Sewing.SewedShape()` and other OCC builders can return null `TopoDS_Shape`. Always check `shape.IsNull()` before calling any method on the result — a null shape causes an immediate SIGSEGV (no Python traceback).

**git index.lock**: The `.git/index.lock` file sometimes gets stuck. Remove it manually:
```bash
rm /Users/ksloan/github/KS_SurfacePsycho/.git/index.lock
```

---

## Dependencies

- **Blender 5.1+** (Python 3.13, arm64)
- **cadquery_ocp_novtk 7.9.3.1** — OCC Python bindings, bundled as a wheel in `wheels/`. Provides `OCP.*` imports. Only `macos-arm64` wheel is present.
- No pip-installable dependencies beyond what OCC provides. `numpy` and `mathutils` come from Blender.
