# ExportFixes Branch — Change Log

All changes are relative to the `main` branch of the KS_SurfacePsycho fork of SurfacePsycho.

---

## blender_manifest.toml

Restricted the `platforms` and `wheels` list to `macos-arm64` only. The original manifest listed wheels for four platforms (Windows, Linux, and both macOS architectures) but only the arm64 wheel was present in the repository. This caused the extension build to fail immediately with a fatal archive error.

---

## common/utils.py

### split_by_index and split_by_index_dict

Both functions were marked `# KNOWN TO FAIL ON SEVERAL CASES` in the original code. They used a fragile slicing approach that broke when segment indices were 1-based (as the `knot_segment` Blender attribute is) or non-contiguous. Rewrote both to use a dictionary grouping approach that handles any index scheme correctly.

### dict_to_list_missing_index_filled

This function assumed dictionary keys were 0-based, so when `knot_segment` produced 1-based keys (e.g. `{1: [...], 2: [...]}`) it inserted a spurious empty list at index 0, shifting all segments off by one and causing every knot lookup to return an empty array. Fixed to use `min(dict.keys())` as the base index.

### shells_to_solids

Added a null/empty shape guard at the top of the function. `BRepBuilderAPI_Sewing.SewedShape()` can return a null `TopoDS_Shape` when sewing fails. Calling `.ShapeType()` on a null shape caused a hard SIGSEGV crash inside OpenCASCADE (null pointer dereference in C++), which took down all of Blender with no Python traceback. The guard returns an empty list immediately if the shape is null.

### knot_tcol_from_att

Added a monotonic truncation pass after the existing zero-padding strip. A B-spline knot vector must be non-decreasing. In the Pinnace model, the `knot_segment` Blender attribute assigns all knot values for multiple wire segments to the same index, causing two segments' knot arrays to be concatenated into one (e.g. `[0→1, 0→1]`). The moment the knot sequence decreases (1.0 → 0.0) signals the boundary between two segments' data. Truncating at that point gives OpenCASCADE the correct single-segment knot vector.

---

## common/compound_utils.py

The `convert_compound_to_patches` function looped over all modifiers on an object and accessed `m.node_group` without checking whether the modifier was a geometry nodes modifier. `MirrorModifier` and other built-in Blender modifiers do not have a `node_group` attribute, causing an `AttributeError`. Fixed by adding a `hasattr(m, 'node_group')` guard before the attribute access.

---

## exporter/export_edge.py

### bspline()

The original code had `if not None` (always True) where it should have checked `if self.seg_aligned_attrs["isclamped"] is not None`. This meant `isclamped` and `iscyclic` were always read from index `[0]` of whatever was passed rather than the correct per-segment scalar value.

Added diagnostic output to the failure path of `StepToGeom.MakeBSplineCurve_s`. When OpenCASCADE returns `None` (invalid curve definition), the degree, clamped/cyclic flags, control point count, and raw knot/multiplicity arrays are printed to the terminal. This was essential for diagnosing the knot concatenation issue.

---

## exporter/export_final_shapes.py

### node_warnings loop in make_shapes_from_objects

The modifier warning check iterated `m.node_warnings` on all modifiers without first verifying the modifier type. `MirrorModifier` objects do not have a `node_warnings` attribute. Added a `hasattr(m, 'node_warnings')` guard. (Same class of bug as the `compound_utils.py` fix above.)

### compound_to_topods — sewing null guard

After our `shells_to_solids` null guard in `utils.py`, the call site in `compound_to_topods` was updated to check `swd.IsNull()` before passing the sewn shape downstream, with a fallback to the unsewn list of component shapes.

### compound_to_topods — per-patch try/except

Wrapped each `blender_object_to_topods_shapes` call in a try/except so that a single bad patch within a compound does not abort the export of the entire model. Failures are logged to the terminal with the object name and error.

### make_shapes_from_objects — per-object try/except

Added the same try/except wrapper around `blender_object_to_topods_shapes` in the main object loop. This prevents plain mesh objects with stale SP type attributes (see `problems.md`) from crashing the entire export.

### bezier_face_to_topods — CP_count guard

Added an explicit check for the `CP_count` attribute before accessing it. If the attribute is missing, raises a `KeyError` with the object name and a list of attributes that *are* present, making the cause immediately obvious in the log.

---

## exporter/export_process_cad.py

Added `faulthandler.enable()` at the start of `export_step`. Python's `faulthandler` module prints a full Python-level stack trace to stderr even when the interpreter is killed by a signal (SIGSEGV, SIGABRT). This was critical for identifying that the crash was occurring inside `shells_to_solids` → `ShapeType()` on a null OCC shape, which would otherwise produce no Python traceback at all — just a silent Blender crash.

---

## exporter/export_process_svg.py

Fixed a broken import: `from .export_final_shapes import SP_Contour_export`. The `SP_Contour_export` class was moved to `export_contour.py` during an earlier refactor but the import in `export_process_svg.py` was not updated. This caused a silent `ImportError` at extension load time, which prevented the entire SurfacePsycho addon from registering — removing the STEP and IGES options from Blender's export menu entirely.

Corrected to: `from .export_contour import SP_Contour_export`
