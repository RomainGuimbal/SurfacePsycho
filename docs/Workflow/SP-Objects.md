# SP Objects

## Add
Add SP objects from the add menu `shift+A > Surface`, `shift+A > Curve` or from the asset library

## What they are 
* Under the hood SurfacePsycho compatible objects are simply Blender objects which stores the right attributes. a
* Most of the time, it is a mesh object with a [Meshing Modifier](https://github.com/RomainGuimbal/SurfacePsycho/wiki/3.-Modifers-and-Tools#meshing-modifiers)
* The meshing modifier provides the attributes required for the exporter to read and for interaction between objects
* New SP objects can be made from scratch by adding a _meshing modifier_ to any mesh

## Types
| Entity |   Icon & color | Entity |   Icon & color | Entity |   Icon & color |
|---|---|---|---|---|---|
| NURBS Patch  | ![NURBS Patch Icon](https://github.com/RomainGuimbal/SurfacePsycho/assets/39882829/a9c76de6-a101-4602-83dd-448d9dd33f84)  | Flat Patch  | ![Flat Patch Icon](https://github.com/RomainGuimbal/SurfacePsycho/assets/39882829/a9921279-1aaf-49c6-9929-6a28a3beee5e)  | Bezier Patch | ![Bezier Patch Icon](https://github.com/RomainGuimbal/SurfacePsycho/assets/39882829/df4d0035-86cf-4cf3-bb7f-1f71f272c6e4)  |
| Curve | ![Curve Icon](https://github.com/RomainGuimbal/SurfacePsycho/assets/39882829/4cbfc44b-4549-4b42-be13-9b7c9bb7d6d8) | Compound | ![Compound Icon](https://github.com/user-attachments/assets/b08f5587-98c9-47c9-a4a3-58221e801c02) | Others | ICON TO ADD |

## Curve
A curve object contains a single _wire_. Requires a [Curve Meshing modifier](https://github.com/RomainGuimbal/SurfacePsycho/wiki/Curve-Meshing-[Modifier]). Default Blender curves cannot be exported with SP directly, but they can be converted with [SP - Copy Internal Curve](https://github.com/RomainGuimbal/SurfacePsycho/wiki/Copy-Internal-Curve-[Modifier]).

## FlatPatch
Planar surfaces built from a set of _wires_. Theses wires are flatten to either the object XY plane or to mean plane if *Orient* option is enabled. Requires a [FlatPatch Meshing modifier](https://github.com/RomainGuimbal/SurfacePsycho/wiki/FlatPatch-Meshing-[Modifier])

## NURBS Patch
Your typical Non-Uniform-Rational-B-Spline. Requires a [NURBS Patch Meshing modifier](https://github.com/RomainGuimbal/SurfacePsycho/wiki/NURBS-Patch-Meshing-[Modifier])

## Bezier Patch
Single span NURBS patch. The 2 reason for the separation is that they are faster and simpler to work with. As a consequence a lot of algorithm are implemented on them at first, and ported to NURBS later. Requires a [Bezier Patch Meshing modifier](https://github.com/RomainGuimbal/SurfacePsycho/wiki/SP---Bezier-Patch-Meshing)

## Compound
An object containing several SP shapes. Can be used for [procedural modeling](https://github.com/RomainGuimbal/SurfacePsycho/wiki/Procedural-modeling-with-SP). Requires a [Compound Meshing modifier](https://github.com/RomainGuimbal/SurfacePsycho/wiki/Compound-Meshing-[Modifier])

## Wire
A single chain of vertices (open or closed) used to represent a chain of segments. To edit them see [Editing-Wires](./Editing-Wires.md)

## Segments
Represent patch edges, or any curve piece with a single geometrical definition. A modifier which has a segment target can take it from any patch or curve.
