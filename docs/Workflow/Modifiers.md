# Modifiers
SurfacePsycho comes with a set of GeometryNodes modifiers. Like any Blender modifier, you stack them to chain non-destructive operations.
> For information about specific modifers, go to *Modifiers* section.

## Basic Workflow
To non destructively edit SP objects : 
1. **Add modifiers** to your SP object from the asset browser or from the modifier list
2. **Arrange them** in the order you need (top one is applied first)
3. **Tweak their settings**

## Meshing Modifiers
Meshing modifiers are a specific category of modifiers responsible for evaluating the shapes on your SP objects. Each SP object must have one to be considered an SP object.
There is one for each object type [(see object types)](../Workflow/SP%20Objects.md#types).

The meshing modifier must be the last one to change the shape. Nontheless you can add some modfiers after it for: 
   - **Mirror** : Blender's default mirror modifier
   - **Viewers** : overlays for analysis and display

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