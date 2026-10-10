# Your data is safe
Files using SurfacePsycho objects open **without** the add-on ! They are perfectly standard .blend files. No lost of data or anything. This is by design and stay the case.

# Modifiers updates
SP objects made with older SP versions might not export properly or connect to more recent patches. To update them use `Replace Node Group`

<img src="https://github.com/user-attachments/assets/355c96b0-7f07-4186-b21a-75af1fb085b9" width= 400>

It replaces globaly any node you specify by its name.

> ### Example 
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
