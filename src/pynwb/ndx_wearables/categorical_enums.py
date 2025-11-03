from enum import Enum
from hdmf.common import DynamicTable
try:
    # HDMF is where DynamicTable lives
    from hdmf.common import DynamicTable
except Exception as e:
    raise ImportError("hdmf is required for meanings table builders") from e


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

def build_sleep_phase_meanings():
    table = DynamicTable(
        name="sleep_phase_meanings",
        description="Category definitions for sleep stages",
    )
    # create empty columns first
    table.add_column(name="category", description="Sleep phase label")
    table.add_column(name="meaning", description="Human-readable description")

    labels = [e.value for e in SleepPhase]
    descs = [
        "Wakefulness",
        "Non-REM stage 1",
        "Non-REM stage 2",
        "Non-REM stage 3 (deep sleep)",
        "Rapid eye movement (REM) sleep",
    ]
    for cat, desc in zip(labels, descs):
        table.add_row(category=cat, meaning=desc)

    return table

def build_activity_class_meanings():
    table = DynamicTable(
        name="activity_class_meanings",
        description="Category definitions for activity classes",
    )
    table.add_column(name="category", description="Activity label")
    table.add_column(name="meaning", description="Human-readable description")

    labels = [e.value for e in ActivityClass]
    descs = [
        "Minimal movement",
        "Ambulatory movement at a comfortable pace",
        "Ambulatory movement at a faster pace",
    ]
    for cat, desc in zip(labels, descs):
        table.add_row(category=cat, meaning=desc)

    return table

ENUM_MAP = {
    "sleep_phase": SleepPhase,
    "activity_class": ActivityClass,
}