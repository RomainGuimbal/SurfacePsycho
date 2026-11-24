# Test plan :
# - 1. import a step file (it converts to sp),
# - 2. export it (it cannot be lossless so it is different)
# - 3. import it (some features such as multi segment wires are imported differently so it still cannot be compared to the first import)
# - 4. export it
# - 5. import it
# - 6. compare meshes with 3.
# - 7. export it
# - 8. compare the step

import bpy

#######################################################
step_files = [
    "jante.stp",
    "Audi_R8_Wheel.stp",
    "plancher G5.step",
    "Darts_tip_remover_ASM.stp",
    "Taycan.igs",
    "Assy meca standard.stp",
]
tested_file = step_files[0]
#######################################################
# Weird code because waiting for a modal operator to finish is like not natural

for o in bpy.data.objects:
    bpy.data.objects.remove(o)


def run_modal(op_path, args, interval=0.1):
    """op_path: bpy.ops path like 'wm.sp_cad_import'.
    args: dict of operator arguments."""
    module, name = op_path.split(".")
    op_call = getattr(getattr(bpy.ops, module), name)

    # 'wm.sp_cad_import' -> 'WM_OT_sp_cad_import'
    bl_idname = module.upper() + "_OT_" + name

    result = op_call("EXEC_DEFAULT", **args)
    if "RUNNING_MODAL" not in result and "FINISHED" not in result:
        raise RuntimeError(f"{op_path} failed to start: {result}")
    while any(op.bl_idname == bl_idname for op in bpy.context.window.modal_operators):
        yield interval


def workflow():
    # fully linear code, reads like a normal script
    print("Import 1")
    yield from run_modal(
        "wm.sp_cad_import",
        {
            "filepath": "C:\\Users\\romai\\Documents\\Projets\\26 - Bezier Quest\\STEP samples\\"
            + tested_file
        },
    )
    print("Export 1")
    yield from run_modal(
        "wm.sp_step_export",
        {
            "filepath": "C:\\Users\\romai\\Documents\\Projets\\26 - Bezier Quest\\Testing\\"
            + f"{tested_file} cycle1.stp.",
            "use_selection": False,
        },
    )

    # ... normal code between steps, conditions, loops, whatever
    print("all done, right?")


def drive(gen):
    try:
        interval = next(gen)
    except StopIteration:
        return None  # workflow finished, stop the timer
    return interval


bpy.app.timers.register(lambda: drive(workflow()), first_interval=1)
