## Must know
1. Every SP object can support your own GeometryNodes modifiers, but each object is limited to a single shape except for [Compounds](https://github.com/RomainGuimbal/SurfacePsycho/wiki/2.-SP-Objects#compound). Make a compound to start: `Shift+A`>`Surface`>`Compound`
1. Add a GeometryNodes modifier to it (necessarily on top of the compound meshing modifier), create a new node group and edit the node tree.
1. GeometryNodes compatible with SP must have the following :
   - The **output** must be made only of instances with a shape type attribute (on the instance domain).
   - To add it, use a [`SP - Set Patch Instance Type`](https://github.com/RomainGuimbal/SurfacePsycho/wiki/Set-Patch-Instance-Type-[Node-Group]) node group on your instances and select your desired type.
   - Each shape instance must contain exactly what other SP object meshes contain : Some control geometry with some attributes on it

## Tips
- Look at pre-made shapes in the assets. They are examples for how to make procedural setups.
- Use vertices indices to select and move them
- `SP - Grid coordinates` node gives you the row and column index of points
