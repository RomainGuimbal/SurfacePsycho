# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

"""
StepAP242 module, see official documentation at
https://www.opencascade.com/doc/occt-7.4.0/refman/html/package_stepap242.html
"""


from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_StepAP242')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_StepAP242')
    _StepAP242 = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_StepAP242', [dirname(__file__)])
        except ImportError:
            import _StepAP242
            return _StepAP242
        try:
            _mod = imp.load_module('_StepAP242', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _StepAP242 = swig_import_helper()
    del swig_import_helper
else:
    import _StepAP242
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _StepAP242.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _StepAP242.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _StepAP242.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _StepAP242.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _StepAP242.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _StepAP242.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _StepAP242.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _StepAP242.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _StepAP242.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _StepAP242.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _StepAP242.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _StepAP242.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _StepAP242.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _StepAP242.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _StepAP242.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _StepAP242.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _StepAP242.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _StepAP242.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)


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


def process_exception(error: 'Standard_Failure', method_name: 'std::string', class_name: 'std::string') -> "void":
    return _StepAP242.process_exception(error, method_name, class_name)
process_exception = _StepAP242.process_exception

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.TCollection
import OCC.Core.StepData
import OCC.Core.Interface
import OCC.Core.Message
import OCC.Core.OSD
import OCC.Core.TColStd
import OCC.Core.MoniTool
import OCC.Core.TopoDS
import OCC.Core.TopAbs
import OCC.Core.TopLoc
import OCC.Core.gp
import OCC.Core.Resource
import OCC.Core.StepBasic
import OCC.Core.StepShape
import OCC.Core.StepGeom
import OCC.Core.StepRepr
import OCC.Core.StepDimTol
import OCC.Core.StepAP214
import OCC.Core.StepVisual
import OCC.Core.TColgp

from enum import IntEnum
from OCC.Core.Exception import *




def Handle_StepAP242_IdAttribute_Create() -> "opencascade::handle< StepAP242_IdAttribute >":
    return _StepAP242.Handle_StepAP242_IdAttribute_Create()
Handle_StepAP242_IdAttribute_Create = _StepAP242.Handle_StepAP242_IdAttribute_Create

def Handle_StepAP242_IdAttribute_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< StepAP242_IdAttribute >":
    return _StepAP242.Handle_StepAP242_IdAttribute_DownCast(t)
Handle_StepAP242_IdAttribute_DownCast = _StepAP242.Handle_StepAP242_IdAttribute_DownCast

def Handle_StepAP242_IdAttribute_IsNull(t: 'opencascade::handle< StepAP242_IdAttribute > const &') -> "bool":
    return _StepAP242.Handle_StepAP242_IdAttribute_IsNull(t)
Handle_StepAP242_IdAttribute_IsNull = _StepAP242.Handle_StepAP242_IdAttribute_IsNull

def Handle_StepAP242_ItemIdentifiedRepresentationUsage_Create() -> "opencascade::handle< StepAP242_ItemIdentifiedRepresentationUsage >":
    return _StepAP242.Handle_StepAP242_ItemIdentifiedRepresentationUsage_Create()
Handle_StepAP242_ItemIdentifiedRepresentationUsage_Create = _StepAP242.Handle_StepAP242_ItemIdentifiedRepresentationUsage_Create

def Handle_StepAP242_ItemIdentifiedRepresentationUsage_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< StepAP242_ItemIdentifiedRepresentationUsage >":
    return _StepAP242.Handle_StepAP242_ItemIdentifiedRepresentationUsage_DownCast(t)
Handle_StepAP242_ItemIdentifiedRepresentationUsage_DownCast = _StepAP242.Handle_StepAP242_ItemIdentifiedRepresentationUsage_DownCast

def Handle_StepAP242_ItemIdentifiedRepresentationUsage_IsNull(t: 'opencascade::handle< StepAP242_ItemIdentifiedRepresentationUsage > const &') -> "bool":
    return _StepAP242.Handle_StepAP242_ItemIdentifiedRepresentationUsage_IsNull(t)
Handle_StepAP242_ItemIdentifiedRepresentationUsage_IsNull = _StepAP242.Handle_StepAP242_ItemIdentifiedRepresentationUsage_IsNull

def Handle_StepAP242_DraughtingModelItemAssociation_Create() -> "opencascade::handle< StepAP242_DraughtingModelItemAssociation >":
    return _StepAP242.Handle_StepAP242_DraughtingModelItemAssociation_Create()
Handle_StepAP242_DraughtingModelItemAssociation_Create = _StepAP242.Handle_StepAP242_DraughtingModelItemAssociation_Create

def Handle_StepAP242_DraughtingModelItemAssociation_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< StepAP242_DraughtingModelItemAssociation >":
    return _StepAP242.Handle_StepAP242_DraughtingModelItemAssociation_DownCast(t)
Handle_StepAP242_DraughtingModelItemAssociation_DownCast = _StepAP242.Handle_StepAP242_DraughtingModelItemAssociation_DownCast

def Handle_StepAP242_DraughtingModelItemAssociation_IsNull(t: 'opencascade::handle< StepAP242_DraughtingModelItemAssociation > const &') -> "bool":
    return _StepAP242.Handle_StepAP242_DraughtingModelItemAssociation_IsNull(t)
Handle_StepAP242_DraughtingModelItemAssociation_IsNull = _StepAP242.Handle_StepAP242_DraughtingModelItemAssociation_IsNull

def Handle_StepAP242_GeometricItemSpecificUsage_Create() -> "opencascade::handle< StepAP242_GeometricItemSpecificUsage >":
    return _StepAP242.Handle_StepAP242_GeometricItemSpecificUsage_Create()
Handle_StepAP242_GeometricItemSpecificUsage_Create = _StepAP242.Handle_StepAP242_GeometricItemSpecificUsage_Create

def Handle_StepAP242_GeometricItemSpecificUsage_DownCast(t: 'opencascade::handle< Standard_Transient > const &') -> "opencascade::handle< StepAP242_GeometricItemSpecificUsage >":
    return _StepAP242.Handle_StepAP242_GeometricItemSpecificUsage_DownCast(t)
Handle_StepAP242_GeometricItemSpecificUsage_DownCast = _StepAP242.Handle_StepAP242_GeometricItemSpecificUsage_DownCast

def Handle_StepAP242_GeometricItemSpecificUsage_IsNull(t: 'opencascade::handle< StepAP242_GeometricItemSpecificUsage > const &') -> "bool":
    return _StepAP242.Handle_StepAP242_GeometricItemSpecificUsage_IsNull(t)
Handle_StepAP242_GeometricItemSpecificUsage_IsNull = _StepAP242.Handle_StepAP242_GeometricItemSpecificUsage_IsNull
class StepAP242_IdAttribute(OCC.Core.Standard.Standard_Transient):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Standard.Standard_Transient]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, StepAP242_IdAttribute, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Standard.Standard_Transient]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, StepAP242_IdAttribute, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Returns a idattribute.

        Returns
        -------
        None

        """
        this = _StepAP242.new_StepAP242_IdAttribute(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def AttributeValue(self, *args) -> "opencascade::handle< TCollection_HAsciiString >":
        """
        Returns field attributevalue.

        Returns
        -------
        opencascade::handle<TCollection_HAsciiString>

        """
        return _StepAP242.StepAP242_IdAttribute_AttributeValue(self, *args)


    def IdentifiedItem(self, *args) -> "StepAP242_IdAttributeSelect":
        """
        Returns identifieditem.

        Returns
        -------
        StepAP242_IdAttributeSelect

        """
        return _StepAP242.StepAP242_IdAttribute_IdentifiedItem(self, *args)


    def Init(self, *args) -> "void":
        """
        Init all field own and inherited.

        Parameters
        ----------
        theAttributeValue: TCollection_HAsciiString
        theIdentifiedItem: StepAP242_IdAttributeSelect

        Returns
        -------
        None

        """
        return _StepAP242.StepAP242_IdAttribute_Init(self, *args)


    def SetAttributeValue(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        theAttributeValue: TCollection_HAsciiString

        Returns
        -------
        None

        """
        return _StepAP242.StepAP242_IdAttribute_SetAttributeValue(self, *args)


    def SetIdentifiedItem(self, *args) -> "void":
        """
        Set field identifieditem.

        Parameters
        ----------
        theIdentifiedItem: StepAP242_IdAttributeSelect

        Returns
        -------
        None

        """
        return _StepAP242.StepAP242_IdAttribute_SetIdentifiedItem(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_StepAP242_IdAttribute_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _StepAP242.delete_StepAP242_IdAttribute
    __del__ = lambda self: None
StepAP242_IdAttribute_swigregister = _StepAP242.StepAP242_IdAttribute_swigregister
StepAP242_IdAttribute_swigregister(StepAP242_IdAttribute)

class StepAP242_IdAttributeSelect(OCC.Core.StepData.StepData_SelectType):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.StepData.StepData_SelectType]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, StepAP242_IdAttributeSelect, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.StepData.StepData_SelectType]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, StepAP242_IdAttributeSelect, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Returns a idattributeselect select type.

        Returns
        -------
        None

        """
        this = _StepAP242.new_StepAP242_IdAttributeSelect(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Action(self, *args) -> "opencascade::handle< StepBasic_Action >":
        """
        Returns value as a action (null if another type).

        Returns
        -------
        opencascade::handle<StepBasic_Action>

        """
        return _StepAP242.StepAP242_IdAttributeSelect_Action(self, *args)


    def Address(self, *args) -> "opencascade::handle< StepBasic_Address >":
        """
        Returns value as a address (null if another type).

        Returns
        -------
        opencascade::handle<StepBasic_Address>

        """
        return _StepAP242.StepAP242_IdAttributeSelect_Address(self, *args)


    def ApplicationContext(self, *args) -> "opencascade::handle< StepBasic_ApplicationContext >":
        """
        Returns value as a applicationcontext (null if another type).

        Returns
        -------
        opencascade::handle<StepBasic_ApplicationContext>

        """
        return _StepAP242.StepAP242_IdAttributeSelect_ApplicationContext(self, *args)


    def DimensionalSize(self, *args) -> "opencascade::handle< StepShape_DimensionalSize >":
        """
        Returns value as a dimensionalsize (null if another type).

        Returns
        -------
        opencascade::handle<StepShape_DimensionalSize>

        """
        return _StepAP242.StepAP242_IdAttributeSelect_DimensionalSize(self, *args)


    def GeometricTolerance(self, *args) -> "opencascade::handle< StepDimTol_GeometricTolerance >":
        """
        Returns value as a geometrictolerance (null if another type).

        Returns
        -------
        opencascade::handle<StepDimTol_GeometricTolerance>

        """
        return _StepAP242.StepAP242_IdAttributeSelect_GeometricTolerance(self, *args)


    def Group(self, *args) -> "opencascade::handle< StepBasic_Group >":
        """
        Returns value as a group (null if another type).

        Returns
        -------
        opencascade::handle<StepBasic_Group>

        """
        return _StepAP242.StepAP242_IdAttributeSelect_Group(self, *args)


    def ProductCategory(self, *args) -> "opencascade::handle< StepBasic_ProductCategory >":
        """
        Returns value as a productcategory (null if another type).

        Returns
        -------
        opencascade::handle<StepBasic_ProductCategory>

        """
        return _StepAP242.StepAP242_IdAttributeSelect_ProductCategory(self, *args)


    def PropertyDefinition(self, *args) -> "opencascade::handle< StepRepr_PropertyDefinition >":
        """
        Returns value as a propertydefinition (null if another type).

        Returns
        -------
        opencascade::handle<StepRepr_PropertyDefinition>

        """
        return _StepAP242.StepAP242_IdAttributeSelect_PropertyDefinition(self, *args)


    def Representation(self, *args) -> "opencascade::handle< StepRepr_Representation >":
        """
        Returns value as a representation (null if another type).

        Returns
        -------
        opencascade::handle<StepRepr_Representation>

        """
        return _StepAP242.StepAP242_IdAttributeSelect_Representation(self, *args)


    def ShapeAspect(self, *args) -> "opencascade::handle< StepRepr_ShapeAspect >":
        """
        Returns value as a shapeaspect (null if another type).

        Returns
        -------
        opencascade::handle<StepRepr_ShapeAspect>

        """
        return _StepAP242.StepAP242_IdAttributeSelect_ShapeAspect(self, *args)


    def ShapeAspectRelationship(self, *args) -> "opencascade::handle< StepRepr_ShapeAspectRelationship >":
        """
        Returns value as a shapeaspectrelationship (null if another type).

        Returns
        -------
        opencascade::handle<StepRepr_ShapeAspectRelationship>

        """
        return _StepAP242.StepAP242_IdAttributeSelect_ShapeAspectRelationship(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _StepAP242.delete_StepAP242_IdAttributeSelect
    __del__ = lambda self: None
StepAP242_IdAttributeSelect_swigregister = _StepAP242.StepAP242_IdAttributeSelect_swigregister
StepAP242_IdAttributeSelect_swigregister(StepAP242_IdAttributeSelect)

class StepAP242_ItemIdentifiedRepresentationUsage(OCC.Core.Standard.Standard_Transient):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.Standard.Standard_Transient]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, StepAP242_ItemIdentifiedRepresentationUsage, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.Standard.Standard_Transient]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, StepAP242_ItemIdentifiedRepresentationUsage, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Returns a itemidentifiedrepresentationusage.

        Returns
        -------
        None

        """
        this = _StepAP242.new_StepAP242_ItemIdentifiedRepresentationUsage(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Definition(self, *args) -> "StepAP242_ItemIdentifiedRepresentationUsageDefinition":
        """
        Returns field definition.

        Returns
        -------
        StepAP242_ItemIdentifiedRepresentationUsageDefinition

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_Definition(self, *args)


    def Description(self, *args) -> "opencascade::handle< TCollection_HAsciiString >":
        """
        Returns field description.

        Returns
        -------
        opencascade::handle<TCollection_HAsciiString>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_Description(self, *args)


    def IdentifiedItem(self, *args) -> "opencascade::handle< StepRepr_HArray1OfRepresentationItem >":
        """
        Returns field identifieditem.

        Returns
        -------
        opencascade::handle<StepRepr_HArray1OfRepresentationItem>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_IdentifiedItem(self, *args)


    def IdentifiedItemValue(self, *args) -> "opencascade::handle< StepRepr_RepresentationItem >":
        """
        Returns identified item with given number.

        Parameters
        ----------
        num: int

        Returns
        -------
        opencascade::handle<StepRepr_RepresentationItem>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_IdentifiedItemValue(self, *args)


    def Init(self, *args) -> "void":
        """
        Init all fields own and inherited.

        Parameters
        ----------
        theName: TCollection_HAsciiString
        theDescription: TCollection_HAsciiString
        theDefinition: StepAP242_ItemIdentifiedRepresentationUsageDefinition
        theUsedRepresentation: StepRepr_Representation
        theIdentifiedItem: StepRepr_HArray1OfRepresentationItem

        Returns
        -------
        None

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_Init(self, *args)


    def Name(self, *args) -> "opencascade::handle< TCollection_HAsciiString >":
        """
        Returns field name.

        Returns
        -------
        opencascade::handle<TCollection_HAsciiString>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_Name(self, *args)


    def NbIdentifiedItem(self, *args) -> "Standard_Integer":
        """
        Returns number of identified items.

        Returns
        -------
        int

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_NbIdentifiedItem(self, *args)


    def SetDefinition(self, *args) -> "void":
        """
        Set field definition.

        Parameters
        ----------
        theDefinition: StepAP242_ItemIdentifiedRepresentationUsageDefinition

        Returns
        -------
        None

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_SetDefinition(self, *args)


    def SetDescription(self, *args) -> "void":
        """
        Set field description.

        Parameters
        ----------
        theDescription: TCollection_HAsciiString

        Returns
        -------
        None

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_SetDescription(self, *args)


    def SetIdentifiedItem(self, *args) -> "void":
        """
        Set fiels identifieditem.

        Parameters
        ----------
        theIdentifiedItem: StepRepr_HArray1OfRepresentationItem

        Returns
        -------
        None

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_SetIdentifiedItem(self, *args)


    def SetIdentifiedItemValue(self, *args) -> "void":
        """
        Set identified item with given number.

        Parameters
        ----------
        num: int
        theItem: StepRepr_RepresentationItem

        Returns
        -------
        None

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_SetIdentifiedItemValue(self, *args)


    def SetName(self, *args) -> "void":
        """
        Set field name.

        Parameters
        ----------
        theName: TCollection_HAsciiString

        Returns
        -------
        None

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_SetName(self, *args)


    def SetUsedRepresentation(self, *args) -> "void":
        """
        Set field usedrepresentation.

        Parameters
        ----------
        theUsedRepresentation: StepRepr_Representation

        Returns
        -------
        None

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_SetUsedRepresentation(self, *args)


    def UsedRepresentation(self, *args) -> "opencascade::handle< StepRepr_Representation >":
        """
        Retuns field usedrepresentation.

        Returns
        -------
        opencascade::handle<StepRepr_Representation>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_UsedRepresentation(self, *args)



    @staticmethod
    def DownCast(t):
      return Handle_StepAP242_ItemIdentifiedRepresentationUsage_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _StepAP242.delete_StepAP242_ItemIdentifiedRepresentationUsage
    __del__ = lambda self: None
StepAP242_ItemIdentifiedRepresentationUsage_swigregister = _StepAP242.StepAP242_ItemIdentifiedRepresentationUsage_swigregister
StepAP242_ItemIdentifiedRepresentationUsage_swigregister(StepAP242_ItemIdentifiedRepresentationUsage)

class StepAP242_ItemIdentifiedRepresentationUsageDefinition(OCC.Core.StepData.StepData_SelectType):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.StepData.StepData_SelectType]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, StepAP242_ItemIdentifiedRepresentationUsageDefinition, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.StepData.StepData_SelectType]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, StepAP242_ItemIdentifiedRepresentationUsageDefinition, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Returns a itemidentifiedrepresentationusagedefinition select type.

        Returns
        -------
        None

        """
        this = _StepAP242.new_StepAP242_ItemIdentifiedRepresentationUsageDefinition(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def AppliedApprovalAssignment(self, *args) -> "opencascade::handle< StepAP214_AppliedApprovalAssignment >":
        """
        Returns value as a appliedapprovalassignment (null if another type).

        Returns
        -------
        opencascade::handle<StepAP214_AppliedApprovalAssignment>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_AppliedApprovalAssignment(self, *args)


    def AppliedDateAndTimeAssignment(self, *args) -> "opencascade::handle< StepAP214_AppliedDateAndTimeAssignment >":
        """
        Returns value as a applieddateandtimeassignment (null if another type).

        Returns
        -------
        opencascade::handle<StepAP214_AppliedDateAndTimeAssignment>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_AppliedDateAndTimeAssignment(self, *args)


    def AppliedDateAssignment(self, *args) -> "opencascade::handle< StepAP214_AppliedDateAssignment >":
        """
        Returns value as a applieddateassignment (null if another type).

        Returns
        -------
        opencascade::handle<StepAP214_AppliedDateAssignment>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_AppliedDateAssignment(self, *args)


    def AppliedDocumentReference(self, *args) -> "opencascade::handle< StepAP214_AppliedDocumentReference >":
        """
        Returns value as a applieddocumentreference (null if another type).

        Returns
        -------
        opencascade::handle<StepAP214_AppliedDocumentReference>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_AppliedDocumentReference(self, *args)


    def AppliedExternalIdentificationAssignment(self, *args) -> "opencascade::handle< StepAP214_AppliedExternalIdentificationAssignment >":
        """
        Returns value as a appliedexternalidentificationassignment (null if another type).

        Returns
        -------
        opencascade::handle<StepAP214_AppliedExternalIdentificationAssignment>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_AppliedExternalIdentificationAssignment(self, *args)


    def AppliedGroupAssignment(self, *args) -> "opencascade::handle< StepAP214_AppliedGroupAssignment >":
        """
        Returns value as a appliedgroupassignment (null if another type).

        Returns
        -------
        opencascade::handle<StepAP214_AppliedGroupAssignment>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_AppliedGroupAssignment(self, *args)


    def AppliedOrganizationAssignment(self, *args) -> "opencascade::handle< StepAP214_AppliedOrganizationAssignment >":
        """
        Returns value as a appliedorganizationassignment (null if another type).

        Returns
        -------
        opencascade::handle<StepAP214_AppliedOrganizationAssignment>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_AppliedOrganizationAssignment(self, *args)


    def AppliedPersonAndOrganizationAssignment(self, *args) -> "opencascade::handle< StepAP214_AppliedPersonAndOrganizationAssignment >":
        """
        Returns value as a appliedpersonandorganizationassignment (null if another type).

        Returns
        -------
        opencascade::handle<StepAP214_AppliedPersonAndOrganizationAssignment>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_AppliedPersonAndOrganizationAssignment(self, *args)


    def AppliedSecurityClassificationAssignment(self, *args) -> "opencascade::handle< StepAP214_AppliedSecurityClassificationAssignment >":
        """
        Returns value as a appliedsecurityclassificationassignment (null if another type).

        Returns
        -------
        opencascade::handle<StepAP214_AppliedSecurityClassificationAssignment>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_AppliedSecurityClassificationAssignment(self, *args)


    def DimensionalSize(self, *args) -> "opencascade::handle< StepShape_DimensionalSize >":
        """
        Returns value as a dimensionalsize (null if another type).

        Returns
        -------
        opencascade::handle<StepShape_DimensionalSize>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_DimensionalSize(self, *args)


    def GeneralProperty(self, *args) -> "opencascade::handle< StepBasic_GeneralProperty >":
        """
        Returns value as a generalproperty (null if another type).

        Returns
        -------
        opencascade::handle<StepBasic_GeneralProperty>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_GeneralProperty(self, *args)


    def GeometricTolerance(self, *args) -> "opencascade::handle< StepDimTol_GeometricTolerance >":
        """
        Returns value as a geometrictolerance (null if another type).

        Returns
        -------
        opencascade::handle<StepDimTol_GeometricTolerance>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_GeometricTolerance(self, *args)


    def ProductDefinitionRelationship(self, *args) -> "opencascade::handle< StepBasic_ProductDefinitionRelationship >":
        """
        Returns value as a productdefinitionrelationship (null if another type).

        Returns
        -------
        opencascade::handle<StepBasic_ProductDefinitionRelationship>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_ProductDefinitionRelationship(self, *args)


    def PropertyDefinition(self, *args) -> "opencascade::handle< StepRepr_PropertyDefinition >":
        """
        Returns value as a propertydefinition (null if another type).

        Returns
        -------
        opencascade::handle<StepRepr_PropertyDefinition>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_PropertyDefinition(self, *args)


    def PropertyDefinitionRelationship(self, *args) -> "opencascade::handle< StepRepr_PropertyDefinitionRelationship >":
        """
        Returns value as a propertydefinitionrelationship (null if another type).

        Returns
        -------
        opencascade::handle<StepRepr_PropertyDefinitionRelationship>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_PropertyDefinitionRelationship(self, *args)


    def ShapeAspect(self, *args) -> "opencascade::handle< StepRepr_ShapeAspect >":
        """
        Returns value as a shapeaspect (null if another type).

        Returns
        -------
        opencascade::handle<StepRepr_ShapeAspect>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_ShapeAspect(self, *args)


    def ShapeAspectRelationship(self, *args) -> "opencascade::handle< StepRepr_ShapeAspectRelationship >":
        """
        Returns value as a shapeaspectrelationship (null if another type).

        Returns
        -------
        opencascade::handle<StepRepr_ShapeAspectRelationship>

        """
        return _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_ShapeAspectRelationship(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _StepAP242.delete_StepAP242_ItemIdentifiedRepresentationUsageDefinition
    __del__ = lambda self: None
StepAP242_ItemIdentifiedRepresentationUsageDefinition_swigregister = _StepAP242.StepAP242_ItemIdentifiedRepresentationUsageDefinition_swigregister
StepAP242_ItemIdentifiedRepresentationUsageDefinition_swigregister(StepAP242_ItemIdentifiedRepresentationUsageDefinition)

class StepAP242_DraughtingModelItemAssociation(StepAP242_ItemIdentifiedRepresentationUsage):
    __swig_setmethods__ = {}
    for _s in [StepAP242_ItemIdentifiedRepresentationUsage]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, StepAP242_DraughtingModelItemAssociation, name, value)
    __swig_getmethods__ = {}
    for _s in [StepAP242_ItemIdentifiedRepresentationUsage]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, StepAP242_DraughtingModelItemAssociation, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Returns
        -------
        None

        """
        this = _StepAP242.new_StepAP242_DraughtingModelItemAssociation(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this


    @staticmethod
    def DownCast(t):
      return Handle_StepAP242_DraughtingModelItemAssociation_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _StepAP242.delete_StepAP242_DraughtingModelItemAssociation
    __del__ = lambda self: None
StepAP242_DraughtingModelItemAssociation_swigregister = _StepAP242.StepAP242_DraughtingModelItemAssociation_swigregister
StepAP242_DraughtingModelItemAssociation_swigregister(StepAP242_DraughtingModelItemAssociation)

class StepAP242_GeometricItemSpecificUsage(StepAP242_ItemIdentifiedRepresentationUsage):
    __swig_setmethods__ = {}
    for _s in [StepAP242_ItemIdentifiedRepresentationUsage]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, StepAP242_GeometricItemSpecificUsage, name, value)
    __swig_getmethods__ = {}
    for _s in [StepAP242_ItemIdentifiedRepresentationUsage]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, StepAP242_GeometricItemSpecificUsage, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Returns
        -------
        None

        """
        this = _StepAP242.new_StepAP242_GeometricItemSpecificUsage(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this


    @staticmethod
    def DownCast(t):
      return Handle_StepAP242_GeometricItemSpecificUsage_DownCast(t)


    __repr__ = _dumps_object

    __swig_destroy__ = _StepAP242.delete_StepAP242_GeometricItemSpecificUsage
    __del__ = lambda self: None
StepAP242_GeometricItemSpecificUsage_swigregister = _StepAP242.StepAP242_GeometricItemSpecificUsage_swigregister
StepAP242_GeometricItemSpecificUsage_swigregister(StepAP242_GeometricItemSpecificUsage)



# This file is compatible with both classic and new-style classes.


