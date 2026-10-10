# Usage of SubD to Compound
## Ingredients
- 1 SP Compound object (cf. [Compound object](https://github.com/RomainGuimbal/SurfacePsycho/wiki/2.-SP-Objects#compound))
- 1 SubD to Compound modifier

## Directions
- Add the modifier to the Compound object
- Make sure it is above the _Compound Meshing_ modifier
- Any mesh you create inside the compound object is now subdivided smoothly and converted to Bezier patches
- Adjust the subdivision level
- ~~Serve warm, with a glass of white wine~~

> If you want to edit individual patches, use [explode compound](https://github.com/RomainGuimbal/SurfacePsycho/wiki/Explode-Compound)

> To improve editing speed, you can temporarily uncheck _Compute_ and disable _Compound Meshing_. It is then equivalent to the standard Subdivision Surface modifier.

> Supports creases

> Ignores N-gons and triangles

> Not yet accurate and precisely continuous
