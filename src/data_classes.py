"""
Data Classes used for type hints and clarity.
"""

from dataclasses import dataclass,field


@dataclass
class CPUData:
    """CPU usage snapshot for each core and total percentage."""

    per_cpu: list[float]
    total: float


@dataclass
class MemoryData:
    """Memory usage snapshot with formatted sizes and percentage."""

    used: float
    total: float
    percent: float
    used_str: str = field(init=False)
    total_str: str = field(init=False)
    
    def __post_init__(self):
        self.used_str = convert_to_GB(self.used)
        self.total_str = convert_to_GB(self.total)
    
    def to_dict(self) -> dict:
        return {"used":self.used_str,"total":self.total_str,"percent":self.percent}


@dataclass
class DiskData:
    """Disk usage snapshot for one partition."""

    device: str
    mountpoint: str
    used: float
    total: float
    percent: float
    used_str: str = field(init=False)
    total_str: str = field(init=False)
    
    def __post_init__(self):
        self.used_str = convert_to_GB(self.used)
        self.total_str = convert_to_GB(self.total)
    
    def to_dict(self) -> dict:
        return {"used":self.used_str,"total":self.total_str,"percent":self.percent}


@dataclass
class Data:
    """Aggregated system metrics data container."""

    cpu: CPUData
    mem: MemoryData
    disks: list[DiskData]


def convert_to_GB(num: float) -> str:
    """Convert bytes to a human-readable gigabyte string.

    Args:
        num: Bytes value to convert.

    Returns:
        A string formatted as '{value:.2f}GB'.
    """
    return f"{num / 1024**3:.2f}GB"