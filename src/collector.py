"""
Collect the metrics displayed to user.
This module provides helpers for CPU, memory, and disk metrics via psutil.
"""

import psutil

from src.data_classes import CPUData, MemoryData, DiskData


def get_cpu_usage(interval: float, force: bool = True) -> CPUData:
    """Get CPU usage for each core and total CPU usage.

    Args:
        interval: Sample interval in seconds. This function will sleep for interval seconds.
        force: Placeholder argument for compatibility/current API usage.

    Returns:
        CPUData object with per-core percentages and total percentage.

    Raises:
        RuntimeError: If psutil returns an empty per-core list.
    """
    cpu_percent_list = psutil.cpu_percent(interval, percpu=True)

    if not cpu_percent_list:
        raise RuntimeError("Cores list is empty - psutil has failed for some reason")

    total_cpu_percent = round(
        sum(cpu_percent_list) / len(cpu_percent_list), 1
    )  # Average percent rounded to one decimal point
    return CPUData(cpu_percent_list, total_cpu_percent)


def get_memory() -> MemoryData:
    """Get memory usage statistics.

    Returns:
        MemoryData with used, total (formatted as GB strings) and percentage used.
    """
    mem_stats = psutil.virtual_memory()
    total = mem_stats.total  # Total
    available = (  # noqa: F841
        mem_stats.available
    )  # Memory that can be given by the os immediately  # noqa: F841
    percent = mem_stats.percent  # total - available / total * 100
    used = mem_stats.used  # Memory currently in use
    free = mem_stats.free  # noqa: F841
    return MemoryData(convert_to_GB(used), convert_to_GB(total), percent)


def get_disk() -> list[DiskData]:
    """Get disk usage statistics for each mounted partition.

    Returns:
        List of DiskData objects with device, mountpoint, used, total, and percent used.
    """
    """
    Input: no input

    Output: List of every partition info (mountpoint, device, total, used, percent) (list[dict])
    """
    disk_list: list[DiskData] = []

    for disk_par in psutil.disk_partitions():
        usage = psutil.disk_usage(disk_par.mountpoint)

        disk_list.append(
            DiskData(
                disk_par.device,
                disk_par.mountpoint,
                convert_to_GB(usage.used),
                convert_to_GB(usage.total),
                usage.percent,
            )
        )

    return disk_list


def convert_to_GB(num: float) -> str:
    """Convert bytes to a human-readable gigabyte string.

    Args:
        num: Bytes value to convert.

    Returns:
        A string formatted as '{value:.2f}GB'.
    """
    return f"{num / 1024**3:.2f}GB"


if __name__ == "__main__":
    print(
        "Warning, you are trying to run collector.py, that shouldn't be run directly. Are you sure you want to continue this action? (Y/N) (Useful only for dev testing)"
    )
    if "Y" in input():
        print(get_cpu_usage(2))
        print(get_memory())
        print(get_disk())
    else:
        print("exiting...")
