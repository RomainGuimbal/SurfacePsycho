ASSET_NODE_GROUPS_LEVEL_0 = {
    "SP - Disc CP",
    "SP - Set Segment Type",
}

ASSET_NODE_GROUPS_LEVEL_1 = {
    "SP - Set Patch Instance Type",
}

ASSET_NODE_GROUPS_LEVEL_2 = {
    "SP - Reorder Grid Index",
    "SP - Reorder Grid Index [Tool]",
}

ASSET_NODE_GROUPS_CURVE_AND_FLATPATCH = {
    "SP - Blend Curve",
    "SP - Connect Curve",
    "SP - Continuities between Segments",
    "SP - Convert Circles and Ellipses to Splines",
    "SP - Copy Internal Curve",
    "SP - Copy Mesh Face",
    "SP - Crop or Extend Curve",
    "SP - Crown Curve",
    "SP - Curve Meshing",
    "SP - Edge Offset of Flat Patch",
    "SP - Fillet Curve or FlatPatch",
    "SP - Fillet Polyline with Circles",
    "SP - Fit Curve",
    "SP - FlatPatch Meshing",
    "SP - Inset FlatPatch",
    "SP - Interpolate Curve or FlatPatch",
    "SP - Interval Curve",
    "SP - Make Parallel to Flat Patch",
    "SP - Make SVG Ready",
    "SP - Maths Function Segment",
    "SP - Multi Split Curve",
    "SP - NURBS to Bezier Curve or FlatPatch",
    "SP - Oblong Wire",
    "SP - Offset Curve",
    "SP - Plot Curve Torsion",
    "SP - Plot Distance Between Curves",
    "SP - Radial Array FlatPatch",
    "SP - Raise or Lower Curve Degree",
    "SP - Raise or Lower Degree of Selected Segment",
    "SP - Reorder Curve Index",
    "SP - Reorder Curve Selection",
    "SP - Reproject Ellipse Arcs Ends",
    "SP - Resample Selection",
    "SP - Sample Curve Per Degree",
    "SP - Set Edge Length",
    "SP - Split Curve",
    "SP - Switch Curve Direction",
    "SP - Trim Curve with Curve",
}

ASSET_NODE_GROUPS_BEZIER_PATCH = {
    "SP - Bezier Patch Meshing",
    "SP - Bezier Segment Through Segment",
    "SP - Blend Surfaces",
    "SP - Connect Bezier Patch",
    "SP - Convert Flat Patch to Bezier Patch",
    "SP - Coon Patch",
    "SP - Crop Patch to Point",
    "SP - Crown Surface",
    "SP - Displace Bezier Patch Control Grid",
    "SP - Fillet Trim Contour",
    "SP - Flatten Patch",
    "SP - Flatten Patch Side",
    "SP - Gradient Map",
    "SP - Loft",
    "SP - Loft from Internal Curves",
    "SP - Offset Precisely",
    "SP - Project Curve on Surface",
    "SP - Railed Bezier Surface",
    "SP - Raise or Lower Degree Bezier Patch",
    "SP - Reparametrize Bezier Patch",
    "SP - Ruled Surface from Mesh Loop",
    "SP - Select Patch Range",
    "SP - Shrinkwrap Bezier Patch",
    "SP - Side Aligned Reparametrize",
    "SP - Trim Bezier Surface from Projected Wires",
    "SP - Trim Patch with Segment",
    "SP - UV Curve on Surface",
}

ASSET_NODE_GROUPS_NURBS_PATCH = {
    "SP - Continuity Analysis",
    "SP - Convert Contour",
    "SP - Crop or Extend Patch",
    "SP - Curvature Analysis",
    "SP - Fit Patch",
    "SP - Insert Knot NURBS Patch",
    "SP - Interpolate Patch",
    "SP - NURBS Patch Meshing",
    "SP - NURBS Weighting",
    "SP - Set Knot NURBS Patch",
    "SP - Sweep",
}

ASSET_NODE_GROUPS_OTHER_SURFACES = {
    "SP - Adjust Revolution Sweep Angle",
    "SP - Compare Mesh",
    "SP - Conical Meshing",
    "SP - Connect Flat Patch",
    "SP - Copy Geometry",
    "SP - Cylindrical Meshing",
    "SP - Fill Patch",
    "SP - Isoparametric Curve",
    "SP - Patch Normal to Side",
    "SP - Plot Distance from Mesh",
    "SP - Spherical Meshing",
    "SP - Square Fill",
    "SP - Surface of Extrusion Meshing",
    "SP - Surface of Revolution Meshing",
    "SP - Symmetrize",
    "SP - Toroidal Meshing",
    "SP - Transform UVMap",
}

ASSET_NODE_GROUPS_COMPOUND = {
    "SP - Add Shape to Compound",
    "SP - Cable Compound",
    "SP - Compound Meshing",
    "SP - Copy Compound Nearest Edges",
    "SP - Copy Compound Nearest Shapes",
    "SP - Cylinder Compound",
    "SP - Extrude Compound",
    "SP - Flip Compound Face",
    "SP - Frame Compound",
    "SP - Interval Curves",
    "SP - Oblong Extrusion Compound",
    "SP - Patch-Patch Intersection Curves",
    "SP - Pipe Compound",
    "SP - Poly to Compound",
    "SP - Profile Revolution Compound",
    "SP - Slab Compound",
    "SP - Split to Patches",
    "SP - SubD to Compound",
    "SP - Text to Compound",
    "SP - Trim Bezier Patch",
    "SP - Trim Bezier Patches as Compound",
    "SP - Tubes Compound",
}

ASSET_NODE_GROUPS = (
    ASSET_NODE_GROUPS_LEVEL_0
    | ASSET_NODE_GROUPS_LEVEL_1
    | ASSET_NODE_GROUPS_LEVEL_2
    | ASSET_NODE_GROUPS_CURVE_AND_FLATPATCH
    | ASSET_NODE_GROUPS_BEZIER_PATCH
    | ASSET_NODE_GROUPS_NURBS_PATCH
    | ASSET_NODE_GROUPS_OTHER_SURFACES
    | ASSET_NODE_GROUPS_COMPOUND
)
