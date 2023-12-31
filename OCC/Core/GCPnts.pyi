from enum import IntEnum
from typing import overload, NewType, Optional, Tuple

from OCC.Core.Standard import *
from OCC.Core.NCollection import *
from OCC.Core.Adaptor3d import *
from OCC.Core.Adaptor2d import *
from OCC.Core.math import *
from OCC.Core.GeomAbs import *
from OCC.Core.gp import *


class GCPnts_DeflectionType(IntEnum):
    GCPnts_Linear: int = ...
    GCPnts_Circular: int = ...
    GCPnts_Curved: int = ...
    GCPnts_DefComposite: int = ...

GCPnts_Linear = GCPnts_DeflectionType.GCPnts_Linear
GCPnts_Circular = GCPnts_DeflectionType.GCPnts_Circular
GCPnts_Curved = GCPnts_DeflectionType.GCPnts_Curved
GCPnts_DefComposite = GCPnts_DeflectionType.GCPnts_DefComposite

class GCPnts_AbscissaType(IntEnum):
    GCPnts_LengthParametrized: int = ...
    GCPnts_Parametrized: int = ...
    GCPnts_AbsComposite: int = ...

GCPnts_LengthParametrized = GCPnts_AbscissaType.GCPnts_LengthParametrized
GCPnts_Parametrized = GCPnts_AbscissaType.GCPnts_Parametrized
GCPnts_AbsComposite = GCPnts_AbscissaType.GCPnts_AbsComposite

class GCPnts_AbscissaPoint:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, Abscissa: float, U0: float) -> None: ...
    @overload
    def __init__(self, Tol: float, C: Adaptor3d_Curve, Abscissa: float, U0: float) -> None: ...
    @overload
    def __init__(self, Tol: float, C: Adaptor2d_Curve2d, Abscissa: float, U0: float) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, Abscissa: float, U0: float) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, Abscissa: float, U0: float, Ui: float) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, Abscissa: float, U0: float, Ui: float) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, Abscissa: float, U0: float, Ui: float, Tol: float) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, Abscissa: float, U0: float, Ui: float, Tol: float) -> None: ...
    def IsDone(self) -> bool: ...
    @overload
    @staticmethod
    def Length(C: Adaptor3d_Curve) -> float: ...
    @overload
    @staticmethod
    def Length(C: Adaptor2d_Curve2d) -> float: ...
    @overload
    @staticmethod
    def Length(C: Adaptor3d_Curve, Tol: float) -> float: ...
    @overload
    @staticmethod
    def Length(C: Adaptor2d_Curve2d, Tol: float) -> float: ...
    @overload
    @staticmethod
    def Length(C: Adaptor3d_Curve, U1: float, U2: float) -> float: ...
    @overload
    @staticmethod
    def Length(C: Adaptor2d_Curve2d, U1: float, U2: float) -> float: ...
    @overload
    @staticmethod
    def Length(C: Adaptor3d_Curve, U1: float, U2: float, Tol: float) -> float: ...
    @overload
    @staticmethod
    def Length(C: Adaptor2d_Curve2d, U1: float, U2: float, Tol: float) -> float: ...
    def Parameter(self) -> float: ...

class GCPnts_DistFunction2dMV(math_MultipleVarFunction):
    def __init__(self, theCurvLinDist: GCPnts_DistFunction2d) -> None: ...
    def NbVariables(self) -> int: ...
    def Value(self, X: math_Vector) -> Tuple[bool, float]: ...

class GCPnts_DistFunctionMV(math_MultipleVarFunction):
    def __init__(self, theCurvLinDist: GCPnts_DistFunction) -> None: ...
    def NbVariables(self) -> int: ...
    def Value(self, X: math_Vector) -> Tuple[bool, float]: ...

class GCPnts_QuasiUniformAbscissa:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, NbPoints: int) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, NbPoints: int, U1: float, U2: float) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, NbPoints: int) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, NbPoints: int, U1: float, U2: float) -> None: ...
    @overload
    def Initialize(self, C: Adaptor3d_Curve, NbPoints: int) -> None: ...
    @overload
    def Initialize(self, C: Adaptor3d_Curve, NbPoints: int, U1: float, U2: float) -> None: ...
    @overload
    def Initialize(self, C: Adaptor2d_Curve2d, NbPoints: int) -> None: ...
    @overload
    def Initialize(self, C: Adaptor2d_Curve2d, NbPoints: int, U1: float, U2: float) -> None: ...
    def IsDone(self) -> bool: ...
    def NbPoints(self) -> int: ...
    def Parameter(self, Index: int) -> float: ...

class GCPnts_QuasiUniformDeflection:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, Deflection: float, Continuity: Optional[GeomAbs_Shape] = GeomAbs_C1) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, Deflection: float, Continuity: Optional[GeomAbs_Shape] = GeomAbs_C1) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, Deflection: float, U1: float, U2: float, Continuity: Optional[GeomAbs_Shape] = GeomAbs_C1) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, Deflection: float, U1: float, U2: float, Continuity: Optional[GeomAbs_Shape] = GeomAbs_C1) -> None: ...
    def Deflection(self) -> float: ...
    @overload
    def Initialize(self, C: Adaptor3d_Curve, Deflection: float, Continuity: Optional[GeomAbs_Shape] = GeomAbs_C1) -> None: ...
    @overload
    def Initialize(self, C: Adaptor2d_Curve2d, Deflection: float, Continuity: Optional[GeomAbs_Shape] = GeomAbs_C1) -> None: ...
    @overload
    def Initialize(self, C: Adaptor3d_Curve, Deflection: float, U1: float, U2: float, Continuity: Optional[GeomAbs_Shape] = GeomAbs_C1) -> None: ...
    @overload
    def Initialize(self, C: Adaptor2d_Curve2d, Deflection: float, U1: float, U2: float, Continuity: Optional[GeomAbs_Shape] = GeomAbs_C1) -> None: ...
    def IsDone(self) -> bool: ...
    def NbPoints(self) -> int: ...
    def Parameter(self, Index: int) -> float: ...
    def Value(self, Index: int) -> gp_Pnt: ...

class GCPnts_TangentialDeflection:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, AngularDeflection: float, CurvatureDeflection: float, MinimumOfPoints: Optional[int] = 2, UTol: Optional[float] = 1.0e-9, theMinLen: Optional[float] = 1.0e-7) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, FirstParameter: float, LastParameter: float, AngularDeflection: float, CurvatureDeflection: float, MinimumOfPoints: Optional[int] = 2, UTol: Optional[float] = 1.0e-9, theMinLen: Optional[float] = 1.0e-7) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, AngularDeflection: float, CurvatureDeflection: float, MinimumOfPoints: Optional[int] = 2, UTol: Optional[float] = 1.0e-9, theMinLen: Optional[float] = 1.0e-7) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, FirstParameter: float, LastParameter: float, AngularDeflection: float, CurvatureDeflection: float, MinimumOfPoints: Optional[int] = 2, UTol: Optional[float] = 1.0e-9, theMinLen: Optional[float] = 1.0e-7) -> None: ...
    def AddPoint(self, thePnt: gp_Pnt, theParam: float, theIsReplace: Optional[bool] = True) -> int: ...
    @staticmethod
    def ArcAngularStep(theRadius: float, theLinearDeflection: float, theAngularDeflection: float, theMinLength: float) -> float: ...
    @overload
    def Initialize(self, C: Adaptor3d_Curve, AngularDeflection: float, CurvatureDeflection: float, MinimumOfPoints: Optional[int] = 2, UTol: Optional[float] = 1.0e-9, theMinLen: Optional[float] = 1.0e-7) -> None: ...
    @overload
    def Initialize(self, C: Adaptor3d_Curve, FirstParameter: float, LastParameter: float, AngularDeflection: float, CurvatureDeflection: float, MinimumOfPoints: Optional[int] = 2, UTol: Optional[float] = 1.0e-9, theMinLen: Optional[float] = 1.0e-7) -> None: ...
    @overload
    def Initialize(self, C: Adaptor2d_Curve2d, AngularDeflection: float, CurvatureDeflection: float, MinimumOfPoints: Optional[int] = 2, UTol: Optional[float] = 1.0e-9, theMinLen: Optional[float] = 1.0e-7) -> None: ...
    @overload
    def Initialize(self, C: Adaptor2d_Curve2d, FirstParameter: float, LastParameter: float, AngularDeflection: float, CurvatureDeflection: float, MinimumOfPoints: Optional[int] = 2, UTol: Optional[float] = 1.0e-9, theMinLen: Optional[float] = 1.0e-7) -> None: ...
    def NbPoints(self) -> int: ...
    def Parameter(self, I: int) -> float: ...
    def Value(self, I: int) -> gp_Pnt: ...

class GCPnts_UniformAbscissa:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, Abscissa: float, Toler: Optional[float] = -1) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, Abscissa: float, U1: float, U2: float, Toler: Optional[float] = -1) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, NbPoints: int, Toler: Optional[float] = -1) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, NbPoints: int, U1: float, U2: float, Toler: Optional[float] = -1) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, Abscissa: float, Toler: Optional[float] = -1) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, Abscissa: float, U1: float, U2: float, Toler: Optional[float] = -1) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, NbPoints: int, Toler: Optional[float] = -1) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, NbPoints: int, U1: float, U2: float, Toler: Optional[float] = -1) -> None: ...
    def Abscissa(self) -> float: ...
    @overload
    def Initialize(self, C: Adaptor3d_Curve, Abscissa: float, Toler: Optional[float] = -1) -> None: ...
    @overload
    def Initialize(self, C: Adaptor3d_Curve, Abscissa: float, U1: float, U2: float, Toler: Optional[float] = -1) -> None: ...
    @overload
    def Initialize(self, C: Adaptor3d_Curve, NbPoints: int, Toler: Optional[float] = -1) -> None: ...
    @overload
    def Initialize(self, C: Adaptor3d_Curve, NbPoints: int, U1: float, U2: float, Toler: Optional[float] = -1) -> None: ...
    @overload
    def Initialize(self, C: Adaptor2d_Curve2d, Abscissa: float, Toler: Optional[float] = -1) -> None: ...
    @overload
    def Initialize(self, C: Adaptor2d_Curve2d, Abscissa: float, U1: float, U2: float, Toler: Optional[float] = -1) -> None: ...
    @overload
    def Initialize(self, C: Adaptor2d_Curve2d, NbPoints: int, Toler: Optional[float] = -1) -> None: ...
    @overload
    def Initialize(self, C: Adaptor2d_Curve2d, NbPoints: int, U1: float, U2: float, Toler: Optional[float] = -1) -> None: ...
    def IsDone(self) -> bool: ...
    def NbPoints(self) -> int: ...
    def Parameter(self, Index: int) -> float: ...

class GCPnts_UniformDeflection:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, Deflection: float, WithControl: Optional[bool] = True) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, Deflection: float, WithControl: Optional[bool] = True) -> None: ...
    @overload
    def __init__(self, C: Adaptor3d_Curve, Deflection: float, U1: float, U2: float, WithControl: Optional[bool] = True) -> None: ...
    @overload
    def __init__(self, C: Adaptor2d_Curve2d, Deflection: float, U1: float, U2: float, WithControl: Optional[bool] = True) -> None: ...
    def Deflection(self) -> float: ...
    @overload
    def Initialize(self, C: Adaptor3d_Curve, Deflection: float, WithControl: Optional[bool] = True) -> None: ...
    @overload
    def Initialize(self, C: Adaptor2d_Curve2d, Deflection: float, WithControl: Optional[bool] = True) -> None: ...
    @overload
    def Initialize(self, C: Adaptor3d_Curve, Deflection: float, U1: float, U2: float, WithControl: Optional[bool] = True) -> None: ...
    @overload
    def Initialize(self, C: Adaptor2d_Curve2d, Deflection: float, U1: float, U2: float, WithControl: Optional[bool] = True) -> None: ...
    def IsDone(self) -> bool: ...
    def NbPoints(self) -> int: ...
    def Parameter(self, Index: int) -> float: ...
    def Value(self, Index: int) -> gp_Pnt: ...

#classnotwrapped
class GCPnts_DistFunction: ...

#classnotwrapped
class GCPnts_DistFunction2d: ...

# harray1 classes
# harray2 classes
# hsequence classes

GCPnts_AbscissaPoint_Length = GCPnts_AbscissaPoint.Length
GCPnts_AbscissaPoint_Length = GCPnts_AbscissaPoint.Length
GCPnts_AbscissaPoint_Length = GCPnts_AbscissaPoint.Length
GCPnts_AbscissaPoint_Length = GCPnts_AbscissaPoint.Length
GCPnts_AbscissaPoint_Length = GCPnts_AbscissaPoint.Length
GCPnts_AbscissaPoint_Length = GCPnts_AbscissaPoint.Length
GCPnts_AbscissaPoint_Length = GCPnts_AbscissaPoint.Length
GCPnts_AbscissaPoint_Length = GCPnts_AbscissaPoint.Length
GCPnts_TangentialDeflection_ArcAngularStep = GCPnts_TangentialDeflection.ArcAngularStep
