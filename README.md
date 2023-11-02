# SurfacePsycho
Surfacing Blender addon

The addon offers a new surfacing workflow optimized for industrial deigners. It notably allows .STEP export, several continuity types and some forms of trimming (much more in progress). By using GeometryNodes on meshes objects, it benefits from many vanilla blender tools such as sculting, and I recommand the following addons to work with :
* [EdgeFlow](https://github.com/BenjaminSauder/EdgeFlow)
* LoopTools (Shipped with Blender)

[BlenderArtists thread](https://blenderartists.org/t/surfacepsycho-addon-project/1487629)

## Features
* Primitives
  * Bicubic bezier patch ("The PsychoPatch" :D)
  * Cubic bezier curve
  * Biquadratic bezier patch

* .STEP export
  * Sewing between patches
  * Mirror modifier

* Editing
  * Trim and extend parallel to sides (in UV space)
  * Connect side to curve
  * Contiunities C0, G1 and C1 between patches
  * Connect to untrimmed surface
  * Make patch linear sweep (with rail curves)

* Inspect
  * Curvature clover (plots principal curvatures at a specific surface point)
  * Curvature combs

## Current limitations
* Continuities doesn't support scaling
* Mirror on several axis or several mirror modifiers
* Continuities between N patches
* Higher degrees patches and curves
* Curved trims
* Curvature combs only support internal cubic bezier curves
* Biquadratic patches and linear sweeps exports as bicubic patches

## To expect soon
* Conversion with Blender internal NURBS system
* UVs for blender materials
* Quadratic bezier curve
* Curve from linear UV space cut (don't worry it will make sense eventually)
