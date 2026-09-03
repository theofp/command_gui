
from enum import Enum
import inspect

from . import CommandEnums
from .CommandEnums import *

PreDict = {
    "MiscType": CommandType.Misc,
    "MovementType": CommandType.Movement,
}

CommandDict = {
	command.name: PreDict[enum.__name__]
	for enum in list([MiscType, MovementType])
	if issubclass(enum, Enum)
	for command in enum
}

CommandStructure = { # Uninplemented File Loads
    
    MiscType.Undefined.name : None,
    MiscType.Wait.name : [[float]],
    MiscType.Start.name : None,
    MiscType.Stop.name : None,
    MiscType.Resume.name : None,
    MiscType.CancelMotion.name : None,
    MiscType.Return.name : None,
    MiscType.Home.name : None,
    MiscType.OpenGripper.name : None,
    MiscType.CloseGripper.name : None,
    MiscType.SavePosition.name : None,
    MiscType.SaveTrajectory.name : None,

    MovementType.GoTo.name : [[float, float, float, float, float]],
    MovementType.GoToXYZ.name : [[float, float, float],
                                [float, float, float, SolverType],
                                [float, float, float, SolverType, float]],
    MovementType.GoToL.name : [float, float, float],
    MovementType.GoToXYZL.name : [[float, float, float, float],
                                 [float, float, float, float, SolverType],
                                 [float, float, float, float, SolverType, float]]
    }