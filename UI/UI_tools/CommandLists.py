
from enum import Enum
import inspect

from . import CommandEnums
from .CommandEnums import *


Commands = {
	command.value: enum.__name__
	for _, enum in inspect.getmembers(CommandEnums, inspect.isclass)
	if issubclass(enum, Enum)
	for command in enum
}

CommandStructure = { # Uninplemented File Loads
    
    MiscType.Undefined.name : None,
    MiscType.Wait : [float],
    MiscType.Start : None,
    MiscType.Stop : None,
    MiscType.Resume : None,
    MiscType.CancelMotion : None,
    MiscType.Return : None,
    MiscType.Home : None,
    MiscType.OpenGripper : None,
    MiscType.CloseGripper : None,
    MiscType.SavePosition : None,
    MiscType.SaveTrajectory : None,

    MovementType.GoTo : [[float, float, float, float, float]],
    MovementType.GoToXYZ : [[float, float, float],
                             [float, float, float, SolverType],
                             [float, float, float, SolverType, float]],
    MovementType.GoToL : [float, float, float],
    MovementType.GoToXYZL : [[float, float, float, float],
                              [float, float, float, float, SolverType],
                              [float, float, float, float, SolverType, float]]
    }