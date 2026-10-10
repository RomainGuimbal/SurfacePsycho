# Modes
## Grid Patch
Used to contrain control points to keep the patches symmetric. Typically used for a car hood or roof to maintain continuity when passing through the mirror plane. It acts only on the positions of existing control points and don't add new ones. 

> If you are looking for classic mesh symmetry, use the default mirror modifier

Currently only supported for Bezier surfaces, or NURBS with automatic knots.

## Curve or FlatPatch
### Mirror
Complete symmetry of the wires

### Points
For local symmetry. Symmetrizes only the control points selected by the factor

### Segment
Symmetrizes the selected segment
