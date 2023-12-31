# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

"""
Intrv module, see official documentation at
https://www.opencascade.com/doc/occt-7.4.0/refman/html/package_intrv.html
"""


from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_Intrv')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_Intrv')
    _Intrv = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_Intrv', [dirname(__file__)])
        except ImportError:
            import _Intrv
            return _Intrv
        try:
            _mod = imp.load_module('_Intrv', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _Intrv = swig_import_helper()
    del swig_import_helper
else:
    import _Intrv
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
    __swig_destroy__ = _Intrv.delete_SwigPyIterator
    __del__ = lambda self: None

    def value(self) -> "PyObject *":
        return _Intrv.SwigPyIterator_value(self)

    def incr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _Intrv.SwigPyIterator_incr(self, n)

    def decr(self, n: 'size_t'=1) -> "swig::SwigPyIterator *":
        return _Intrv.SwigPyIterator_decr(self, n)

    def distance(self, x: 'SwigPyIterator') -> "ptrdiff_t":
        return _Intrv.SwigPyIterator_distance(self, x)

    def equal(self, x: 'SwigPyIterator') -> "bool":
        return _Intrv.SwigPyIterator_equal(self, x)

    def copy(self) -> "swig::SwigPyIterator *":
        return _Intrv.SwigPyIterator_copy(self)

    def next(self) -> "PyObject *":
        return _Intrv.SwigPyIterator_next(self)

    def __next__(self) -> "PyObject *":
        return _Intrv.SwigPyIterator___next__(self)

    def previous(self) -> "PyObject *":
        return _Intrv.SwigPyIterator_previous(self)

    def advance(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _Intrv.SwigPyIterator_advance(self, n)

    def __eq__(self, x: 'SwigPyIterator') -> "bool":
        return _Intrv.SwigPyIterator___eq__(self, x)

    def __ne__(self, x: 'SwigPyIterator') -> "bool":
        return _Intrv.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _Intrv.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator &":
        return _Intrv.SwigPyIterator___isub__(self, n)

    def __add__(self, n: 'ptrdiff_t') -> "swig::SwigPyIterator *":
        return _Intrv.SwigPyIterator___add__(self, n)

    def __sub__(self, *args) -> "ptrdiff_t":
        return _Intrv.SwigPyIterator___sub__(self, *args)
    def __iter__(self):
        return self
SwigPyIterator_swigregister = _Intrv.SwigPyIterator_swigregister
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
    return _Intrv.process_exception(error, method_name, class_name)
process_exception = _Intrv.process_exception

from six import with_metaclass
import warnings
from OCC.Wrapper.wrapper_utils import Proxy, deprecated

import OCC.Core.Standard
import OCC.Core.NCollection

from enum import IntEnum
from OCC.Core.Exception import *

Intrv_Before = _Intrv.Intrv_Before
Intrv_JustBefore = _Intrv.Intrv_JustBefore
Intrv_OverlappingAtStart = _Intrv.Intrv_OverlappingAtStart
Intrv_JustEnclosingAtEnd = _Intrv.Intrv_JustEnclosingAtEnd
Intrv_Enclosing = _Intrv.Intrv_Enclosing
Intrv_JustOverlappingAtStart = _Intrv.Intrv_JustOverlappingAtStart
Intrv_Similar = _Intrv.Intrv_Similar
Intrv_JustEnclosingAtStart = _Intrv.Intrv_JustEnclosingAtStart
Intrv_Inside = _Intrv.Intrv_Inside
Intrv_JustOverlappingAtEnd = _Intrv.Intrv_JustOverlappingAtEnd
Intrv_OverlappingAtEnd = _Intrv.Intrv_OverlappingAtEnd
Intrv_JustAfter = _Intrv.Intrv_JustAfter
Intrv_After = _Intrv.Intrv_After


class Intrv_Position(IntEnum):
	Intrv_Before = 0
	Intrv_JustBefore = 1
	Intrv_OverlappingAtStart = 2
	Intrv_JustEnclosingAtEnd = 3
	Intrv_Enclosing = 4
	Intrv_JustOverlappingAtStart = 5
	Intrv_Similar = 6
	Intrv_JustEnclosingAtStart = 7
	Intrv_Inside = 8
	Intrv_JustOverlappingAtEnd = 9
	Intrv_OverlappingAtEnd = 10
	Intrv_JustAfter = 11
	Intrv_After = 12
Intrv_Before = Intrv_Position.Intrv_Before
Intrv_JustBefore = Intrv_Position.Intrv_JustBefore
Intrv_OverlappingAtStart = Intrv_Position.Intrv_OverlappingAtStart
Intrv_JustEnclosingAtEnd = Intrv_Position.Intrv_JustEnclosingAtEnd
Intrv_Enclosing = Intrv_Position.Intrv_Enclosing
Intrv_JustOverlappingAtStart = Intrv_Position.Intrv_JustOverlappingAtStart
Intrv_Similar = Intrv_Position.Intrv_Similar
Intrv_JustEnclosingAtStart = Intrv_Position.Intrv_JustEnclosingAtStart
Intrv_Inside = Intrv_Position.Intrv_Inside
Intrv_JustOverlappingAtEnd = Intrv_Position.Intrv_JustOverlappingAtEnd
Intrv_OverlappingAtEnd = Intrv_Position.Intrv_OverlappingAtEnd
Intrv_JustAfter = Intrv_Position.Intrv_JustAfter
Intrv_After = Intrv_Position.Intrv_After

class Intrv_SequenceOfInterval(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Intrv_SequenceOfInterval, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Intrv_SequenceOfInterval, name)
    __repr__ = _swig_repr

    def begin(self) -> "NCollection_Sequence< Intrv_Interval >::iterator":
        return _Intrv.Intrv_SequenceOfInterval_begin(self)

    def end(self) -> "NCollection_Sequence< Intrv_Interval >::iterator":
        return _Intrv.Intrv_SequenceOfInterval_end(self)

    def cbegin(self) -> "NCollection_Sequence< Intrv_Interval >::const_iterator":
        return _Intrv.Intrv_SequenceOfInterval_cbegin(self)

    def cend(self) -> "NCollection_Sequence< Intrv_Interval >::const_iterator":
        return _Intrv.Intrv_SequenceOfInterval_cend(self)

    def __init__(self, *args):
        this = _Intrv.new_Intrv_SequenceOfInterval(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Size(self) -> "Standard_Integer":
        return _Intrv.Intrv_SequenceOfInterval_Size(self)

    def Length(self) -> "Standard_Integer":
        return _Intrv.Intrv_SequenceOfInterval_Length(self)

    def Lower(self) -> "Standard_Integer":
        return _Intrv.Intrv_SequenceOfInterval_Lower(self)

    def Upper(self) -> "Standard_Integer":
        return _Intrv.Intrv_SequenceOfInterval_Upper(self)

    def IsEmpty(self) -> "Standard_Boolean":
        return _Intrv.Intrv_SequenceOfInterval_IsEmpty(self)

    def Reverse(self) -> "void":
        return _Intrv.Intrv_SequenceOfInterval_Reverse(self)

    def Exchange(self, I: 'Standard_Integer const', J: 'Standard_Integer const') -> "void":
        return _Intrv.Intrv_SequenceOfInterval_Exchange(self, I, J)
    if _newclass:
        delNode = staticmethod(_Intrv.Intrv_SequenceOfInterval_delNode)
    else:
        delNode = _Intrv.Intrv_SequenceOfInterval_delNode

    def Clear(self, theAllocator: 'opencascade::handle< NCollection_BaseAllocator > const &'=0) -> "void":
        return _Intrv.Intrv_SequenceOfInterval_Clear(self, theAllocator)

    def Assign(self, theOther: 'Intrv_SequenceOfInterval') -> "NCollection_Sequence< Intrv_Interval > &":
        return _Intrv.Intrv_SequenceOfInterval_Assign(self, theOther)

    def Set(self, theOther: 'Intrv_SequenceOfInterval') -> "NCollection_Sequence< Intrv_Interval > &":
        return _Intrv.Intrv_SequenceOfInterval_Set(self, theOther)

    def Remove(self, *args) -> "void":
        return _Intrv.Intrv_SequenceOfInterval_Remove(self, *args)

    def Append(self, *args) -> "void":
        return _Intrv.Intrv_SequenceOfInterval_Append(self, *args)

    def Prepend(self, *args) -> "void":
        return _Intrv.Intrv_SequenceOfInterval_Prepend(self, *args)

    def InsertBefore(self, *args) -> "void":
        return _Intrv.Intrv_SequenceOfInterval_InsertBefore(self, *args)

    def InsertAfter(self, *args) -> "void":
        return _Intrv.Intrv_SequenceOfInterval_InsertAfter(self, *args)

    def Split(self, theIndex: 'Standard_Integer const', theSeq: 'Intrv_SequenceOfInterval') -> "void":
        return _Intrv.Intrv_SequenceOfInterval_Split(self, theIndex, theSeq)

    def First(self) -> "Intrv_Interval const &":
        return _Intrv.Intrv_SequenceOfInterval_First(self)

    def ChangeFirst(self) -> "Intrv_Interval &":
        return _Intrv.Intrv_SequenceOfInterval_ChangeFirst(self)

    def Last(self) -> "Intrv_Interval const &":
        return _Intrv.Intrv_SequenceOfInterval_Last(self)

    def ChangeLast(self) -> "Intrv_Interval &":
        return _Intrv.Intrv_SequenceOfInterval_ChangeLast(self)

    def Value(self, theIndex: 'Standard_Integer const') -> "Intrv_Interval const &":
        return _Intrv.Intrv_SequenceOfInterval_Value(self, theIndex)

    def ChangeValue(self, theIndex: 'Standard_Integer const') -> "Intrv_Interval &":
        return _Intrv.Intrv_SequenceOfInterval_ChangeValue(self, theIndex)

    def __call__(self, *args) -> "Intrv_Interval &":
        return _Intrv.Intrv_SequenceOfInterval___call__(self, *args)

    def SetValue(self, theIndex: 'Standard_Integer const', theItem: 'Intrv_Interval') -> "void":
        return _Intrv.Intrv_SequenceOfInterval_SetValue(self, theIndex, theItem)
    __swig_destroy__ = _Intrv.delete_Intrv_SequenceOfInterval
    __del__ = lambda self: None

    def __len__(self):
        return self.Size()

Intrv_SequenceOfInterval_swigregister = _Intrv.Intrv_SequenceOfInterval_swigregister
Intrv_SequenceOfInterval_swigregister(Intrv_SequenceOfInterval)

def Intrv_SequenceOfInterval_delNode(theNode: 'NCollection_SeqNode *', theAl: 'opencascade::handle< NCollection_BaseAllocator > &') -> "void":
    return _Intrv.Intrv_SequenceOfInterval_delNode(theNode, theAl)
Intrv_SequenceOfInterval_delNode = _Intrv.Intrv_SequenceOfInterval_delNode

class Intrv_Interval(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Intrv_Interval, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Intrv_Interval, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        No available documentation.

        Returns
        -------
        None

        No available documentation.

        Parameters
        ----------
        Start: float
        End: float

        Returns
        -------
        None

        No available documentation.

        Parameters
        ----------
        Start: float
        TolStart: Standard_ShortReal
        End: float
        TolEnd: Standard_ShortReal

        Returns
        -------
        None

        """
        this = _Intrv.new_Intrv_Interval(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Bounds(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        TolStart: Standard_ShortReal
        TolEnd: Standard_ShortReal

        Returns
        -------
        Start: float
        End: float

        """
        return _Intrv.Intrv_Interval_Bounds(self, *args)


    def CutAtEnd(self, *args) -> "void":
        """
        <-----****+****  old one **+**------> tool for cutting <<< <<< <-----****+****  result.

        Parameters
        ----------
        End: float
        TolEnd: Standard_ShortReal

        Returns
        -------
        None

        """
        return _Intrv.Intrv_Interval_CutAtEnd(self, *args)


    def CutAtStart(self, *args) -> "void":
        """
        ****+****-----------> old one <----------**+** tool for cutting >>> >>> ****+****-----------> result.

        Parameters
        ----------
        Start: float
        TolStart: Standard_ShortReal

        Returns
        -------
        None

        """
        return _Intrv.Intrv_Interval_CutAtStart(self, *args)


    def End(self, *args) -> "Standard_Real":
        """
        No available documentation.

        Returns
        -------
        float

        """
        return _Intrv.Intrv_Interval_End(self, *args)


    def FuseAtEnd(self, *args) -> "void":
        """
        <---------------------****+**** old one <-----------------**+**  new one to fuse >>> >>> <---------------------****+**** result.

        Parameters
        ----------
        End: float
        TolEnd: Standard_ShortReal

        Returns
        -------
        None

        """
        return _Intrv.Intrv_Interval_FuseAtEnd(self, *args)


    def FuseAtStart(self, *args) -> "void":
        """
        ****+****--------------------> old one ****+****------------------------> new one to fuse <<< <<< ****+****------------------------> result.

        Parameters
        ----------
        Start: float
        TolStart: Standard_ShortReal

        Returns
        -------
        None

        """
        return _Intrv.Intrv_Interval_FuseAtStart(self, *args)


    def IsAfter(self, *args) -> "Standard_Boolean":
        """
        True if me is after other **-----------**** me ***----------------**  other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsAfter(self, *args)


    def IsBefore(self, *args) -> "Standard_Boolean":
        """
        True if me is before other ***----------------**  me **-----------**** other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsBefore(self, *args)


    def IsEnclosing(self, *args) -> "Standard_Boolean":
        """
        True if me is enclosing other ***----------------------------**** me ***------------------** other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsEnclosing(self, *args)


    def IsInside(self, *args) -> "Standard_Boolean":
        """
        True if me is inside other **-----------****  me ***--------------------------**  other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsInside(self, *args)


    def IsJustAfter(self, *args) -> "Standard_Boolean":
        """
        True if me is just after other ****-------****  me ***-----------**  other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsJustAfter(self, *args)


    def IsJustBefore(self, *args) -> "Standard_Boolean":
        """
        True if me is just before other ***--------****   me ***-----------** other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsJustBefore(self, *args)


    def IsJustEnclosingAtEnd(self, *args) -> "Standard_Boolean":
        """
        True if me is just enclosing other at end ***----------------------------**** me ***-----------------****  other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsJustEnclosingAtEnd(self, *args)


    def IsJustEnclosingAtStart(self, *args) -> "Standard_Boolean":
        """
        True if me is just enclosing other at start ***---------------------------**** me ***------------------** other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsJustEnclosingAtStart(self, *args)


    def IsJustOverlappingAtEnd(self, *args) -> "Standard_Boolean":
        """
        True if me is just overlapping other at end ***-----------*  me ***------------------------** other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsJustOverlappingAtEnd(self, *args)


    def IsJustOverlappingAtStart(self, *args) -> "Standard_Boolean":
        """
        True if me is just overlapping other at start ***-----------***  me ***------------------------** other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsJustOverlappingAtStart(self, *args)


    def IsOverlappingAtEnd(self, *args) -> "Standard_Boolean":
        """
        True if me is overlapping other at end ***-----------** me ***---------------***  other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsOverlappingAtEnd(self, *args)


    def IsOverlappingAtStart(self, *args) -> "Standard_Boolean":
        """
        True if me is overlapping other at start ***---------------***  me ***-----------** other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsOverlappingAtStart(self, *args)


    def IsProbablyEmpty(self, *args) -> "Standard_Boolean":
        """
        True if mystart+mytolstart > myend-mytolend or if myend+mytolend > mystart-mytolstart.

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsProbablyEmpty(self, *args)


    def IsSimilar(self, *args) -> "Standard_Boolean":
        """
        True if me and other have the same bounds *----------------***  me ***-----------------**  other.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        bool

        """
        return _Intrv.Intrv_Interval_IsSimilar(self, *args)


    def Position(self, *args) -> "Intrv_Position":
        """
        True if me is before other **-----------**** other ***-----*   before ***------------*  justbefore ***-----------------*  overlappingatstart ***--------------------------*  justenclosingatend ***-------------------------------------* enclosing ***----*  justoverlappingatstart ***-------------*  similar ***------------------------* justenclosingatstart ***-*  inside ***------*  justoverlappingatend ***-----------------* overlappingatend ***--------* justafter ***---* after.

        Parameters
        ----------
        Other: Intrv_Interval

        Returns
        -------
        Intrv_Position

        """
        return _Intrv.Intrv_Interval_Position(self, *args)


    def SetEnd(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        End: float
        TolEnd: Standard_ShortReal

        Returns
        -------
        None

        """
        return _Intrv.Intrv_Interval_SetEnd(self, *args)


    def SetStart(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        Start: float
        TolStart: Standard_ShortReal

        Returns
        -------
        None

        """
        return _Intrv.Intrv_Interval_SetStart(self, *args)


    def Start(self, *args) -> "Standard_Real":
        """
        No available documentation.

        Returns
        -------
        float

        """
        return _Intrv.Intrv_Interval_Start(self, *args)


    def TolEnd(self, *args) -> "Standard_ShortReal":
        """
        No available documentation.

        Returns
        -------
        Standard_ShortReal

        """
        return _Intrv.Intrv_Interval_TolEnd(self, *args)


    def TolStart(self, *args) -> "Standard_ShortReal":
        """
        No available documentation.

        Returns
        -------
        Standard_ShortReal

        """
        return _Intrv.Intrv_Interval_TolStart(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _Intrv.delete_Intrv_Interval
    __del__ = lambda self: None
Intrv_Interval_swigregister = _Intrv.Intrv_Interval_swigregister
Intrv_Interval_swigregister(Intrv_Interval)

class Intrv_Intervals(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Intrv_Intervals, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Intrv_Intervals, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        """
        Creates a void sequence of intervals.

        Returns
        -------
        None

        Creates a sequence of one interval.

        Parameters
        ----------
        Int: Intrv_Interval

        Returns
        -------
        None

        """
        this = _Intrv.new_Intrv_Intervals(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def Intersect(self, *args) -> "void":
        """
        Intersects the intervals with the interval <tool>.

        Parameters
        ----------
        Tool: Intrv_Interval

        Returns
        -------
        None

        Intersects the intervals with the intervals in the sequence <tool>.

        Parameters
        ----------
        Tool: Intrv_Intervals

        Returns
        -------
        None

        """
        return _Intrv.Intrv_Intervals_Intersect(self, *args)


    def NbIntervals(self, *args) -> "Standard_Integer":
        """
        No available documentation.

        Returns
        -------
        int

        """
        return _Intrv.Intrv_Intervals_NbIntervals(self, *args)


    def Subtract(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        Tool: Intrv_Interval

        Returns
        -------
        None

        No available documentation.

        Parameters
        ----------
        Tool: Intrv_Intervals

        Returns
        -------
        None

        """
        return _Intrv.Intrv_Intervals_Subtract(self, *args)


    def Unite(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        Tool: Intrv_Interval

        Returns
        -------
        None

        No available documentation.

        Parameters
        ----------
        Tool: Intrv_Intervals

        Returns
        -------
        None

        """
        return _Intrv.Intrv_Intervals_Unite(self, *args)


    def Value(self, *args) -> "Intrv_Interval const &":
        """
        No available documentation.

        Parameters
        ----------
        Index: int

        Returns
        -------
        Intrv_Interval

        """
        return _Intrv.Intrv_Intervals_Value(self, *args)


    def XUnite(self, *args) -> "void":
        """
        No available documentation.

        Parameters
        ----------
        Tool: Intrv_Interval

        Returns
        -------
        None

        No available documentation.

        Parameters
        ----------
        Tool: Intrv_Intervals

        Returns
        -------
        None

        """
        return _Intrv.Intrv_Intervals_XUnite(self, *args)


    __repr__ = _dumps_object

    __swig_destroy__ = _Intrv.delete_Intrv_Intervals
    __del__ = lambda self: None
Intrv_Intervals_swigregister = _Intrv.Intrv_Intervals_swigregister
Intrv_Intervals_swigregister(Intrv_Intervals)



# This file is compatible with both classic and new-style classes.


