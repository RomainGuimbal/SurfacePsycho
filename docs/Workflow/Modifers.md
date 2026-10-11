# Modifiers

## Usage
To non destructively edit SP objects : 
* Drag and drop modifiers from the asset library onto the object to edit
* Reorder them to your liking (top one is applied first)
* Set their parameters


## Modifiers order
* The meshing modifier should stay last (bottom) except for the following modifiers which must be after: 
   - Mirror
   - Curvature Analysis
   - Continuity Analysis
   - Plot Distance from Mesh
   - Distance Between Curves
   - Any other viewer/analysis modifier

* Modifiers before the meshing modifier act on the control geometry


## Compatible default Blender modifiers
* Any deform modifier (which do not modify vertex indexing) works in part 1 of the stack (e.g. `Displace` modifier). It simply deforms the control geometry. 
You can also use an _Array modifier_ then a _Weld modifier_ on a _Curve object_

* `Mirror` modifier :
Because symmetry is important in product design, standard `mirror` is supported on all entities. Important to note however : 
  * the mirror modifier(s) needs to be placed last
  * Merge option can cause issues at export 
  * Bisect and UV settings are not supported

* `Array` modifier :
Works for compounds but just the first shape of the compound