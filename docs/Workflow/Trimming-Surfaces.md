# Trimming Surfaces

## Manual Trimming
### Add a Trim Contour
To quickly add a trim contour `N Panel > SurfacePsycho > Edit > Trim Contour > Add` :
![Assign geometry to trim contour from panel](<../Images/assign trim.jpg>)

### Edit it
Trim contours in SurfacePsycho are defined with the [wire system](./Editing-Wires.md). The wires are projected over the X-Y plane of the object (X represents U, Y represents V). The trim contour is simply some geometry marked as such. 

To mark or unmark some, `N Panel > SurfacePsycho > Edit > Trim Contour > Toggle`. 

The ``Select`` button allows you to view what is already assigned.

## Non-Destructive Trimming
Trimming surfaces can be automated by modifiers of the trim category. Note that [SP - Crop or Extend Patch](../Modifers/Trim/SP%20-%20Crop-or-Extend-Patch.md) acts on the control points of the surface and not on its trim contour.