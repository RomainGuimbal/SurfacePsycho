# SP - NURBS to Bezier Patches

NURBS to Bezier splits a multi%20span NURBS patch into multiple single span (Bezier) patches. It's a compound type operation. Therefore it can only work if added to a [compound object](../../Workflow/SP%20Objects.md). To use it you need to choose a NURBS object as an operation target. In order to get individual Bezier patches, use [explode compound](../../Workflow/Explode%20Compound.md) on the compound object.
