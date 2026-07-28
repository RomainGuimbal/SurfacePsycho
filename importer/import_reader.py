import unicodedata
from pathlib import Path
import OCP.TopAbs as TopAbs
import OCP.TopAbs as TopAbs
import OCP.TDF as TDF
import OCP.Quantity as Quantity
import warnings

from OCP.TDataStd import TDataStd_Name
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCP.IGESControl import IGESControl_Reader
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.STEPControl import STEPControl_Reader
from OCP.TCollection import TCollection_ExtendedString, TCollection_AsciiString
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDocStd import TDocStd_Document
from OCP.TopLoc import TopLoc_Location
from OCP.XCAFDoc import (
    XCAFDoc_DocumentTool,
    XCAFDoc_ColorTool,
    XCAFDoc_ColorCurv,
    XCAFDoc_ColorSurf,
    XCAFDoc_ColorGen,
)

from ..common.utils import create_collection

def read_cad(filepath, import_colors=True):
    # STEP
    file_path = Path(filepath)
    if file_path.suffix.lower() in [".step", ".stp"]:

        # if import_colors:
        #     all_file_shapes_dic = read_step_file_with_names_colors(filepath)
        # else:
        root_shape = read_step_file(filepath)

    # IGES
    elif file_path.suffix in [".igs", ".iges", ".IGES", ".IGS"]:
        iges_reader = IGESControl_Reader()
        status = iges_reader.ReadFile(filepath)
        if status != IFSelect_RetDone:
            raise ValueError("Error reading IGES file")
        iges_reader.TransferRoots()
        root_shape = iges_reader.OneShape()

    if root_shape == None:
        warnings.warn("No shape in file")

    return root_shape


######################################################
# Step import adapted from python OCC Extends module #
######################################################


def read_step_file(filename, verbosity=True) -> TopAbs.TopAbs_SHAPE:
    """read the STEP file and returns a compound
    filename: the file path
    verbosity: optional, False by default.
    as_compound: True by default. If there are more than one shape at root,
    gather all shapes into one compound. Otherwise returns a list of shapes.
    """
    if not Path(filename).is_file():
        raise FileNotFoundError(f"{filename} not found.")

    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)
    if status != IFSelect_RetDone:
        raise AssertionError("Error: can't read file.")

    if verbosity:
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)

    # Translate step root shapes to occ shapes
    transfer_result = step_reader.TransferRoots()
    if not transfer_result:
        raise AssertionError("Transfer failed.")

    # Transfers as a single compound no matter what
    root_shape = step_reader.OneShape()
    return root_shape


def read_step_file_with_names_colors(
    filename,
) -> dict[TopAbs.TopAbs_SHAPE : tuple[TDF.TDF_Label, Quantity.Quantity_Color]]:
    if not Path(filename).is_file():
        raise FileNotFoundError(f"{filename} not found.")

    output_shapes = {}

    # create an handle to a document
    doc = TDocStd_Document(TCollection_ExtendedString("pythonocc-doc-step-import"))

    # Get root assembly
    shape_tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    color_tool = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
    # layer_tool = XCAFDoc_DocumentTool_LayerTool(doc.Main())
    # mat_tool = XCAFDoc_DocumentTool_MaterialTool(doc.Main())

    reader = STEPCAFControl_Reader()
    reader.SetColorMode(True)
    # reader.SetLayerMode(True)
    reader.SetNameMode(True)
    # reader.SetMatMode(True)
    # reader.SetGDTMode(True)

    status = reader.ReadFile(filename)
    if status == IFSelect_RetDone:
        reader.Transfer(doc)

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

    def _add_shape_from_label(lab, ls_subss):
        """
        Args :
            lab : shape label
            ls_subss : label sequence of shape. For face colors
        """

        # Get unpositionned shape from label
        shape = shape_tool.GetShape_s(lab)

        # Absolute position of shape
        loc = TopLoc_Location()
        for l in locs:
            loc = loc.Multiplied(l)

        # Color
        c = Quantity_Color(0.5, 0.5, 0.5, Quantity_TOC_RGB)  # default color
        color_set = False

        # if color Instance exists for our shape, add it to color_tool
        if (
            color_tool.GetInstanceColor(shape, XCAFDoc_ColorGen, c)
            or color_tool.GetInstanceColor(shape, XCAFDoc_ColorSurf, c)
            or color_tool.GetInstanceColor(shape, XCAFDoc_ColorCurv, c)
        ):
            color_tool.SetInstanceColor(shape, XCAFDoc_ColorGen, c)
            color_tool.SetInstanceColor(shape, XCAFDoc_ColorSurf, c)
            color_tool.SetInstanceColor(shape, XCAFDoc_ColorCurv, c)
            color_set = True

        # if no color Instance, look for standard color
        if not color_set:
            if (
                color_tool.GetColor(shape, XCAFDoc_ColorGen, c)
                or color_tool.GetColor(shape, XCAFDoc_ColorSurf, c)
                or color_tool.GetColor(shape, XCAFDoc_ColorCurv, c)
            ):
                color_tool.SetInstanceColor(shape, XCAFDoc_ColorGen, c)
                color_tool.SetInstanceColor(shape, XCAFDoc_ColorSurf, c)
                color_tool.SetInstanceColor(shape, XCAFDoc_ColorCurv, c)

        # Moving the shape to its location
        shape_disp = BRepBuilderAPI_Transform(shape, loc.Transformation()).Shape()

        # Add shape to output list
        if shape_disp not in output_shapes.keys():
            output_shapes[shape_disp] = [get_name(lab), c]

        # Subshape level (face, wire... ?)
        for i in range(ls_subss.Length()):
            lab_subs = ls_subss.Value(i + 1)
            shape_sub = shape_tool.GetShape_s(lab_subs)

            c = Quantity_Color(0.5, 0.5, 0.5, Quantity_TOC_RGB)  # default color
            color_set = False
            if (
                color_tool.GetInstanceColor(shape_sub, XCAFDoc_ColorGen, c)
                or color_tool.GetInstanceColor(shape_sub, XCAFDoc_ColorSurf, c)
                or color_tool.GetInstanceColor(shape_sub, XCAFDoc_ColorCurv, c)
            ):
                color_tool.SetInstanceColor(shape_sub, XCAFDoc_ColorGen, c)
                color_tool.SetInstanceColor(shape_sub, XCAFDoc_ColorSurf, c)
                color_tool.SetInstanceColor(shape_sub, XCAFDoc_ColorCurv, c)
                color_set = True

            if not color_set:
                if (
                    XCAFDoc_ColorTool.GetColor(shape, XCAFDoc_ColorGen, c)
                    or XCAFDoc_ColorTool.GetColor(shape, XCAFDoc_ColorSurf, c)
                    or XCAFDoc_ColorTool.GetColor(shape, XCAFDoc_ColorCurv, c)
                ):
                    color_tool.SetInstanceColor(shape, XCAFDoc_ColorGen, c)
                    color_tool.SetInstanceColor(shape, XCAFDoc_ColorSurf, c)
                    color_tool.SetInstanceColor(shape, XCAFDoc_ColorCurv, c)

            shape_to_disp = BRepBuilderAPI_Transform(
                shape_sub, loc.Transformation()
            ).Shape()

            # position the subshape to display
            if shape_to_disp not in output_shapes.keys():
                output_shapes[shape_to_disp] = [get_name(lab_subs), c]

    def _get_sub_shapes(lab, loc):
        """
        Recursive
        Args:
           lab (TDF_Label): label of parent shape
        """
        # "l" means TDF_Label
        # "ls" means TDF_LabelSequence
        # "subss" means sub shape
        ls_subss = TDF_LabelSequence()
        shape_tool.GetSubShapes_s(lab, ls_subss)
        ls_comps = TDF_LabelSequence()
        shape_tool.GetComponents_s(lab, ls_comps)

        # parent_name = get_name(lab)
        # print("Name :", parent_name)

        # Several sub shapes -> Recurse
        if shape_tool.IsAssembly_s(lab):
            ls_components = TDF_LabelSequence()
            shape_tool.GetComponents_s(lab, ls_components)
            for i in range(ls_components.Length()):
                l_comp = ls_components.Value(i + 1)
                if shape_tool.IsReference_s(l_comp):
                    label_reference = TDF_Label()
                    shape_tool.GetReferredShape(l_comp, label_reference)
                    # Overrite location with parent location
                    loc = shape_tool.GetLocation_s(l_comp)
                    locs.append(loc)
                    # print(">>>>")
                    # lvl += 1
                    _get_sub_shapes(label_reference, loc)
                    # lvl -= 1
                    # print("<<<<")
                    locs.pop()

        # Single sub shape
        elif shape_tool.IsSimpleShape_s(lab):
            _add_shape_from_label(lab, ls_subss)

    def _get_shapes():
        """Get all shapes from the document"""

        # Get root labels
        labels = TDF_LabelSequence()
        shape_tool.GetFreeShapes(labels)
        print(f"\nNumber of shapes at root :{labels.Length()}\n")

        # Get sub shapes recursively
        for i in range(labels.Length()):
            root_item = labels.Value(i + 1)
            _get_sub_shapes(root_item, None)

    _get_shapes()
    return output_shapes


class ImportHierarchy:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.init_reader()

        # Init main data
        self.faces = []  # tuples (face, name, color, collection)
        self.edges = []  # tuples (edges, collection)
        self.hierarchy = {}

        # Create root collection
        root_name = self.filepath.stem
        root_collection = create_collection(root_name)
        self.hierarchy[root_collection] = []

        # Get root labels
        labels = TDF_LabelSequence()
        self.shape_tool.GetFreeShapes(labels)
        print(f"\nNumber of shapes at root :{labels.Length()}\n")

        # Get sub shapes recursively
        for i in range(labels.Length()):
            root_item = labels.Value(i + 1)
            self.hierarchy[root_collection].append(
                self._get_sub_hierarchy(root_item, root_collection)
            )

    def init_reader(self):
        if not self.filepath.is_file():
            raise FileNotFoundError(f"{self.filepath} not found.")

        # create an handle to a document
        doc = TDocStd_Document(TCollection_ExtendedString("pythonocc-doc-step-import"))

        # Get root assembly
        self.shape_tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
        self.color_tool = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
        # layer_tool = XCAFDoc_DocumentTool_LayerTool(doc.Main())
        # mat_tool = XCAFDoc_DocumentTool_MaterialTool(doc.Main())

        step_reader = STEPCAFControl_Reader()
        step_reader.SetColorMode(True)
        # step_reader.SetLayerMode(True)
        step_reader.SetNameMode(True)
        # step_reader.SetMatMode(True)
        # step_reader.SetGDTMode(True)

        status = step_reader.ReadFile(self.filepath)
        if status == IFSelect_RetDone:
            step_reader.Transfer(doc)

        self.locs = []

        self.reader = step_reader


    def _add_shape_from_label(lab, ls_subss):
        pass
        # match shape.ShapeType():
        #     case TopAbs.TopAbs_COMPOUND:
        #         hierarchy[parent_col] = []
        #         new_collection = create_collection("Compound", parent_col)
        #         iterator = TopoDS_Iterator(shape)
        #         while iterator.More():
        #             hierarchy[parent_col].append(
        #                 self.create_shape_hierarchy(iterator.Value(), new_collection)
        #             )
        #             iterator.Next()

        #     case TopAbs.TopAbs_COMPSOLID:
        #         hierarchy[parent_col] = []
        #         new_collection = create_collection("CompSolid", parent_col)
        #         iterator = TopoDS_Iterator(shape)
        #         while iterator.More():
        #             hierarchy[parent_col].append(
        #                 self.create_shape_hierarchy(iterator.Value(), new_collection)
        #             )
        #             iterator.Next()

        #     case TopAbs.TopAbs_SOLID:
        #         hierarchy[parent_col] = []
        #         new_collection = create_collection("Solid", parent_col)
        #         iterator = TopoDS_Iterator(shape)
        #         while iterator.More():
        #             hierarchy[parent_col].append(
        #                 self.create_shape_hierarchy(iterator.Value(), new_collection)
        #             )
        #             iterator.Next()

        #     case TopAbs.TopAbs_SHELL:
        #         hierarchy[parent_col] = []
        #         new_collection = create_collection("Shell", parent_col)
        #         iterator = TopoDS_Iterator(shape)
        #         while iterator.More():
        #             hierarchy[parent_col].append(
        #                 self.create_shape_hierarchy(iterator.Value(), new_collection)
        #             )
        #             iterator.Next()

    def _get_sub_hierarchy(self, lab, parent_col):
        """
        Recursive
        Args:
           lab (TDF_Label): label of parent shape
        """

        hierarchy = {}
    
        # "l" means TDF_Label
        # "ls" means TDF_LabelSequence
        # "subss" means sub shape
        ls_subss = TDF_LabelSequence()
        self.shape_tool.GetSubShapes_s(lab, ls_subss)
        # ls_comps = TDF_LabelSequence()
        # self.shape_tool.GetComponents_s(lab, ls_comps)

        # Several sub shapes -> Recurse
        if self.shape_tool.IsAssembly_s(lab):
            ls_components = TDF_LabelSequence()
            self.shape_tool.GetComponents_s(lab, ls_components)

            hierarchy[parent_col] = []
            new_collection = create_collection("Solid", parent_col)

            for i in range(ls_components.Length()):
                l_comp = ls_components.Value(i + 1)
                if self.shape_tool.IsReference_s(l_comp):

                    label_reference = TDF_Label()
                    self.shape_tool.GetReferredShape(l_comp, label_reference)
                    # Overrite location with parent location
                    loc = self.shape_tool.GetLocation_s(l_comp)
                    self.locs.append(loc)
                    hierarchy[parent_col].append(self._get_sub_hierarchy(label_reference, loc, new_collection))
                    self.locs.pop()

        # Single sub shape
        elif self.shape_tool.IsSimpleShape_s(lab):
            self._add_shape_from_label(lab, ls_subss)

    

        return hierarchy

#     case TopAbs.TopAbs_FACE:  # must be before wire and edge
#         face = TopoDS.Face_s(shape)
#         hierarchy["Face"] = face
#         self.faces.append((face, name, color, parent_col))

#     case TopAbs.TopAbs_WIRE:  # must be before edge
#         wire = TopoDS.Wire_s(shape)
#         hierarchy["Wire"] = wire
#         self.edges.append((wire, name, color, parent_col))

#     case TopAbs.TopAbs_EDGE:
#         edge = TopoDS.Edge_s(shape)
#         hierarchy["Edge"] = edge
#         self.edges.append((edge, name, color, parent_col))



# ###########################
# # IGES import OCC Extends #
# ###########################
# def read_iges_file(
#     filename, return_as_shapes=False, verbosity=False, visible_only=False
# ):
#     """read the IGES file and returns a compound
#     filename: the file path
#     return_as_shapes: optional, False by default. If True returns a list of shapes,
#                       else returns a single compound
#     verbosity: optionl, False by default.
#     """
#     if not isfile(filename):
#         raise FileNotFoundError(f"{filename} not found.")

#     IGESControl_Controller.Init_s()

#     iges_reader = IGESControl_Reader()
#     iges_reader.SetReadVisible(visible_only)
#     status = iges_reader.ReadFile(filename)

#     if status != IFSelect_RetDone:  # check status
#         raise IOError("Cannot read IGES file")

#     if verbosity:
#         failsonly = False
#         iges_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
#         iges_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)
#     iges_reader.ClearShapes()
#     iges_reader.TransferRoots()
#     nbr = iges_reader.NbShapes()

#     _shapes = []
#     for i in range(1, nbr + 1):
#         a_shp = iges_reader.Shape(i)
#         if not a_shp.IsNull():
#             _shapes.append(a_shp)

#     # create a compound and store all shapes
#     if not return_as_shapes:
#         builder = BRep_Builder()
#         compound = TopoDS_Compound()
#         builder.MakeCompound(compound)
#         for s in _shapes:
#             builder.Add(compound, s)
#         return [compound]

#     return _shapes
