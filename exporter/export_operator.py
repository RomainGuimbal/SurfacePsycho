import bpy
from datetime import datetime
import re
import os
from os.path import join

# from .macros import SP_Props_Group
from .export_process_cad import export_step, export_iges
from .export_process_svg import export_svg
from bpy.props import (
    StringProperty,
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
)
from bpy_extras.io_utils import (
    ExportHelper,
)


class SP_OT_ExportStep(bpy.types.Operator, ExportHelper):
    bl_idname = "wm.sp_step_export"
    bl_label = "Export STEP"
    filename_ext = ".step"
    filter_glob: StringProperty(default="*.step", options={"HIDDEN"}, maxlen=255)
    use_selection: BoolProperty(
        name="Selected Only", description="Selected only", default=True
    )
    scale: FloatProperty(name="Scale", default=1000, min=0)

    sew: BoolProperty(name="Sew Surfaces", description="Sew", default=True)

    sew_tolerance_exponent: IntProperty(
        name="Sewing Tolerance Exponent",
        description="In millimeter, after scale have been applied (-1 = 0.1mm)",
        default=-1,
        soft_min=-10,
        soft_max=0,
    )

    def execute(self, context):
        export_isdone = export_step(
            context,
            self.filepath,
            self.use_selection,
            self.scale,
            self.sew,
            10**self.sew_tolerance_exponent,
        )

        if export_isdone:
            pass
            # self.report({'INFO'}, f"Step file exported as {self.filepath}.step")
        else:
            self.report({"INFO"}, "No SurfacePsycho Objects selected")
        return {"FINISHED"}


class SP_OT_ExportIges(bpy.types.Operator, ExportHelper):
    bl_idname = "wm.sp_iges_export"
    bl_label = "Export IGES"
    filename_ext = ".iges"
    filter_glob: StringProperty(default="*.iges", options={"HIDDEN"}, maxlen=255)
    use_selection: BoolProperty(
        name="Selected Only", description="Selected only", default=True
    )
    scale: FloatProperty(name="Scale", default=1000, min=0)

    sew: BoolProperty(name="Sew Surfaces", description="Sew", default=True)

    sew_tolerance_exponent: IntProperty(
        name="Sewing Tolerance Exponent",
        description="In millimeter, after scale have been applied (-1 = 0.1mm)",
        default=-1,
        soft_min=-10,
        soft_max=0,
    )

    def execute(self, context):
        export_iges(
            context,
            self.filepath,
            self.use_selection,
            self.scale,
            self.sew,
            10**self.sew_tolerance_exponent,
        )
        return {"FINISHED"}


class SP_OT_ExportSvg(bpy.types.Operator, ExportHelper):
    bl_idname = "wm.sp_svg_export"
    bl_label = "Export SVG"

    filename_ext = ".svg"
    filter_glob: StringProperty(default="*.svg", options={"HIDDEN"}, maxlen=255)
    use_selection: BoolProperty(
        name="Selected Only", description="Selected only", default=True
    )
    plane: EnumProperty(
        name="Projection Plane",
        default="XY",
        items=[
            ("XY", "XY", "XY Plane"),
            ("YZ", "YZ", "YZ Plane"),
            ("XZ", "XZ", "XZ Plane"),
        ],
    )
    origin_mode: EnumProperty(
        name="Origin Mode",
        default="auto",
        items=[
            ("auto", "Auto", "Fits exported entities"),
            (
                "world",
                "World",
                "Place entities relative to Scene origin. Thay may be out of canvas",
            ),
        ],
    )
    scale: FloatProperty(
        name="Scale", default=100, min=0, description="In pixel per Blender unit"
    )
    color_mode: EnumProperty(
        name="Color",
        default="material",
        items=[
            (
                "material",
                "From Material",
                "Color svg paths according to material in object first slot",
                "MATERIAL",
                1,
            ),
            (
                "object",
                "From Object",
                "Color svg paths according to object color property",
                "OBJECT_DATAMODE",
                2,
            ),
        ],
    )

    def execute(self, context):
        export_svg(
            context,
            self.filepath,
            self.use_selection,
            self.plane,
            self.origin_mode,
            self.scale,
            self.color_mode,
        )
        return {"FINISHED"}


class SP_OT_QuickExport(bpy.types.Operator):
    bl_idname = "wm.sp_quick_export"
    bl_label = "SP - Quick export"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Exports selection as .STEP at current .blend location."

    def execute(self, context):
        # Get file name
        blendname = bpy.path.display_name_from_filepath(bpy.data.filepath)
        if blendname == "":
            blendname = "SP Export"

        # Get date
        today = datetime.today()
        date_str = today.strftime("%d-%m-%Y")

        # Get temp dir
        blenddir = bpy.path.abspath("//")
        if blenddir != "":
            dir = blenddir
        else:
            dir = context.preferences.filepaths.temporary_directory
            if dir == "":
                self.report(
                    {"WARNING"},
                    "Save your file first or set the temporary directory in preferences",
                )
                return {"CANCELED"}

        # Pattern for files: blendname (number) date_str.step
        pattern = re.compile(
            rf"^{re.escape(blendname)} {re.escape(date_str)} \((\d+)\)\.step$"
        )

        # Find next available number to avoid overrides
        existing_numbers = []
        for fname in os.listdir(dir):
            match = pattern.match(fname)
            if match:
                existing_numbers.append(int(match.group(1)))
        next_number = 1
        if existing_numbers:
            next_number = max(existing_numbers) + 1

        filename = f"{blendname} {date_str} ({next_number}).step"
        pathstr = join(dir, filename)

        export_isdone = export_step(context, pathstr, True, 1000, False, 1e-1)
        if export_isdone:
            self.report({"INFO"}, f"Step file exported at {pathstr}")
        else:
            self.report({"INFO"}, "No SurfacePsycho Objects selected")
        return {"FINISHED"}


classes = [SP_OT_ExportSvg, SP_OT_ExportStep, SP_OT_ExportIges, SP_OT_QuickExport]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes[::-1]:
        bpy.utils.unregister_class(c)
