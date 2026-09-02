from enum import Enum

# General Command Types

class CommandType(Enum):

    Undefined = 0
    Movement = 1
    Misc = 2
    Trajectory = 3


# Command Subtypes

class MiscType(Enum):

    Undefined = 0
    Wait = 1
    Start = 2
    Stop = 3 
    Resume = 4
    CancelMotion = 5
    Return = 6
    Home = 7
    OpenGripper = 8
    CloseGripper = 9
    SavePosition = 10
    SaveTrajectory = 11

class MovementType(Enum):

    Undefined = 0
    GoTo = 1
    GoToXYZ = 2
    GoToL = 3
    GoToXYZL = 4

# MISC

class SolverType(Enum):

    Undefined = 0
    StaticWrist = 1
    FourD = 2
    FourDSmart = 3
    FiveD = 4
    FiveDSmart = 5

class MotionTypeXYZ(Enum):

    Undefined = 0
    Joint = 2
    Linear = 4

class MotionType(Enum):
  
  Undefined = 0
  Joint = 1
  Linear = 3 