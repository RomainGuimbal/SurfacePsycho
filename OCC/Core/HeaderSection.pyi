from enum import IntEnum
from typing import overload, NewType, Optional, Tuple

from OCC.Core.Standard import *
from OCC.Core.NCollection import *
from OCC.Core.Interface import *
from OCC.Core.TCollection import *
from OCC.Core.StepData import *


class headersection:
    @staticmethod
    def Protocol() -> HeaderSection_Protocol: ...

class HeaderSection_FileDescription(Standard_Transient):
    def __init__(self) -> None: ...
    def Description(self) -> Interface_HArray1OfHAsciiString: ...
    def DescriptionValue(self, num: int) -> TCollection_HAsciiString: ...
    def ImplementationLevel(self) -> TCollection_HAsciiString: ...
    def Init(self, aDescription: Interface_HArray1OfHAsciiString, aImplementationLevel: TCollection_HAsciiString) -> None: ...
    def NbDescription(self) -> int: ...
    def SetDescription(self, aDescription: Interface_HArray1OfHAsciiString) -> None: ...
    def SetImplementationLevel(self, aImplementationLevel: TCollection_HAsciiString) -> None: ...

class HeaderSection_FileName(Standard_Transient):
    def __init__(self) -> None: ...
    def Author(self) -> Interface_HArray1OfHAsciiString: ...
    def AuthorValue(self, num: int) -> TCollection_HAsciiString: ...
    def Authorisation(self) -> TCollection_HAsciiString: ...
    def Init(self, aName: TCollection_HAsciiString, aTimeStamp: TCollection_HAsciiString, aAuthor: Interface_HArray1OfHAsciiString, aOrganization: Interface_HArray1OfHAsciiString, aPreprocessorVersion: TCollection_HAsciiString, aOriginatingSystem: TCollection_HAsciiString, aAuthorisation: TCollection_HAsciiString) -> None: ...
    def Name(self) -> TCollection_HAsciiString: ...
    def NbAuthor(self) -> int: ...
    def NbOrganization(self) -> int: ...
    def Organization(self) -> Interface_HArray1OfHAsciiString: ...
    def OrganizationValue(self, num: int) -> TCollection_HAsciiString: ...
    def OriginatingSystem(self) -> TCollection_HAsciiString: ...
    def PreprocessorVersion(self) -> TCollection_HAsciiString: ...
    def SetAuthor(self, aAuthor: Interface_HArray1OfHAsciiString) -> None: ...
    def SetAuthorisation(self, aAuthorisation: TCollection_HAsciiString) -> None: ...
    def SetName(self, aName: TCollection_HAsciiString) -> None: ...
    def SetOrganization(self, aOrganization: Interface_HArray1OfHAsciiString) -> None: ...
    def SetOriginatingSystem(self, aOriginatingSystem: TCollection_HAsciiString) -> None: ...
    def SetPreprocessorVersion(self, aPreprocessorVersion: TCollection_HAsciiString) -> None: ...
    def SetTimeStamp(self, aTimeStamp: TCollection_HAsciiString) -> None: ...
    def TimeStamp(self) -> TCollection_HAsciiString: ...

class HeaderSection_FileSchema(Standard_Transient):
    def __init__(self) -> None: ...
    def Init(self, aSchemaIdentifiers: Interface_HArray1OfHAsciiString) -> None: ...
    def NbSchemaIdentifiers(self) -> int: ...
    def SchemaIdentifiers(self) -> Interface_HArray1OfHAsciiString: ...
    def SchemaIdentifiersValue(self, num: int) -> TCollection_HAsciiString: ...
    def SetSchemaIdentifiers(self, aSchemaIdentifiers: Interface_HArray1OfHAsciiString) -> None: ...

class HeaderSection_Protocol(StepData_Protocol):
    def __init__(self) -> None: ...
    def SchemaName(self) -> str: ...
    def TypeNumber(self, atype: Standard_Type) -> int: ...

# harray1 classes
# harray2 classes
# hsequence classes
