from os.path import splitext, split, isfile
from ..common.utils import list_of_shapes_to_compound
import unicodedata

from OCP.TDataStd import TDataStd_Name
from OCP.BRep import BRep_Builder
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCP.IGESControl import IGESControl_Controller, IGESControl_Reader
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB #, Quantity_ColorRGBA
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.STEPControl import STEPControl_Reader
from OCP.TCollection import TCollection_ExtendedString, TCollection_AsciiString
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDocStd import TDocStd_Document
from OCP.TopLoc import TopLoc_Location
from OCP.TopoDS import TopoDS_Compound
from OCP.XCAFDoc import (
    XCAFDoc_DocumentTool,
    XCAFDoc_ColorTool,
    # XCAFDoc_ShapeTool,
    XCAFDoc_ColorCurv,
    XCAFDoc_ColorSurf,
    XCAFDoc_ColorGen,
    XCAFDoc_ColorType,
)

# from OCP.IGESCAFControl import IGESCAFControl_Reader
# from OCP.TopTools import TopTools_IndexedMapOfShape
# from OCP.XCAFApp import XCAFApp_Application

def read_cad(filepath):
    # Create document
    doc = None

    # STEP
    if splitext(split(filepath)[1])[1].lower() in [".step", ".stp"]:
        shape = read_step_file(filepath)
        if shape == None:
            return False

        doc = None

        # # create an handle to a document
        # doc = TDocStd_Document(TCollection_ExtendedString("pythonocc-doc-step-import"))

        # # # Get root assembly
        # # shape_tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
        # # color_tool = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())

        # step_reader = STEPCAFControl_Reader()
        # step_reader.SetColorMode(True)
        # step_reader.SetLayerMode(True)
        # step_reader.SetNameMode(True)
        # step_reader.SetMatMode(True)
        # step_reader.SetGDTMode(True)

        # status = step_reader.ReadFile(filepath)
        # if status == IFSelect_RetDone:
        #     step_reader.Transfer(doc)

        # _toplevel_shapes, doc = read_step_file_with_names_colors(filepath)
        # (topods_shape, label, color)
        # shape = list(_toplevel_shapes.items())[0][0]
        # print(len(list(_toplevel_shapes.items())))

    # IGES
    elif splitext(split(filepath)[1])[1] in [".igs", ".iges", ".IGES", ".IGS"]:
        iges_reader = IGESControl_Reader()
        status = iges_reader.ReadFile(filepath)
        if status != IFSelect_RetDone:
            raise ValueError("Error reading IGES file")
        iges_reader.TransferRoots()
        shape = iges_reader.OneShape()
        # shape = read_iges_file(filepath)

    container_name = splitext(split(filepath)[1])[0]

    return shape, doc, container_name


#######################################
# Step import adapted from Build 123d #
#######################################

# # Issue : it does all the import. It creates objects and all
# def import_step(filepath):

#     def get_name(label: TDF_Label) -> str:
#         """Extract name and format"""
#         name = ""
#         std_name = TDataStd_Name()
#         if label.FindAttribute(TDataStd_Name.GetID_s(), std_name):
#             name = TCollection_AsciiString(std_name.Get()).ToCString()
#         # Remove characters that cause ocp_vscode to fail
#         clean_name = "".join(ch for ch in name if unicodedata.category(ch)[0] != "C")
#         return clean_name.translate(str.maketrans(" .()", "____"))

#     def get_color(shape: TopoDS_Shape) -> Quantity_ColorRGBA:
#         """Get the color - take that of the largest Face if multiple"""

#         def get_col(obj: TopoDS_Shape) -> Quantity_ColorRGBA:
#             col = Quantity_ColorRGBA()
#             if (
#                 color_tool.GetColor(obj, XCAFDoc_ColorCurv, col)
#                 or color_tool.GetColor(obj, XCAFDoc_ColorGen, col)
#                 or color_tool.GetColor(obj, XCAFDoc_ColorSurf, col)
#             ):
#                 return col

#         shape_color = get_col(shape)

#         colors = {}
#         face_explorer = TopExp_Explorer(shape, TopAbs.TopAbs_FACE)
#         while face_explorer.More():
#             current_face = face_explorer.Current()
#             properties = GProp_GProps()
#             BRepGProp.SurfaceProperties_s(current_face, properties)
#             area = properties.Mass()
#             color = get_col(current_face)
#             if color is not None:
#                 colors[area] = color
#             face_explorer.Next()

#         # If there are multiple colors, return the one from the largest face
#         if colors:
#             shape_color = sorted(colors.items())[-1][1]

#         return shape_color

#     def build_assembly(parent_tdf_label: TDF_Label | None = None) -> list[TopoDS_Shape]:
#         """Recursively extract object into an assembly"""
#         sub_tdf_labels = TDF_LabelSequence()
#         if parent_tdf_label is None:
#             shape_tool.GetFreeShapes(sub_tdf_labels)
#         else:
#             shape_tool.GetComponents_s(parent_tdf_label, sub_tdf_labels)

#         sub_shapes: list[TopoDS_Shape] = []
#         for i in range(sub_tdf_labels.Length()):
#             sub_tdf_label = sub_tdf_labels.Value(i + 1)
#             if shape_tool.IsReference_s(sub_tdf_label):
#                 ref_tdf_label = TDF_Label()
#                 shape_tool.GetReferredShape_s(sub_tdf_label, ref_tdf_label)
#             else:
#                 ref_tdf_label = sub_tdf_label

#             downcast_LUT = {
#                 TopAbs.TopAbs_VERTEX: TopoDS.Vertex_s,
#                 TopAbs.TopAbs_EDGE: TopoDS.Edge_s,
#                 TopAbs.TopAbs_WIRE: TopoDS.Wire_s,
#                 TopAbs.TopAbs_FACE: TopoDS.Face_s,
#                 TopAbs.TopAbs_SHELL: TopoDS.Shell_s,
#                 TopAbs.TopAbs_SOLID: TopoDS.Solid_s,
#                 TopAbs.TopAbs_COMPOUND: TopoDS.Compound_s,
#                 TopAbs.TopAbs_COMPSOLID: TopoDS.CompSolid_s,
#             }

#             topods_lut = {
#                 TopoDS_Compound: Compound,
#                 TopoDS_Edge: Edge,
#                 TopoDS_Face: Face,
#                 TopoDS_Shell: Shell,
#                 TopoDS_Solid: Solid,
#                 TopoDS_Vertex: Vertex,
#                 TopoDS_Wire: Wire,
#             }

#             sub_topo_shape = downcast_LUT[shape_tool.GetShape_s(ref_tdf_label)]
#             if shape_tool.IsAssembly_s(ref_tdf_label):
#                 sub_shape = TopoDS_Compound()
#                 sub_shape.children = build_assembly(ref_tdf_label)
#             else:
#                 sub_shape = topods_lut[type(sub_topo_shape)](sub_topo_shape)

#             sub_shape.color = get_color(sub_topo_shape)
#             sub_shape.label = get_name(ref_tdf_label)
#             sub_shape.move(shape_tool.GetLocation_s(sub_tdf_label))

#             sub_shapes.append(sub_shape)
#         return sub_shapes

#     fmt = TCollection_ExtendedString("XCAF")
#     doc = TDocStd_Document(fmt)
#     shape_tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
#     color_tool = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
#     reader = STEPCAFControl_Reader()
#     reader.SetNameMode(True)
#     reader.SetColorMode(True)
#     reader.SetLayerMode(True)
#     reader.ReadFile(filepath)
#     reader.Transfer(doc)

#     root = TopoDS_Compound()
#     root.children = build_assembly()
#     # Remove empty Compound wrapper if single free object
#     if len(root.children) == 1:
#         root = root.children[0]

#     return root, doc


########################################
# Step import adapted from OCC Extends #
########################################


def read_step_file(filename, as_compound=True, verbosity=True):
    """read the STEP file and returns a compound
    filename: the file path
    verbosity: optional, False by default.
    as_compound: True by default. If there are more than one shape at root,
    gather all shapes into one compound. Otherwise returns a list of shapes.
    """
    if not isfile(filename):
        raise FileNotFoundError(f"{filename} not found.")

    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)

    if status != IFSelect_RetDone:
        raise AssertionError("Error: can't read file.")
    if verbosity:
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)
    transfer_result = step_reader.TransferRoots()
    if not transfer_result:
        raise AssertionError("Transfer failed.")
    _nbs = step_reader.NbShapes()
    if _nbs == 0:
        raise AssertionError("No shape to transfer.")
    if _nbs == 1:  # most cases
        return step_reader.Shape(1)
    if _nbs > 1:
        print("Number of shapes:", _nbs)
        shps = []
        # loop over root shapes
        for k in range(1, _nbs + 1):
            new_shp = step_reader.Shape(k)
            if not new_shp.IsNull():
                shps.append(new_shp)
        if as_compound:
            compound, result = list_of_shapes_to_compound(shps)
            if not result:
                print("Warning: all shapes were not added to the compound")
            return compound
        print("Warning, returns a list of shapes.")
        return shps
    return None


def read_step_file_with_names_colors(filename):
    """Returns list of tuples (topods_shape, label, color)
    Use OCAF.
    """
    if not isfile(filename):
        raise FileNotFoundError(f"{filename} not found.")
    # the list:
    output_shapes = {}

    # create an handle to a document
    doc = TDocStd_Document(TCollection_ExtendedString("pythonocc-doc-step-import"))

    # Get root assembly
    shape_tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    color_tool = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    # layer_tool = XCAFDoc_DocumentTool_LayerTool(doc.Main())
    # mat_tool = XCAFDoc_DocumentTool_MaterialTool(doc.Main())

    step_reader = STEPCAFControl_Reader()
    step_reader.SetColorMode(True)
    step_reader.SetLayerMode(True)
    step_reader.SetNameMode(True)
    step_reader.SetMatMode(True)
    step_reader.SetGDTMode(True)

    status = step_reader.ReadFile(filename)
    if status == IFSelect_RetDone:
        step_reader.Transfer(doc)

    locs = []

    def get_name(label: TDF_Label) -> str:
        """Extract name and format"""
        name = ""
        std_name = TDataStd_Name()
        if label.FindAttribute(TDataStd_Name.GetID_s(), std_name):
            name = TCollection_AsciiString(std_name.Get()).ToCString()
        # Remove characters that cause ocp_vscode to fail
        clean_name = "".join(ch for ch in name if unicodedata.category(ch)[0] != "C")
        return clean_name.translate(str.maketrans(" .()", "____"))

    def _get_sub_shapes(lab, loc):
        # global cnt, lvl
        # cnt += 1
        # print("\n[%d] level %d, handling LABEL %s\n" % (cnt, lvl, _get_label_name(lab)))
        # print()
        # print(lab.DumpToString())
        # print()
        # print("Is Assembly    :", shape_tool.IsAssembly(lab))
        # print("Is Free        :", shape_tool.IsFree(lab))
        # print("Is Shape       :", shape_tool.IsShape(lab))
        # print("Is Compound    :", shape_tool.IsCompound(lab))
        # print("Is Component   :", shape_tool.IsComponent(lab))
        # print("Is SimpleShape :", shape_tool.IsSimpleShape(lab))
        # print("Is Reference   :", shape_tool.IsReference(lab))

        # users = TDF_LabelSequence()
        # users_cnt = shape_tool.GetUsers(lab, users)
        # print("Nr Users       :", users_cnt)

        l_subss = TDF_LabelSequence()
        shape_tool.GetSubShapes_s(lab, l_subss)
        # print("Nb subshapes   :", l_subss.Length())
        l_comps = TDF_LabelSequence()
        shape_tool.GetComponents_s(lab, l_comps)
        # print("Nb components  :", l_comps.Length())
        # print()
        name = get_name(lab)
        print("Name :", name)

        if shape_tool.IsAssembly_s(lab):
            l_c = TDF_LabelSequence()
            shape_tool.GetComponents_s(lab, l_c)
            for i in range(l_c.Length()):
                label = l_c.Value(i + 1)
                if shape_tool.IsReference(label):
                    # print("\n########  reference label :", label)
                    label_reference = TDF_Label()
                    shape_tool.GetReferredShape(label, label_reference)
                    loc = shape_tool.GetLocation_s(label)

                    locs.append(loc)
                    # print(">>>>")
                    # lvl += 1
                    _get_sub_shapes(label_reference, loc)
                    # lvl -= 1
                    # print("<<<<")
                    locs.pop()

        elif shape_tool.IsSimpleShape_s(lab):
            # print("\n########  simpleshape label :", lab)
            shape = shape_tool.GetShape_s(lab)
            # print("    all ass locs   :", locs)

            loc = TopLoc_Location()
            for l in locs:
                # print("    take loc       :", l)
                loc = loc.Multiplied(l)

            c = Quantity_Color(0.5, 0.5, 0.5, Quantity_TOC_RGB)  # default color
            color_set = False
            if (
                color_tool.GetInstanceColor(shape, XCAFDoc_ColorGen, c)
                or color_tool.GetInstanceColor(shape, XCAFDoc_ColorSurf, c)
                or color_tool.GetInstanceColor(shape, XCAFDoc_ColorCurv, c)
            ):
                color_tool.SetInstanceColor(shape, 0, c)
                color_tool.SetInstanceColor(shape, 1, c)
                color_tool.SetInstanceColor(shape, 2, c)
                color_set = True
                n = c.Name(c.Red(), c.Green(), c.Blue())
                print(
                    "    instance color Name & RGB: ",
                    c,
                    n,
                    c.Red(),
                    c.Green(),
                    c.Blue(),
                )

            if not color_set:
                if (
                    color_tool.GetColor(shape, XCAFDoc_ColorGen, c)
                    or color_tool.GetColor(shape, XCAFDoc_ColorSurf, c)
                    or color_tool.GetColor(shape, XCAFDoc_ColorCurv, c)
                ):
                    color_tool.SetInstanceColor(shape, 0, c)
                    color_tool.SetInstanceColor(shape, 1, c)
                    color_tool.SetInstanceColor(shape, 2, c)

                    n = c.Name(c.Red(), c.Green(), c.Blue())
                    print(
                        "    shape color Name & RGB: ",
                        c,
                        n,
                        c.Red(),
                        c.Green(),
                        c.Blue(),
                    )

            shape_disp = BRepBuilderAPI_Transform(shape, loc.Transformation()).Shape()
            if shape_disp not in output_shapes:
                output_shapes[shape_disp] = [get_name(lab), c]
            for i in range(l_subss.Length()):
                lab_subs = l_subss.Value(i + 1)
                # print("\n########  simpleshape subshape label :", lab)
                shape_sub = shape_tool.GetShape_s(lab_subs)

                c = Quantity_Color(0.5, 0.5, 0.5, Quantity_TOC_RGB)  # default color
                color_set = False
                if (
                    color_tool.GetInstanceColor(shape_sub, XCAFDoc_ColorGen, c)
                    or color_tool.GetInstanceColor(shape_sub, XCAFDoc_ColorSurf, c)
                    or color_tool.GetInstanceColor(shape_sub, XCAFDoc_ColorCurv, c)
                ):
                    color_tool.SetInstanceColor(shape_sub, 0, c)
                    color_tool.SetInstanceColor(shape_sub, 1, c)
                    color_tool.SetInstanceColor(shape_sub, 2, c)
                    color_set = True
                    n = c.Name(c.Red(), c.Green(), c.Blue())
                    print(
                        "    instance color Name & RGB: ",
                        c,
                        n,
                        c.Red(),
                        c.Green(),
                        c.Blue(),
                    )

                # Set color as parent color ?
                if not color_set:
                    if (
                        XCAFDoc_ColorTool.GetColor(shape, XCAFDoc_ColorType(0), c)
                        or XCAFDoc_ColorTool.GetColor(shape, XCAFDoc_ColorType(1), c)
                        or XCAFDoc_ColorTool.GetColor(shape, XCAFDoc_ColorType(2), c)
                    ):
                        color_tool.SetInstanceColor(shape, 0, c)
                        color_tool.SetInstanceColor(shape, 1, c)
                        color_tool.SetInstanceColor(shape, 2, c)

                        n = c.Name(c.Red(), c.Green(), c.Blue())
                        print(
                            "    shape color Name & RGB: ",
                            c,
                            n,
                            c.Red(),
                            c.Green(),
                            c.Blue(),
                        )
                shape_to_disp = BRepBuilderAPI_Transform(
                    shape_sub, loc.Transformation()
                ).Shape()
                # position the subshape to display
                if shape_to_disp not in output_shapes:
                    output_shapes[shape_to_disp] = [get_name(lab_subs), c]

    def _get_shapes():
        labels = TDF_LabelSequence()
        shape_tool.GetFreeShapes(labels)
        # global cnt
        # cnt += 1

        print()
        print("Number of shapes at root :", labels.Length())
        print()
        for i in range(labels.Length()):
            root_item = labels.Value(i + 1)
            _get_sub_shapes(root_item, None)

    _get_shapes()
    return output_shapes, doc


###########################
# IGES import OCC Extends #
###########################
def read_iges_file(
    filename, return_as_shapes=False, verbosity=False, visible_only=False
):
    """read the IGES file and returns a compound
    filename: the file path
    return_as_shapes: optional, False by default. If True returns a list of shapes,
                      else returns a single compound
    verbosity: optionl, False by default.
    """
    if not isfile(filename):
        raise FileNotFoundError(f"{filename} not found.")

    IGESControl_Controller.Init_s()

    iges_reader = IGESControl_Reader()
    iges_reader.SetReadVisible(visible_only)
    status = iges_reader.ReadFile(filename)

    if status != IFSelect_RetDone:  # check status
        raise IOError("Cannot read IGES file")

    if verbosity:
        failsonly = False
        iges_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        iges_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)
    iges_reader.ClearShapes()
    iges_reader.TransferRoots()
    nbr = iges_reader.NbShapes()

    _shapes = []
    for i in range(1, nbr + 1):
        a_shp = iges_reader.Shape(i)
        if not a_shp.IsNull():
            _shapes.append(a_shp)

    # create a compound and store all shapes
    if not return_as_shapes:
        builder = BRep_Builder()
        compound = TopoDS_Compound()
        builder.MakeCompound(compound)
        for s in _shapes:
            builder.Add(compound, s)
        return [compound]

    return _shapes
