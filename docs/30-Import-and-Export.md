# Import and Export
--- 
## Import
Import any CAD file with `File > Import > SurfacePsycho CAD (.step, .iges)`. The importer is still in progress. Expect variable quality. Also note that the importer doesn't preserve any B-rep connections, it creates the surfaces and curves as individual objects.

--- 
## Export
SurfacePsycho proposes three export formats : **.step**, **.iges** and **.svg**.

### .STEP
`File > Export > SurfacePsycho STEP (.step)`

This will export the selected SP objects. The exporter directly performs sewing

### Quick export
Button in `N panel > SurfacePsycho > Quick export`. Quick exports in the current blend file folder. If the blend file never been saved : it saves at the path specified in ``Edit > Preferences > File Paths > Temporary File``.

### .IGES
`File > Export > SurfacePsycho IGES (.iges)`

The ancestor of step. Here because it costs nothing. Essentially like STEP but with less features.

### .SVG
`File > Export > SurfacePsycho SVG (.svg)` 
Implemented to allow designers to make logo and UI's directly on the product surface.
Since svg only support straight lines and cubic beziers, objects must have the following modifier for conversion [SP - Make SVG Ready](./Modifers/Convert/SP - Make SVG Ready.md) 


> Note : All the other native exporters are also supported but will export standard meshes