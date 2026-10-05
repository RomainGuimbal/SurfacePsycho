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


def read_cad_simple(filepath):
    # STEP
    file_path = Path(filepath)
    if file_path.suffix.lower() in [".step", ".stp"]:
        root_shape = read_step_file(filepath)

    # IGES
    elif file_path.suffix.lower() in [".igs", ".iges"]:
        iges_reader = IGESControl_Reader()
        status = iges_reader.ReadFile(filepath)
        if status != IFSelect_RetDone:
            raise ValueError("Error reading IGES file")
        iges_reader.TransferRoots()
        root_shape = iges_reader.OneShape()

    if root_shape == None:
        warnings.warn("No shape in file")

    return root_shape


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


def get_label_name(label):
    """Return the name of a TDF_Label as a string, fallback to EntryDumpToString or Tag if needed."""

    # Try to use name label if available
    name_attr = TDataStd_Name()
    if label.FindAttribute(TDataStd_Name.GetID_s(), name_attr):
        return name_attr.Get().ToExtString()

    # Fallback: use EntryDumpToString or Tag
    if hasattr(label, "EntryDumpToString"):
        return label.EntryDumpToString()
    elif hasattr(label, "Tag"):
        return str(label.Tag())
    else:
        return str(label)


def rgb_from_label(self, lab):
    """
    Args:
        lab: shape label
    """
    # default color = pink
    c = Quantity_Color(1.0, 0.0, 1.0, Quantity_TOC_RGB)

    shape = self.shape_tool.GetShape_s(lab)

    # Overwrites each type
    c_surf_exists = self.color_tool.GetColor(shape, XCAFDoc_ColorSurf, c)
    if not c_surf_exists:
        c_curv_exists = self.color_tool.GetColor(shape, XCAFDoc_ColorCurv, c)
        if not c_curv_exists:
            c_gen_exists = self.color_tool.GetColor(shape, XCAFDoc_ColorGen, c)
            if not c_gen_exists:
                return (1.0, 1.0, 1.0)

    return (c.Red(), c.Green(), c.Blue())


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

    def _add_hierarchy_level(self, lab, hierarchy, parent_col) -> None:
        """Edits the hierarchy of _get_sub_hierarchy"""

        ls_components = TDF_LabelSequence()
        self.shape_tool.GetComponents_s(lab, ls_components)

        hierarchy[parent_col] = []
        new_collection = create_collection("Solid", parent_col)

        for i in range(ls_components.Length()):
            l_comp = ls_components.Value(i + 1)
            if self.shape_tool.IsReference_s(l_comp):

                label_reference = TDF_Label()
                self.shape_tool.GetReferredShape(l_comp, label_reference)
                # Overwrite location with parent location
                loc = self.shape_tool.GetLocation_s(l_comp)
                self.locs.append(loc)
                hierarchy[parent_col].append(
                    self._get_sub_hierarchy(label_reference, loc, new_collection)
                )
                self.locs.pop()

    def _get_name_and_color():
        # Overwrites each type
        c_gen_exists = self.color_tool.GetColor(shape, XCAFDoc_ColorGen, color)
        c_surf_exists = self.color_tool.GetColor(shape, XCAFDoc_ColorSurf, color)
        c_curv_exists = False  # self.color_tool.GetColor(shape, XCAFDoc_ColorCurv, color) Supposed to be a fallback but overwrite't

        if c_gen_exists or c_surf_exists or c_curv_exists:
            iscolorset = True
            # Color priority (1/type) is the same as CAD assistant material tree display
            colortype = c_gen_exists * 1 + c_surf_exists * 2 + c_curv_exists * 3

        return name, color, colortype, iscolorset

    def _get_sub_shape(self, lab, parent_col, loc):
        """Recurse until single SP object"""

        hierarchy = {}

        shape = self.shape_tool.GetShape_s(lab)
        match shape.ShapeType():
            # The following order is important (Face > Wire > Edge)
            case TopAbs.TopAbs_FACE:
                face = TopoDS.Face_s(shape)
                hierarchy["Face"] = face
                color = rgb_from_label(lab)
                name = get_label_name(lab)
                self.faces.append((face, name, color, parent_col))

            case TopAbs.TopAbs_WIRE:
                wire = TopoDS.Wire_s(shape)
                hierarchy["Wire"] = wire
                name, color = "temp", 0  # get_shape_name_and_color(wire, self.doc)
                self.edges.append((wire, name, color, parent_col))

            case TopAbs.TopAbs_EDGE:
                edge = TopoDS.Edge_s(shape)
                hierarchy["Edge"] = edge
                name, color = "temp", 0  # get_shape_name_and_color(edge, self.doc)
                self.edges.append((edge, name, color, parent_col))

            # case TopAbs.TopAbs_FACE:  # must be before wire and edge
            #     face = TopoDS.Face_s(shape)
            #     hierarchy["Face"] = face
            #     self.faces.append((face, name, color, parent_col))

            # case TopAbs.TopAbs_WIRE:  # must be before edge
            #     wire = TopoDS.Wire_s(shape)
            #     hierarchy["Wire"] = wire
            #     self.edges.append((wire, name, color, parent_col))

            # case TopAbs.TopAbs_EDGE:
            #     edge = TopoDS.Edge_s(shape)
            #     hierarchy["Edge"] = edge
            #     self.edges.append((edge, name, color, parent_col))

            case _:
                type_name = shape.ShapeType().ShapeTypeToString_s()
                type_name = type_name[0].upper() + type_name[:1].lower()

                hierarchy[parent_col] = []

                lab_seq_subss = TDF_LabelSequence()
                self.shape_tool.GetSubShapes_s(lab, lab_seq_subss)

                new_collection = self.create_collection(type_name, parent_col)
                # iterator = TopoDS_Iterator(shape)
                # while iterator.More():
                #     new_lab =
                #     hierarchy[parent_col].append(
                #         _add_shape_from_label(iterator.Value(), new_collection, new_lab, loc)
                #     )
                #     iterator.Next()

        return hierarchy

    def _get_sub_hierarchy(self, lab, parent_col):
        """
        Recursive
        Args:
           lab (TDF_Label): label of parent shape

        "subss" means sub shape
        """

        # current level hierarchy
        hierarchy = {}

        # Assembly, Recurse until simple shape
        if self.shape_tool.IsAssembly_s(lab):
            self._add_hierarchy_level(lab, hierarchy, parent_col)

        # Simple shape, Recurses too but one level deeper until face/edge/wire level
        elif self.shape_tool.IsSimpleShape_s(lab):
            new_collection = self.create_collection("TODO", parent_col)
            hierarchy[parent_col].append(self._get_sub_shape(new_collection, lab))

        return hierarchy


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
