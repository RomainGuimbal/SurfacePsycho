from OCP.TopAbs import TopAbs_FACE
from OCP.TDocStd import TDocStd_Document
from OCP.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCP.XCAFApp import XCAFApp_Application
from OCP.XCAFDoc import (
    XCAFDoc_DocumentTool,
    XCAFDoc_ColorSurf,
)
from OCP.UnitsMethods import (
    UnitsMethods_LengthUnit_Milimeter,
)
from OCP.TCollection import TCollection_ExtendedString

SHAPE_TOOL = None
COLOR_TOOL = None

def init_XCAF_doc():
    # Create the XCAF document
    app = XCAFApp_Application.GetApplication_s()
    doc = TDocStd_Document(TCollection_ExtendedString("XmlXCAF"))
    app.NewDocument(TCollection_ExtendedString("MDTV-XCAF"), doc)

    # Scale
    XCAFDoc_DocumentTool.SetLengthUnit_s(doc, 1, UnitsMethods_LengthUnit_Milimeter)

    SHAPE_TOOL.clear()
    COLOR_TOOL.clear()

    SHAPE_TOOL = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    COLOR_TOOL = XCAFDoc_DocumentTool.ColorTool_s(doc.Main())


def set_exported_face_color(topoFace, rgb_color, shape_tool, color_tool):
    # Init XCAF face
    label = shape_tool.AddShape(topoFace, True)

    color = Quantity_Color(rgb_color[0], rgb_color[1], rgb_color[2], Quantity_TOC_RGB)
    color_tool.SetColor(label, color, XCAFDoc_ColorSurf)
