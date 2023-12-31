# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

"""
IGESCAFControl module, see official documentation at
https://www.opencascade.com/doc/occt-7.4.0/refman/html/package_igescafcontrol.html
"""


from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_IGESCAFControl')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_IGESCAFControl')
    _IGESCAFControl = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_IGESCAFControl', [dirname(__file__)])
        except ImportError:
            import _IGESCAFControl
            return _IGESCAFControl
        try:
            _mod = imp.load_module('_IGESCAFControl', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _IGESCAFControl = swig_import_helper()
    del swig_import_helper
else:
    import _IGESCAFControl
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
    __swig_destroy__ = _IGESCAFControl.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _IGESCAFControl.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _IGESCAFControl.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _IGESCAFControl.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _IGESCAFControl.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _IGESCAFControl.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _IGESCAFControl.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _IGESCAFControl.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _IGESCAFControl.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _IGESCAFControl.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _IGESCAFControl.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _IGESCAFControl.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _IGESCAFControl.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _IGESCAFControl.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _IGESCAFControl.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _IGESCAFControl.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _IGESCAFControl.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _IGESCAFControl.SwigPyIterator_swigregister
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
    return _IGESCAFControl.process_exception(error, method_name, class_name)
process_exception = _IGESCAFControl.process_exception

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection
import OCC.Core.Quantity
import OCC.Core.TCollection
import OCC.Core.IGESControl
import OCC.Core.Transfer
import OCC.Core.Message
import OCC.Core.OSD
import OCC.Core.TColStd
import OCC.Core.Interface
import OCC.Core.MoniTool
import OCC.Core.TopoDS
import OCC.Core.TopAbs
import OCC.Core.TopLoc
import OCC.Core.gp
import OCC.Core.IGESToBRep
import OCC.Core.IGESData
import OCC.Core.Geom
import OCC.Core.GeomAbs
import OCC.Core.TColgp
import OCC.Core.ShapeExtend
import OCC.Core.TColGeom
import OCC.Core.TopTools
import OCC.Core.Geom2d
import OCC.Core.XSControl
import OCC.Core.IFSelect
import OCC.Core.TDocStd
import OCC.Core.TDF
import OCC.Core.CDF
import OCC.Core.CDM
import OCC.Core.Resource
import OCC.Core.PCDM
import OCC.Core.Storage

from enum import IntEnum
from OCC.Core.Exception import *



class igescafcontrol(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, igescafcontrol, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, igescafcontrol, name)
    __repr__ = _swig_repr

    def DecodeColor(*args) -> "Quantity_Color":
        """
        Provides a tool for writing iges file converts iges color index to cascade color.

        Parameters
        ----------
        col: int

        Returns
        -------
        Quantity_Color

        """
        return _IGESCAFControl.igescafcontrol_DecodeColor(*args)

    DecodeColor = staticmethod(DecodeColor)

    def EncodeColor(*args) -> "Standard_Integer":
        """
        Tries to convert cascade color to iges color index if no corresponding color defined in iges, returns 0.

        Parameters
        ----------
        col: Quantity_Color

        Returns
        -------
        int

        """
        return _IGESCAFControl.igescafcontrol_EncodeColor(*args)

    EncodeColor = staticmethod(EncodeColor)

    __repr__ = _dumps_object


    def __init__(self):
        this = _IGESCAFControl.new_igescafcontrol()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _IGESCAFControl.delete_igescafcontrol
    __del__ = lambda self: None
igescafcontrol_swigregister = _IGESCAFControl.igescafcontrol_swigregister
igescafcontrol_swigregister(igescafcontrol)

def igescafcontrol_DecodeColor(*args) -> "Quantity_Color":
    """
    Provides a tool for writing iges file converts iges color index to cascade color.

    Parameters
    ----------
    col: int

    Returns
    -------
    Quantity_Color

    """
    return _IGESCAFControl.igescafcontrol_DecodeColor(*args)

def igescafcontrol_EncodeColor(*args) -> "Standard_Integer":
    """
    Tries to convert cascade color to iges color index if no corresponding color defined in iges, returns 0.

    Parameters
    ----------
    col: Quantity_Color

    Returns
    -------
    int

    """
    return _IGESCAFControl.igescafcontrol_EncodeColor(*args)

class IGESCAFControl_Reader(OCC.Core.IGESControl.IGESControl_Reader):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.IGESControl.IGESControl_Reader]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, IGESCAFControl_Reader, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.IGESControl.IGESControl_Reader]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, IGESCAFControl_Reader, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Creates a reader with an empty iges model and sets colormode, layermode and namemode to standard_true.

        Returns
        -------
        None

        Creates a reader tool and attaches it to an already existing session clears the session if it was not yet set for iges.

        Parameters
        ----------
        theWS: XSControl_WorkSession
        FromScratch: bool,optional
        	default value is Standard_True

        Returns
        -------
        None

        """
        this = _IGESCAFControl.new_IGESCAFControl_Reader(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def GetColorMode(self, *args) -> "Standard_Boolean":
        """
        No available documentation.

        Returns
        -------
        bool

        """
        return _IGESCAFControl.IGESCAFControl_Reader_GetColorMode(self, *args)


    def GetLayerMode(self, *args) -> "Standard_Boolean":
        """
        No available documentation.

        Returns
        -------
        bool

        """
        return _IGESCAFControl.IGESCAFControl_Reader_GetLayerMode(self, *args)


    def GetNameMode(self, *args) -> "Standard_Boolean":
        """
        No available documentation.

        Returns
        -------
        bool

        """
        return _IGESCAFControl.IGESCAFControl_Reader_GetNameMode(self, *args)


    def Perform(self, *args) -> "Standard_Boolean":
        """
        No available documentation.

        Parameters
        ----------
        theFileName: TCollection_AsciiString
        theDoc: TDocStd_Document
        theProgress: Message_ProgressRange,optional
        	default value is Message_ProgressRange()

        Returns
        -------
        bool

        Translate iges file given by filename into the document return true if succeeded, and false in case of fail.

        Parameters
        ----------
        theFileName: char *
        theDoc: TDocStd_Document
        theProgress: Message_ProgressRange,optional
        	default value is Message_ProgressRange()

        Returns
        -------
        bool

        """
        return _IGESCAFControl.IGESCAFControl_Reader_Perform(self, *args)


    def SetColorMode(self, *args) -> "void":
        """
        Set colormode for indicate read colors or not.

        Parameters
        ----------
        theMode: bool

        Returns
        -------
        None

        """
        return _IGESCAFControl.IGESCAFControl_Reader_SetColorMode(self, *args)


    def SetLayerMode(self, *args) -> "void":
        """
        Set layermode for indicate read layers or not.

        Parameters
        ----------
        theMode: bool

        Returns
        -------
        None

        """
        return _IGESCAFControl.IGESCAFControl_Reader_SetLayerMode(self, *args)


    def SetNameMode(self, *args) -> "void":
        """
        Set namemode for indicate read name or not.

        Parameters
        ----------
        theMode: bool

        Returns
        -------
        None

        """
        return _IGESCAFControl.IGESCAFControl_Reader_SetNameMode(self, *args)


    def Transfer(self, *args) -> "Standard_Boolean":
        """
        Translates currently loaded iges file into the document returns true if succeeded, and false in case of fail.

        Parameters
        ----------
        theDoc: TDocStd_Document
        theProgress: Message_ProgressRange,optional
        	default value is Message_ProgressRange()

        Returns
        -------
        bool

        """
        return _IGESCAFControl.IGESCAFControl_Reader_Transfer(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _IGESCAFControl.delete_IGESCAFControl_Reader
    __del__ = lambda self: None
IGESCAFControl_Reader_swigregister = _IGESCAFControl.IGESCAFControl_Reader_swigregister
IGESCAFControl_Reader_swigregister(IGESCAFControl_Reader)

class IGESCAFControl_Writer(OCC.Core.IGESControl.IGESControl_Writer):
    __swig_setmethods__ = {}
    for _s in [OCC.Core.IGESControl.IGESControl_Writer]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, IGESCAFControl_Writer, name, value)
    __swig_getmethods__ = {}
    for _s in [OCC.Core.IGESControl.IGESControl_Writer]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))
    __getattr__ = lambda self, name: _swig_getattr(self, IGESCAFControl_Writer, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Creates a writer with an empty iges model and sets colormode, layermode and namemode to standard_true.

        Returns
        -------
        None

        Creates a reader tool and attaches it to an already existing session clears the session if it was not yet set for iges.

        Parameters
        ----------
        WS: XSControl_WorkSession
        scratch: bool,optional
        	default value is Standard_True

        Returns
        -------
        None

        """
        this = _IGESCAFControl.new_IGESCAFControl_Writer(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def GetColorMode(self, *args) -> "Standard_Boolean":
        """
        No available documentation.

        Returns
        -------
        bool

        """
        return _IGESCAFControl.IGESCAFControl_Writer_GetColorMode(self, *args)


    def GetLayerMode(self, *args) -> "Standard_Boolean":
        """
        No available documentation.

        Returns
        -------
        bool

        """
        return _IGESCAFControl.IGESCAFControl_Writer_GetLayerMode(self, *args)


    def GetNameMode(self, *args) -> "Standard_Boolean":
        """
        No available documentation.

        Returns
        -------
        bool

        """
        return _IGESCAFControl.IGESCAFControl_Writer_GetNameMode(self, *args)


    def Perform(self, *args) -> "Standard_Boolean":
        """
        No available documentation.

        Parameters
        ----------
        doc: TDocStd_Document
        filename: TCollection_AsciiString
        theProgress: Message_ProgressRange,optional
        	default value is Message_ProgressRange()

        Returns
        -------
        bool

        Transfers a document and writes it to a iges file returns true if translation is ok.

        Parameters
        ----------
        doc: TDocStd_Document
        filename: char *
        theProgress: Message_ProgressRange,optional
        	default value is Message_ProgressRange()

        Returns
        -------
        bool

        """
        return _IGESCAFControl.IGESCAFControl_Writer_Perform(self, *args)


    def SetColorMode(self, *args) -> "void":
        """
        Set colormode for indicate write colors or not.

        Parameters
        ----------
        colormode: bool

        Returns
        -------
        None

        """
        return _IGESCAFControl.IGESCAFControl_Writer_SetColorMode(self, *args)


    def SetLayerMode(self, *args) -> "void":
        """
        Set layermode for indicate write layers or not.

        Parameters
        ----------
        layermode: bool

        Returns
        -------
        None

        """
        return _IGESCAFControl.IGESCAFControl_Writer_SetLayerMode(self, *args)


    def SetNameMode(self, *args) -> "void":
        """
        Set namemode for indicate write name or not.

        Parameters
        ----------
        namemode: bool

        Returns
        -------
        None

        """
        return _IGESCAFControl.IGESCAFControl_Writer_SetNameMode(self, *args)


    def Transfer(self, *args) -> "Standard_Boolean":
        """
        Transfers a document to a iges model returns true if translation is ok.

        Parameters
        ----------
        doc: TDocStd_Document
        theProgress: Message_ProgressRange,optional
        	default value is Message_ProgressRange()

        Returns
        -------
        bool

        Transfers labels to a iges model returns true if translation is ok.

        Parameters
        ----------
        labels: TDF_LabelSequence
        theProgress: Message_ProgressRange,optional
        	default value is Message_ProgressRange()

        Returns
        -------
        bool

        Transfers label to a iges model returns true if translation is ok.

        Parameters
        ----------
        label: TDF_Label
        theProgress: Message_ProgressRange,optional
        	default value is Message_ProgressRange()

        Returns
        -------
        bool

        """
        return _IGESCAFControl.IGESCAFControl_Writer_Transfer(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _IGESCAFControl.delete_IGESCAFControl_Writer
    __del__ = lambda self: None
IGESCAFControl_Writer_swigregister = _IGESCAFControl.IGESCAFControl_Writer_swigregister
IGESCAFControl_Writer_swigregister(IGESCAFControl_Writer)



# This file is compatible with both classic and new-style classes.


