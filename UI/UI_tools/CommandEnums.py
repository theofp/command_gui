from enum import Enum

class CommandType(Enum):

    Undefined = 0
    Movement = 1
    Misc = 2
    Trajectory = 3


class MovementType(Enum):

    Undefined = 0
    GoTo = 1
    GoToXYZ = 2
    GoToL = 3
    GoToXYZL = 4

class SolverType(Enum):

    Undefined = 0
    StaticWrist = 1
    FourD = 2
    FourDSmart = 3
    FiveD = 4
    FiveDSmart = 5

class MiscType(Enum):

    Undefined = 0
    Wait = 1
    Stop = 2
    Resume = 3
    WaitAndResume = 4
    GoHome = 5
    SaveMovement = 6
    Backtrack = 7
    Start = 8
    