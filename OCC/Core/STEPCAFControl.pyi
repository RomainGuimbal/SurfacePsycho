from enum import IntEnum
from typing import overload, NewType, Optional, Tuple

from OCC.Core.Standard import *
from OCC.Core.NCollection import *
from OCC.Core.StepBasic import *
from OCC.Core.StepShape import *
from OCC.Core.STEPControl import *
from OCC.Core.TopoDS import *
from OCC.Core.DE import *
from OCC.Core.TColStd import *
from OCC.Core.TCollection import *
from OCC.Core.TDF import *
from OCC.Core.IFSelect import *
from OCC.Core.XSControl import *
from OCC.Core.XCAFDimTolObjects import *
from OCC.Core.StepDimTol import *
from OCC.Core.StepRepr import *
from OCC.Core.StepVisual import *
from OCC.Core.TDocStd import *
from OCC.Core.Message import *
from OCC.Core.XCAFDoc import *
from OCC.Core.STEPConstruct import *


class STEPCAFControl_ActorWrite(STEPControl_ActorWrite):
    def __init__(self) -> None: ...
    def ClearMap(self) -> None: ...
    def IsAssembly(self, S: TopoDS_Shape) -> bool: ...
    def RegisterAssembly(self, S: TopoDS_Shape) -> None: ...
    def SetStdMode(self, stdmode: Optional[bool] = True) -> None: ...

class STEPCAFControl_ConfigurationNode(DE_ConfigurationNode):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, theNode: STEPCAFControl_ConfigurationNode) -> None: ...
    def BuildProvider(self) -> DE_Provider: ...
    def CheckContent(self, theBuffer: NCollection_Buffer) -> bool: ...
    def Copy(self) -> DE_ConfigurationNode: ...
    def GetExtensions(self) -> TColStd_ListOfAsciiString: ...
    def GetFormat(self) -> str: ...
    def GetVendor(self) -> str: ...
    def IsExportSupported(self) -> bool: ...
    def IsImportSupported(self) -> bool: ...
    def Load(self, theResource: DE_ConfigurationContext) -> bool: ...
    def Save(self) -> str: ...

class STEPCAFControl_Controller(STEPControl_Controller):
    def __init__(self) -> None: ...
    @staticmethod
    def Init() -> bool: ...

class STEPCAFControl_ExternFile(Standard_Transient):
    def __init__(self) -> None: ...
    def GetLabel(self) -> TDF_Label: ...
    def GetLoadStatus(self) -> IFSelect_ReturnStatus: ...
    def GetName(self) -> TCollection_HAsciiString: ...
    def GetTransferStatus(self) -> bool: ...
    def GetWS(self) -> XSControl_WorkSession: ...
    def GetWriteStatus(self) -> IFSelect_ReturnStatus: ...
    def SetLabel(self, L: TDF_Label) -> None: ...
    def SetLoadStatus(self, stat: IFSelect_ReturnStatus) -> None: ...
    def SetName(self, name: TCollection_HAsciiString) -> None: ...
    def SetTransferStatus(self, isok: bool) -> None: ...
    def SetWS(self, WS: XSControl_WorkSession) -> None: ...
    def SetWriteStatus(self, stat: IFSelect_ReturnStatus) -> None: ...

class STEPCAFControl_GDTProperty:
    def __init__(self) -> None: ...
    @staticmethod
    def GetDatumRefModifiers(theModifiers: XCAFDimTolObjects_DatumModifiersSequence, theModifWithVal: XCAFDimTolObjects_DatumModifWithValue, theValue: float, theUnit: StepBasic_Unit) -> StepDimTol_HArray1OfDatumReferenceModifier: ...
    @staticmethod
    def GetDatumTargetName(theDatumType: XCAFDimTolObjects_DatumTargetType) -> TCollection_HAsciiString: ...
    @staticmethod
    def GetDatumTargetType(theDescription: TCollection_HAsciiString) -> Tuple[bool, XCAFDimTolObjects_DatumTargetType]: ...
    @staticmethod
    def GetDimClassOfTolerance(theLAF: StepShape_LimitsAndFits) -> Tuple[bool, XCAFDimTolObjects_DimensionFormVariance, XCAFDimTolObjects_DimensionGrade]: ...
    @staticmethod
    def GetDimModifierName(theModifier: XCAFDimTolObjects_DimensionModif) -> TCollection_HAsciiString: ...
    @staticmethod
    def GetDimModifiers(theCRI: StepRepr_CompoundRepresentationItem, theModifiers: XCAFDimTolObjects_DimensionModifiersSequence) -> None: ...
    @staticmethod
    def GetDimQualifierName(theQualifier: XCAFDimTolObjects_DimensionQualifier) -> TCollection_HAsciiString: ...
    @staticmethod
    def GetDimQualifierType(theDescription: TCollection_HAsciiString) -> Tuple[bool, XCAFDimTolObjects_DimensionQualifier]: ...
    @staticmethod
    def GetDimType(theName: TCollection_HAsciiString) -> Tuple[bool, XCAFDimTolObjects_DimensionType]: ...
    @staticmethod
    def GetDimTypeName(theType: XCAFDimTolObjects_DimensionType) -> TCollection_HAsciiString: ...
    @staticmethod
    def GetGeomTolerance(theType: XCAFDimTolObjects_GeomToleranceType) -> StepDimTol_GeometricTolerance: ...
    @staticmethod
    def GetGeomToleranceModifier(theModifier: XCAFDimTolObjects_GeomToleranceModif) -> StepDimTol_GeometricToleranceModifier: ...
    @overload
    @staticmethod
    def GetGeomToleranceType(theType: XCAFDimTolObjects_GeomToleranceType) -> StepDimTol_GeometricToleranceType: ...
    @overload
    @staticmethod
    def GetGeomToleranceType(theType: StepDimTol_GeometricToleranceType) -> XCAFDimTolObjects_GeomToleranceType: ...
    @staticmethod
    def GetLimitsAndFits(theHole: bool, theFormVariance: XCAFDimTolObjects_DimensionFormVariance, theGrade: XCAFDimTolObjects_DimensionGrade) -> StepShape_LimitsAndFits: ...
    @staticmethod
    def GetTessellation(theShape: TopoDS_Shape) -> StepVisual_TessellatedGeometricSet: ...
    @overload
    @staticmethod
    def GetTolValueType(theDescription: TCollection_HAsciiString) -> Tuple[bool, XCAFDimTolObjects_GeomToleranceTypeValue]: ...
    @overload
    @staticmethod
    def GetTolValueType(theType: XCAFDimTolObjects_GeomToleranceTypeValue) -> TCollection_HAsciiString: ...
    @staticmethod
    def IsDimensionalLocation(theType: XCAFDimTolObjects_DimensionType) -> bool: ...
    @staticmethod
    def IsDimensionalSize(theType: XCAFDimTolObjects_DimensionType) -> bool: ...

class STEPCAFControl_Provider(DE_Provider):
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, theNode: DE_ConfigurationNode) -> None: ...
    def GetFormat(self) -> str: ...
    def GetVendor(self) -> str: ...
    @overload
    def Read(self, thePath: str, theDocument: TDocStd_Document, theWS: XSControl_WorkSession, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    @overload
    def Read(self, thePath: str, theDocument: TDocStd_Document, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    @overload
    def Read(self, thePath: str, theShape: TopoDS_Shape, theWS: XSControl_WorkSession, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    @overload
    def Read(self, thePath: str, theShape: TopoDS_Shape, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    @overload
    def Write(self, thePath: str, theDocument: TDocStd_Document, theWS: XSControl_WorkSession, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    @overload
    def Write(self, thePath: str, theDocument: TDocStd_Document, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    @overload
    def Write(self, thePath: str, theShape: TopoDS_Shape, theWS: XSControl_WorkSession, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    @overload
    def Write(self, thePath: str, theShape: TopoDS_Shape, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...

class STEPCAFControl_Reader:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, WS: XSControl_WorkSession, scratch: Optional[bool] = True) -> None: ...
    def ChangeReader(self) -> STEPControl_Reader: ...
    def ExternFile(self, name: str, ef: STEPCAFControl_ExternFile) -> bool: ...
    def ExternFiles(self) -> False: ...
    @staticmethod
    def FindInstance(NAUO: StepRepr_NextAssemblyUsageOccurrence, STool: XCAFDoc_ShapeTool, Tool: STEPConstruct_Tool, ShapeLabelMap: XCAFDoc_DataMapOfShapeLabel) -> TDF_Label: ...
    def GetColorMode(self) -> bool: ...
    def GetGDTMode(self) -> bool: ...
    def GetLayerMode(self) -> bool: ...
    def GetMatMode(self) -> bool: ...
    def GetNameMode(self) -> bool: ...
    def GetPropsMode(self) -> bool: ...
    def GetSHUOMode(self) -> bool: ...
    def GetShapeLabelMap(self) -> XCAFDoc_DataMapOfShapeLabel: ...
    def GetViewMode(self) -> bool: ...
    def Init(self, WS: XSControl_WorkSession, scratch: Optional[bool] = True) -> None: ...
    def NbRootsForTransfer(self) -> int: ...
    @overload
    def Perform(self, filename: str, doc: TDocStd_Document, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    @overload
    def Perform(self, filename: str, doc: TDocStd_Document, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    def ReadFile(self, theFileName: str) -> IFSelect_ReturnStatus: ...
    def Reader(self) -> STEPControl_Reader: ...
    def SetColorMode(self, colormode: bool) -> None: ...
    def SetGDTMode(self, gdtmode: bool) -> None: ...
    def SetLayerMode(self, layermode: bool) -> None: ...
    def SetMatMode(self, matmode: bool) -> None: ...
    def SetNameMode(self, namemode: bool) -> None: ...
    def SetPropsMode(self, propsmode: bool) -> None: ...
    def SetSHUOMode(self, shuomode: bool) -> None: ...
    def SetViewMode(self, viewmode: bool) -> None: ...
    def Transfer(self, doc: TDocStd_Document, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    def TransferOneRoot(self, num: int, doc: TDocStd_Document, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...

class STEPCAFControl_Writer:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, theWS: XSControl_WorkSession, theScratch: Optional[bool] = True) -> None: ...
    def ChangeWriter(self) -> STEPControl_Writer: ...
    @overload
    def ExternFile(self, theLabel: TDF_Label, theExtFile: STEPCAFControl_ExternFile) -> bool: ...
    @overload
    def ExternFile(self, theName: str, theExtFile: STEPCAFControl_ExternFile) -> bool: ...
    def ExternFiles(self) -> False: ...
    def GetColorMode(self) -> bool: ...
    def GetDimTolMode(self) -> bool: ...
    def GetLayerMode(self) -> bool: ...
    def GetMaterialMode(self) -> bool: ...
    def GetNameMode(self) -> bool: ...
    def GetPropsMode(self) -> bool: ...
    def GetSHUOMode(self) -> bool: ...
    def Init(self, theWS: XSControl_WorkSession, theScratch: Optional[bool] = True) -> None: ...
    @overload
    def Perform(self, theDoc: TDocStd_Document, theFileName: str, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    @overload
    def Perform(self, theDoc: TDocStd_Document, theFileName: str, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    def SetColorMode(self, theColorMode: bool) -> None: ...
    def SetDimTolMode(self, theDimTolMode: bool) -> None: ...
    def SetLayerMode(self, theLayerMode: bool) -> None: ...
    def SetMaterialMode(self, theMaterialMode: bool) -> None: ...
    def SetNameMode(self, theNameMode: bool) -> None: ...
    def SetPropsMode(self, thePropsMode: bool) -> None: ...
    def SetSHUOMode(self, theSHUOMode: bool) -> None: ...
    @overload
    def Transfer(self, theDoc: TDocStd_Document, theMode: Optional[STEPControl_StepModelType] = STEPControl_AsIs, theIsMulti: Optional[str] = 0, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    @overload
    def Transfer(self, theLabel: TDF_Label, theMode: Optional[STEPControl_StepModelType] = STEPControl_AsIs, theIsMulti: Optional[str] = 0, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    @overload
    def Transfer(self, theLabelSeq: TDF_LabelSequence, theMode: Optional[STEPControl_StepModelType] = STEPControl_AsIs, theIsMulti: Optional[str] = 0, theProgress: Optional[Message_ProgressRange] = Message_ProgressRange()) -> bool: ...
    def Write(self, theFileName: str) -> IFSelect_ReturnStatus: ...
    def Writer(self) -> STEPControl_Writer: ...

# harray1 classes
# harray2 classes
# hsequence classes
