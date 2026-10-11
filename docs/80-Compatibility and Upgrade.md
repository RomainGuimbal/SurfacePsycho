# Compatibility and Upgrade

## Your data is safe
Files using SurfacePsycho objects open **without** the add-on ! They are perfectly standard .blend files. No lost of data or anything. This is by design and stay the case.

## Upgrade
SP objects made with older SP versions might not export properly or connect to more recent ones.
Once a new version of the add-on is installed, four operators allows you to upgrade objects:
> Warning : upgrade operators are still experimental and not all exposed in the UI.
> To find them perform an operator search (`F3` by default).
> In case of issue, undo and please report the issue.
> Also note modifiers older than 0.9.4 cannot by losslessly upgraded.

### Upgrade per Object
`SP - Update operator` replaces old modifiers by new ones for the selected objects and perform the versionning actions to preserve the shapes.
> This is the safest operator yet.

### Upgrade All Node Groups
`SP - Update All Node Groups` replaces globally all SP groups of the file by newer ones and perform the versionning actions to preserve the shapes.

### Upgrade Node Group
`SP - Update Node Group` replaces globally one SP groups of the file by it's newer version and perform versionning actions associated to preserve the shapes.

### Replace Node Group
`SP - Replace Node Group` gives additional freedom : you can replace any group by any other globaly in the file. Note it will not perform versionning actions.
<img src="https://github.com/user-attachments/assets/355c96b0-7f07-4186-b21a-75af1fb085b9" width= 400>

> #### Example 
>
> I have an old patches with modifier node group "mod", I want to convert it to the new versions.
> - Add a new patch with shift+A
> - Copy its node-group name (⚠️ can be different from the modifier name)
> - let's say it is called "mod.001"
> - copy the name
> - Click `Replace Node Group`
> - Paste the name into both fields and remove the ".001" of target
> - Click ok
>
> If you have more versions "mod" "mod.001" "mod.002"..., the best is to rename the version you want to keep with no suffix and use ".*" suffix on the target to replace all others at once
