ASSET_NODE_GROUPS_CURVE_AND_FLATPATCH = {
    "SP - Blend Curve",
    "SP - Connect Curve",
    "SP - Continuities between Segments",
    "SP - Convert Circles and Ellipses to Splines",
    "SP - Copy Mesh Face",
    "SP - Copy Internal Curve",
    "SP - Crop or Extend Curve",
    "SP - Crown Curve",
    "SP - Curve Meshing",
    "SP - Plot Distance Between Curves",
    "SP - Fillet Curve or FlatPatch",
    "SP - Fillet Polyline with Circles",
    "SP - Fit Curve",
    "SP - FlatPatch Meshing",
    "SP - Inset FlatPatch",
    "SP - Interpolate Curve or FlatPatch",
    "SP - Interval Curve",
    "SP - Make SVG Ready",
    "SP - Multi Split Curve",
    "SP - NURBS to Bezier Curve or FlatPatch",
    "SP - Oblong Wire",
    "SP - Offset Curve",
    "SP - Plot Curve Torsion",
    "SP - Radial Array FlatPatch",
    "SP - Raise or Lower Curve Degree",
    "SP - Raise or Lower Degree of Selected Segment",
    "SP - Reorder Curve Index",
    "SP - Reorder Curve Selection",
    "SP - Reproject Ellipse Arcs Ends",
    "SP - Resample Selection",
    "SP - Sample Curve Per Degree",
    "SP - Maths Function Segment",
    "SP - Set Edge Length",
    "SP - Split Curve",
    "SP - Switch Curve Direction",
    "SP - Set Segment Type",
    # "SP - Bezier Circlular Arc",
    # "SP - Compose FlatPatch From Sides",
}

ASSET_NODE_GROUPS_BEZIER_PATCH = {
    "SP - Bezier Patch Meshing",
    "SP - Bezier Segment Through Segment",
    "SP - Blend Surfaces",
    "SP - Bump Surface",
    "SP - Connect Bezier Patch",
    "SP - Convert Flat Patch to Bezier Patch",
    "SP - Coon Patch",
    "SP - Crop Patch to Point",
    "SP - Displace Bezier Patch Control Grid",
    "SP - Fillet Trim Contour",
    "SP - Flatten Patch Side",
    "SP - Flatten Patch",
    "SP - Gradient Map",
    "SP - Loft from Internal Curves",
    "SP - Loft",
    "SP - Offset Precisely",
    "SP - Patch Normal to Side",
    "SP - Project Curve on Surface",
    "SP - Raise or Lower Degree Bezier Patch",
    "SP - Reorder Grid Index",
    "SP - Ruled Surface from Mesh Loop",
    "SP - Select Patch Range",
    "SP - Trim Bezier Surface from Projected Wires",
    "SP - UV Curve on Surface",
}

ASSET_NODE_GROUPS_NURBS_PATCH = {
    "SP - NURBS Patch Meshing",
    "SP - NURBS Weighting",
    "SP - Set Knot NURBS Patch",
    "SP - Crop or Extend Patch",
    "SP - Insert Knot NURBS Patch",
    "SP - Curvature Analysis",
    "SP - Continuity Analysis",
    "SP - Fit Patch",
    "SP - Interpolate Patch",
    "SP_Curvature",
    "SP - Convert Contour",
}

ASSET_NODE_GROUPS_OTHER_SURFACES = {
    "SP - Adjust Revolution Sweep Angle",
    "SP - Conical Meshing",
    "SP - Copy Geometry",
    "SP - Cylindrical Meshing",
    "SP - Fill Patch",
    "SP - Isoparametric Curve",
    "SP - Plot Distance from Mesh",
    "SP - Spherical Meshing",
    "SP - Surface of Extrusion Meshing",
    "SP - Surface of Revolution Meshing",
    "SP - Toroidal Meshing",
    "SP - Transform UVMap",
    "SP - Connect Flat Patch",
    "SP - Symmetrize",
    "SP - Square Fill",
}

ASSET_NODE_GROUPS_COMPOUND = {
    "SP - Compound Meshing",
    "SP - Extrude Compound",
    "SP - Intersect Bezier Patches",
    "SP - Interval Curves",
    "SP - NURBS to Bezier Patches",
    "SP - Poly to Compound",
    "SP - Profile Revolution Compound",
    "SP - Set Patch Instance Type",
    "SP - Split to Patches",
    "SP - SubD to Compound",
    "SP - Add Shape to Compound",
    "SP - Copy Compound Nearest Shapes",
    # "SP - Text to Compound", # imported by shape presets
}

ASSET_NODE_GROUPS_SHAPE_PRESETS = {
    "SP - Cylinder Compound",
    "SP - Disc CP",
    "SP - Frame Compound",
    "SP - Oblong Extrusion Compound",
    "SP - Slab Compound",
    "SP - Tubes Compound",
}

ASSET_NODE_GROUPS = (
    ASSET_NODE_GROUPS_CURVE_AND_FLATPATCH
    | ASSET_NODE_GROUPS_BEZIER_PATCH
    | ASSET_NODE_GROUPS_NURBS_PATCH
    | ASSET_NODE_GROUPS_OTHER_SURFACES
    | ASSET_NODE_GROUPS_COMPOUND
    | ASSET_NODE_GROUPS_SHAPE_PRESETS
)
