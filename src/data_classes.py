"""
Data Classes used for type hints and clarity.
"""

from dataclasses import dataclass


@dataclass
class CPUData:
    """CPU usage snapshot for each core and total percentage."""

    per_cpu: list[float]
    total: float


@dataclass
class MemoryData:
    """Memory usage snapshot with formatted sizes and percentage."""

    used: str
    total: str
    percent: float


@dataclass
class DiskData:
    """Disk usage snapshot for one partition."""

    device: str
    mountpoint: str
    used: str
    total: str
    percent: float


@dataclass
class Data:
    """Aggregated system metrics data container."""

    cpu: CPUData
    mem: MemoryData
    disks: list[DiskData]
