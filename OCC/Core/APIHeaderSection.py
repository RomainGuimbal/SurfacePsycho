# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

"""
APIHeaderSection module, see official documentation at
https://www.opencascade.com/doc/occt-7.7.0/refman/html/package_apiheadersection.html
"""

from sys import version_info as _swig_python_version_info
# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _APIHeaderSection
else:
    import _APIHeaderSection

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "this":
            set(self, name, value)
        elif name == "thisown":
            self.this.own(value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _APIHeaderSection.delete_SwigPyIterator

    def value(self):
        return _APIHeaderSection.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _APIHeaderSection.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _APIHeaderSection.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _APIHeaderSection.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _APIHeaderSection.SwigPyIterator_equal(self, x)

    def copy(self):
        return _APIHeaderSection.SwigPyIterator_copy(self)

    def next(self):
        return _APIHeaderSection.SwigPyIterator_next(self)

    def __next__(self):
        return _APIHeaderSection.SwigPyIterator___next__(self)

    def previous(self):
        return _APIHeaderSection.SwigPyIterator_previous(self)

    def advance(self, n):
        return _APIHeaderSection.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _APIHeaderSection.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _APIHeaderSection.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _APIHeaderSection.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _APIHeaderSection.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _APIHeaderSection.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _APIHeaderSection.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self

# Register SwigPyIterator in _APIHeaderSection:
_APIHeaderSection.SwigPyIterator_swigregister(SwigPyIterator)

def _dumps_object(klass):
    """ Overwrite default string output for any wrapped object.
    By default, __repr__ method returns something like:
    <OCC.Core.TopoDS.TopoDS_Shape; proxy of <Swig Object of type 'TopoDS_Shape *' at 0x02BB0758> >
    This is too much verbose.
    We prefer :
    <class 'gp_Pnt'>
    or
    <class 'TopoDS_Shape'>
    """
    klass_name = str(klass.__class__).split(".")[3].split("'")[0]
    repr_string = "<class '" + klass_name + "'"
# for TopoDS_Shape, we also look for the base type
    if klass_name == "TopoDS_Shape":
        if klass.IsNull():
            repr_string += ": Null>"
            return repr_string
        st = klass.ShapeType()
        types = {OCC.Core.TopAbs.TopAbs_VERTEX: "Vertex",
                 OCC.Core.TopAbs.TopAbs_SOLID: "Solid",
                 OCC.Core.TopAbs.TopAbs_EDGE: "Edge",
                 OCC.Core.TopAbs.TopAbs_FACE: "Face",
                 OCC.Core.TopAbs.TopAbs_SHELL: "Shell",
                 OCC.Core.TopAbs.TopAbs_WIRE: "Wire",
                 OCC.Core.TopAbs.TopAbs_COMPOUND: "Compound",
                 OCC.Core.TopAbs.TopAbs_COMPSOLID: "Compsolid"}
        repr_string += "; Type:%s" % types[st]        
    elif hasattr(klass, "IsNull"):
        if klass.IsNull():
            repr_string += "; Null"
    repr_string += ">"
    return repr_string


def process_exception(error, method_name, class_name):
    return _APIHeaderSection.process_exception(error, method_name, class_name)

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.IFSelect
import OCC.Core.Interface
import OCC.Core.TCollection
import OCC.Core.Message
import OCC.Core.OSD
import OCC.Core.TColStd
import OCC.Core.MoniTool
import OCC.Core.TopoDS
import OCC.Core.TopAbs
import OCC.Core.TopLoc
import OCC.Core.gp
import OCC.Core.StepData
import OCC.Core.Resource
import OCC.Core.HeaderSection

from enum import IntEnum
from OCC.Core.Exception import *




def Handle_APIHeaderSection_EditHeader_Create():
    return _APIHeaderSection.Handle_APIHeaderSection_EditHeader_Create()

def Handle_APIHeaderSection_EditHeader_DownCast(t):
    return _APIHeaderSection.Handle_APIHeaderSection_EditHeader_DownCast(t)

def Handle_APIHeaderSection_EditHeader_IsNull(t):
    return _APIHeaderSection.Handle_APIHeaderSection_EditHeader_IsNull(t)
class APIHeaderSection_EditHeader(OCC.Core.IFSelect.IFSelect_Editor):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""
        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        _APIHeaderSection.APIHeaderSection_EditHeader_swiginit(self, _APIHeaderSection.new_APIHeaderSection_EditHeader(*args))


    @staticmethod
    def DownCast(t):
      return Handle_APIHeaderSection_EditHeader_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _APIHeaderSection.delete_APIHeaderSection_EditHeader

# Register APIHeaderSection_EditHeader in _APIHeaderSection:
_APIHeaderSection.APIHeaderSection_EditHeader_swigregister(APIHeaderSection_EditHeader)
class APIHeaderSection_MakeHeader(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, *args):
        r"""

        Parameters
        ----------
        shapetype: int (optional, default to 0)

        Return
        -------
        None

        Description
        -----------
        Prepares a new makeheader from scratch.

        Parameters
        ----------
        model: StepData_StepModel

        Return
        -------
        None

        Description
        -----------
        Prepares a makeheader from the content of a stepmodel see isdone to know if the header is well defined.

        """
        _APIHeaderSection.APIHeaderSection_MakeHeader_swiginit(self, _APIHeaderSection.new_APIHeaderSection_MakeHeader(*args))

    def AddSchemaIdentifier(self, *args):
        r"""

        Parameters
        ----------
        aSchemaIdentifier: TCollection_HAsciiString

        Return
        -------
        None

        Description
        -----------
        Add a subname of schema (if not yet in the list).

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_AddSchemaIdentifier(self, *args)

    def Apply(self, *args):
        r"""

        Parameters
        ----------
        model: StepData_StepModel

        Return
        -------
        None

        Description
        -----------
        Creates an empty header for a new step model and allows the header fields to be completed.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_Apply(self, *args)

    def Author(self, *args):
        r"""
        Return
        -------
        opencascade::handle<Interface_HArray1OfHAsciiString>

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_Author(self, *args)

    def AuthorValue(self, *args):
        r"""

        Parameters
        ----------
        num: int

        Return
        -------
        opencascade::handle<TCollection_HAsciiString>

        Description
        -----------
        Returns the value of the name attribute for the file_name entity.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_AuthorValue(self, *args)

    def Authorisation(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TCollection_HAsciiString>

        Description
        -----------
        Returns the value of the authorization attribute for the file_name entity.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_Authorisation(self, *args)

    def Description(self, *args):
        r"""
        Return
        -------
        opencascade::handle<Interface_HArray1OfHAsciiString>

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_Description(self, *args)

    def DescriptionValue(self, *args):
        r"""

        Parameters
        ----------
        num: int

        Return
        -------
        opencascade::handle<TCollection_HAsciiString>

        Description
        -----------
        Returns the value of the description attribute for the file_description entity.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_DescriptionValue(self, *args)

    def FdValue(self, *args):
        r"""
        Return
        -------
        opencascade::handle<HeaderSection_FileDescription>

        Description
        -----------
        Returns the file_description entity. returns an empty entity if the file_description entity is not initialized.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_FdValue(self, *args)

    def FnValue(self, *args):
        r"""
        Return
        -------
        opencascade::handle<HeaderSection_FileName>

        Description
        -----------
        Returns the file_name entity. returns an empty entity if the file_name entity is not initialized.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_FnValue(self, *args)

    def FsValue(self, *args):
        r"""
        Return
        -------
        opencascade::handle<HeaderSection_FileSchema>

        Description
        -----------
        Returns the file_schema entity. returns an empty entity if the file_schema entity is not initialized.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_FsValue(self, *args)

    def HasFd(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Checks whether there is a file_description entity. returns true if there is one.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_HasFd(self, *args)

    def HasFn(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Checks whether there is a file_name entity. returns true if there is one.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_HasFn(self, *args)

    def HasFs(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Checks whether there is a file_schema entity. returns true if there is one.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_HasFs(self, *args)

    def ImplementationLevel(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TCollection_HAsciiString>

        Description
        -----------
        Returns the value of the implementation_level attribute for the file_description entity.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_ImplementationLevel(self, *args)

    def Init(self, *args):
        r"""

        Parameters
        ----------
        nameval: str

        Return
        -------
        None

        Description
        -----------
        Cancels the former definition and gives a filename to be used when a model has no well defined header.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_Init(self, *args)

    def IsDone(self, *args):
        r"""
        Return
        -------
        bool

        Description
        -----------
        Returns true if all data have been defined (see also hasfn, hasfs, hasfd).

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_IsDone(self, *args)

    def Name(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TCollection_HAsciiString>

        Description
        -----------
        Returns the name attribute for the file_name entity.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_Name(self, *args)

    def NbAuthor(self, *args):
        r"""
        Return
        -------
        int

        Description
        -----------
        Returns the number of values for the author attribute in the file_name entity.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_NbAuthor(self, *args)

    def NbDescription(self, *args):
        r"""
        Return
        -------
        int

        Description
        -----------
        Returns the number of values for the file_description entity in the step file header.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_NbDescription(self, *args)

    def NbOrganization(self, *args):
        r"""
        Return
        -------
        int

        Description
        -----------
        Returns the number of values for the organization attribute in the file_name entity.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_NbOrganization(self, *args)

    def NbSchemaIdentifiers(self, *args):
        r"""
        Return
        -------
        int

        Description
        -----------
        Returns the number of values for the schema_identifier attribute in the file_schema entity.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_NbSchemaIdentifiers(self, *args)

    def NewModel(self, *args):
        r"""

        Parameters
        ----------
        protocol: Interface_Protocol

        Return
        -------
        opencascade::handle<StepData_StepModel>

        Description
        -----------
        Builds a header, creates a new stepmodel, then applies the header to the stepmodel the schema name is taken from the protocol (if it inherits from stepdata, else it is left in blanks).

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_NewModel(self, *args)

    def Organization(self, *args):
        r"""
        Return
        -------
        opencascade::handle<Interface_HArray1OfHAsciiString>

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_Organization(self, *args)

    def OrganizationValue(self, *args):
        r"""

        Parameters
        ----------
        num: int

        Return
        -------
        opencascade::handle<TCollection_HAsciiString>

        Description
        -----------
        Returns the value of attribute organization for the file_name entity.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_OrganizationValue(self, *args)

    def OriginatingSystem(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TCollection_HAsciiString>

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_OriginatingSystem(self, *args)

    def PreprocessorVersion(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TCollection_HAsciiString>

        Description
        -----------
        Returns the name of the preprocessor_version for the file_name entity.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_PreprocessorVersion(self, *args)

    def SchemaIdentifiers(self, *args):
        r"""
        Return
        -------
        opencascade::handle<Interface_HArray1OfHAsciiString>

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SchemaIdentifiers(self, *args)

    def SchemaIdentifiersValue(self, *args):
        r"""

        Parameters
        ----------
        num: int

        Return
        -------
        opencascade::handle<TCollection_HAsciiString>

        Description
        -----------
        Returns the value of the schema_identifier attribute for the file_schema entity.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SchemaIdentifiersValue(self, *args)

    def SetAuthor(self, *args):
        r"""

        Parameters
        ----------
        aAuthor: Interface_HArray1OfHAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetAuthor(self, *args)

    def SetAuthorValue(self, *args):
        r"""

        Parameters
        ----------
        num: int
        aAuthor: TCollection_HAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetAuthorValue(self, *args)

    def SetAuthorisation(self, *args):
        r"""

        Parameters
        ----------
        aAuthorisation: TCollection_HAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetAuthorisation(self, *args)

    def SetDescription(self, *args):
        r"""

        Parameters
        ----------
        aDescription: Interface_HArray1OfHAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetDescription(self, *args)

    def SetDescriptionValue(self, *args):
        r"""

        Parameters
        ----------
        num: int
        aDescription: TCollection_HAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetDescriptionValue(self, *args)

    def SetImplementationLevel(self, *args):
        r"""

        Parameters
        ----------
        aImplementationLevel: TCollection_HAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetImplementationLevel(self, *args)

    def SetName(self, *args):
        r"""

        Parameters
        ----------
        aName: TCollection_HAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetName(self, *args)

    def SetOrganization(self, *args):
        r"""

        Parameters
        ----------
        aOrganization: Interface_HArray1OfHAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetOrganization(self, *args)

    def SetOrganizationValue(self, *args):
        r"""

        Parameters
        ----------
        num: int
        aOrganization: TCollection_HAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetOrganizationValue(self, *args)

    def SetOriginatingSystem(self, *args):
        r"""

        Parameters
        ----------
        aOriginatingSystem: TCollection_HAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetOriginatingSystem(self, *args)

    def SetPreprocessorVersion(self, *args):
        r"""

        Parameters
        ----------
        aPreprocessorVersion: TCollection_HAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetPreprocessorVersion(self, *args)

    def SetSchemaIdentifiers(self, *args):
        r"""

        Parameters
        ----------
        aSchemaIdentifiers: Interface_HArray1OfHAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetSchemaIdentifiers(self, *args)

    def SetSchemaIdentifiersValue(self, *args):
        r"""

        Parameters
        ----------
        num: int
        aSchemaIdentifier: TCollection_HAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetSchemaIdentifiersValue(self, *args)

    def SetTimeStamp(self, *args):
        r"""

        Parameters
        ----------
        aTimeStamp: TCollection_HAsciiString

        Return
        -------
        None

        Description
        -----------
        No available documentation.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_SetTimeStamp(self, *args)

    def TimeStamp(self, *args):
        r"""
        Return
        -------
        opencascade::handle<TCollection_HAsciiString>

        Description
        -----------
        Returns the value of the time_stamp attribute for the file_name entity.

        """
        return _APIHeaderSection.APIHeaderSection_MakeHeader_TimeStamp(self, *args)

    __repr__ = _dumps_object

    __swig_destroy__ = _APIHeaderSection.delete_APIHeaderSection_MakeHeader

# Register APIHeaderSection_MakeHeader in _APIHeaderSection:
_APIHeaderSection.APIHeaderSection_MakeHeader_swigregister(APIHeaderSection_MakeHeader)



