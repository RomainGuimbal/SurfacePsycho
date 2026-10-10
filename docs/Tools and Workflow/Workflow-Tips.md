## Duplicate-Apply
* When some functions you need don't exist, you often want to manually edit the control grid. Since you don't want to lose your modifier stack here is a helpful pattern : 
1. Duplicate the modifier you want to apply (`Shift+D`)
2. Apply one copy (`Shift+A`)
3. Disable the other one
You can now edit the result of modifiers and, if needed, reset to previous state by re-enabling the disabled modifier.

## Generic mesh editing
SP workflow can benefit from many add-ons and built-in tools : 
* [EdgeFlow addon](https://github.com/BenjaminSauder/EdgeFlow)
* LoopTools addon (Shipped with Blender)
* The sculpt mode and proportional editing
* Collection instancing

## Customize your functions
If you know some GeometryNodes, do not hesitate to modify and reuse the node groups to your liking. GeometryNodes makes it relatively easy to understand some of the logic (by disabling and re enabling some groups and look at the result for example). A hint is that the logic very often relies on vertices indices of the control geometries. Also "SP - Grid coordinates" node gives you the row and column of points.
