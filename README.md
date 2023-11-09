# SurfacePsycho
Surfacing Blender addon

A new surfacing workflow optimized for industrial deigners ! It notably allows .STEP export, several continuity types and some forms of trimming (much more in progress). By using GeometryNodes on meshes objects, it benefits from many vanilla blender tools such as sculting, and I recommand the following addons to work with :
* [EdgeFlow](https://github.com/BenjaminSauder/EdgeFlow)
* LoopTools (Shipped with Blender)

[BlenderArtists thread](https://blenderartists.org/t/surfacepsycho-addon-project/1487629)

## Features
* Primitives
  * Bicubic bezier patch ("The PsychoPatch" :D)
  * Biquadratic bezier patch

* .STEP export
  * Sewing between patches
  * Mirror modifier

* Editing
  * Trim and extend parallel to the 4 sides (parallel in UV space)
  * Connect side to curve
  * Contiunities C0, G1 and C1 between patches
  * Patch as linear sweep

* Inspect
  * Curvatures Probe (plots all curvatures at a specific surface point)
  * Curvature combs
  
* Conversions to internal NURBS
  

## Current limitations
* No scaling support
* Mirror limited to one axis and one mirror modifier per patch
* No higher degrees patches and curves
* No curved trims
* Biquadratic patches and linear sweeps exports as bicubic patches

## To expect soon
* Conversion __from__ Blender internal NURBS system
* UV maps on patches without trim
* Quadratic bezier curve
* Trim patch and get curve from linear UV space cut (don't worry it will make sense eventually)
* Curve export
* G1 Continuity with N patches
* Bezier <-> Catmull-rom spline conversion
* Way more
