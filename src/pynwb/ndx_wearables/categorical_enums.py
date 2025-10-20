from enum import Enum

# Concrete constrained subclass examples 
class SleepPhase(str, Enum):
    AWAKE = "awake"
    N1 = "n1"
    N2 = "n2"
    N3 = "n3"
    REM = "rem"

class ActivityClass(str, Enum):
    SITTING = "sitting"
    WALKING = "walking"
    RUNNING = "running"

# Add more 