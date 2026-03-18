"""
Data Classes used for type hints and clearabillity
"""

from dataclasses import dataclass

@dataclass
class CPUData:
    per_cpu: list[float]
    total: float

@dataclass
class MemoryData:
    used: str
    total: str
    percent: float

@dataclass
class DiskData:
    device: str
    mountpoint: str
    used: str
    total: str
    percent: float



@dataclass
class Data:
    cpu: CPUData
    mem: MemoryData
    disks: list[DiskData]

