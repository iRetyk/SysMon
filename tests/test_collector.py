import pytest

from collections import namedtuple

from src import (
    CPUData,
    MemoryData,
    DiskData,
    get_cpu_usage,
    get_memory,
    get_disk,
    convert_to_GB,
)


########################
## Test get_cpu_usage ##
########################
@pytest.mark.parametrize(
    "mock_per_core,mock_total",
    [
        ([0.0, 0.0, 0.0, 0.0], 0.0),
        ([10.0, 20.0, 30.0, 40.0], 25.0),
        ([100.0, 100.0, 100.0, 100.0], 100.0),
        ([0.0, 50.0, 50.0, 100.0], 50.0),
        ([1.0, 2.0, 3.0, 4.0], 2.5),
        ([33.3, 33.3, 33.4], 33.3),
        ([0.0], 0.0),
        ([100.0, 0.0, 50.0, 25.0], 43.8),
    ],
)
def test_cpu(mocker, mock_per_core, mock_total):
    mocker.patch("src.collector.psutil.cpu_percent", return_value=mock_per_core)
    assert CPUData(mock_per_core, mock_total) == get_cpu_usage(2)


def test_cpu_empty_list(mocker):
    mocker.patch("src.collector.psutil.cpu_percent", return_value=[])

    with pytest.raises(RuntimeError):
        get_cpu_usage(2)


#####################
## Test get_memory ##
#####################

mock_svmem = namedtuple("svmem", ["total", "available", "free", "used", "percent"])


@pytest.mark.parametrize(
    "total,available,free,used,percent",
    [
        (20, 10, 15, 7, 6.5),
        (0, 0, 0, 0, 0),
    ],
)
def test_mem(mocker, total, available, free, used, percent):
    mock_memory_object = mock_svmem(
        total=total, available=available, free=free, used=used, percent=percent
    )

    mocker.patch("src.collector.psutil.virtual_memory", return_value=mock_memory_object)

    mem_stats = get_memory()

    assert mem_stats == MemoryData(convert_to_GB(used), convert_to_GB(total), percent)


###################
## Test get_disk ##
###################


Partition = namedtuple("Partition", ["mountpoint", "device"])
Usage = namedtuple("Usage", ["total", "used", "percent"])


@pytest.mark.parametrize(
    "mountpoint,device,total,used,percent",
    [
        ("/", "/dev/sda1", 500_000_000_000, 300_000_000_000, 60.0),
        ("/data", "/dev/sdb1", 1_000_000_000_000, 400_000_000_000, 40.0),
    ],
)
def test_disk(mocker, mountpoint, device, total, used, percent):
    mocker.patch(
        "psutil.disk_partitions",
        return_value=[Partition(mountpoint=mountpoint, device=device)],
    )
    mocker.patch(
        "psutil.disk_usage", return_value=Usage(total=total, used=used, percent=percent)
    )
    disk_stats_list = get_disk()

    assert disk_stats_list == [
        DiskData(device, mountpoint, convert_to_GB(used), convert_to_GB(total), percent)
    ]
