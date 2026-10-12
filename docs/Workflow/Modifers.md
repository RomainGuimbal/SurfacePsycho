# Modifiers

## Usage
To non destructively edit SP objects : 
* Drag and drop a modifier from the asset library onto the object to edit or search for it in the modifier list
* Reorder the stack to your liking (top one is applied first)
* Set its parameters

## Meshing Modifiers
Each SP object must have a Meshing modifiers to be evaluated as a STEP shape.
There is one for each object type ([see object types](../Workflow/SP%20Objects.md#types)).
The meshing modifier must be the last one editing the shape. Modifiers before the meshing modifier act on the control geometry. Some modifiers are however made to come after :
   - Mirror
   - Any other viewer/analysis modifier


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