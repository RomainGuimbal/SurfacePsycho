from os.path import isfile
from OCP.IFSelect import IFSelect_RetDone
from OCP.IGESControl import IGESControl_Writer
from OCP.Interface import Interface_Static
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs

from .export_shapes_final import gather_export_shapes


def export_step(
    context,
    filepath,
    use_selection,
    scale,
    sew,
    sew_tolerance,
):
    brep_shapes = gather_export_shapes(context, use_selection, scale, sew, sew_tolerance)
    if brep_shapes is not None:
        write_step_file(brep_shapes, filepath, application_protocol="AP203")
        return True
    else:
        return False


def export_iges(
    context,
    filepath,
    use_selection,
    scale,
    sew,
    sew_tolerance,
):
    brep_shapes = gather_export_shapes(context, use_selection, scale, sew, sew_tolerance)
    if brep_shapes is not None:
        write_iges_file(brep_shapes, filepath)
        return True
    else:
        return False


#####################################
# STEP export (copy of OCC Extends) #
#####################################


def write_step_file(a_shape, filename, application_protocol="AP203"):
    """exports a shape to a STEP file
    a_shape: the topods_shape to export (a compound, a solid etc.)
    filename: the filename
    application protocol: "AP203" or "AP214IS" or "AP242DIS"
    """
    # a few checks
    if a_shape.IsNull():
        raise AssertionError(f"Shape {a_shape} is null.")
    if application_protocol not in ["AP203", "AP214IS", "AP242DIS"]:
        raise AssertionError(
            f"application_protocol must be either AP203 or AP214IS. You passed {application_protocol}."
        )
    if isfile(filename):
        raise AssertionError(f"{filename} already exists.")
    
    # creates and initialise the step exporter
    step_writer = STEPControl_Writer()
    Interface_Static.SetCVal_s("write.step.schema", application_protocol)

    # transfer shapes and write file
    step_writer.Transfer(a_shape, STEPControl_AsIs)
    status = step_writer.Write(filename)

    if status != IFSelect_RetDone:
        raise IOError("Error while writing shape to STEP file.")
    if not isfile(filename):
        raise IOError(f"{filename} not saved to filesystem.")


#####################################
# IGES export (copy of OCC Extends) #
#####################################


def write_iges_file(a_shape, filename):
    """exports a shape to a STEP file
    a_shape: the topods_shape to export (a compound, a solid etc.)
    filename: the filename
    application protocol: "AP203" or "AP214"
    """
    # a few checks
    if a_shape.IsNull():
        raise AssertionError("Shape is null.")
    if isfile(filename):
        print(f"Warning: {filename} already exists and will be replaced")
    # creates and initialise the step exporter
    iges_writer = IGESControl_Writer()
    iges_writer.AddShape(a_shape)
    status = iges_writer.Write(filename)

    if status != IFSelect_RetDone:
        raise AssertionError("Not done.")
    if not isfile(filename):
        raise IOError("File not written to disk.")
