"""Tests for logger module."""

import pytest

import json
from unittest.mock import MagicMock
from dataclasses import asdict

from src import Logger, Data, CPUData, MemoryData, DiskData


##############
## Test log ##
##############


@pytest.mark.parametrize(
    "mock_data,mock_time",
    [
        (
            Data(
                cpu=CPUData(per_cpu=[5.0, 30.4, 7.8, 6.7], total=15.2),
                mem=MemoryData(used="20.00 GB", total="40.00 GB", percent=40.0),
                disks=[
                    DiskData(
                        device="/dev/disk1",
                        mountpoint="/",
                        used="1.50 GB",
                        total="8.00 GB",
                        percent=70.0,
                    ),
                    DiskData(
                        device="/dev/disk2",
                        mountpoint="/data",
                        used="0.20 GB",
                        total="18.00 GB",
                        percent=98.0,
                    ),
                ],
            ),
            "2026-03-18T15:42:10.123456",
        ),
        (
            Data(
                cpu=CPUData(per_cpu=[], total=0.0),
                mem=MemoryData(used="0 GB", total="0 GB", percent=0.0),
                disks=[],
            ),
            "0000",
        ),
    ],
)
def test_log(mocker, mock_data: Data, mock_time):
    """
    Test the log method of the Logger class.
    """

    # mock all function calls inside Logger.log
    mock_dt = mocker.patch("src.logger.datetime.datetime")
    mock_dt.now.return_value.isoformat.return_value = mock_time
    mock_log_json: MagicMock = mocker.patch("src.logger.Logger.log_json")

    logger = Logger("/")
    logger.log(mock_data)

    # Making a hard copy is necessary - If making shallow copy or using the same object the test doesn't detect some failures.
    mock_data_copy = {k: v for k, v in asdict(mock_data).items()}
    mock_data_copy["time"] = mock_time

    mock_log_json.assert_called_once_with(mock_data_copy)


###################
## Test log_json ##
###################


@pytest.mark.parametrize(
    "mock_data",
    [
        (
            Data(
                cpu=CPUData(per_cpu=[5.0, 30.4, 7.8, 6.7], total=15.2),
                mem=MemoryData(used="20.00 GB", total="40.00 GB", percent=40.0),
                disks=[
                    DiskData(
                        device="/dev/disk1",
                        mountpoint="/",
                        used="1.50 GB",
                        total="8.00 GB",
                        percent=70.0,
                    ),
                    DiskData(
                        device="/dev/disk2",
                        mountpoint="/data",
                        used="0.20 GB",
                        total="18.00 GB",
                        percent=98.0,
                    ),
                ],
            ),
            "2026-03-18T15:42:10.123456",
        ),
        (
            Data(
                cpu=CPUData(per_cpu=[], total=0.0),
                mem=MemoryData(used="0 GB", total="0 GB", percent=0.0),
                disks=[],
            ),
            "0000",
        ),
    ],
)
def test_log_json(mocker, mock_data: Data):
    mock_dump: MagicMock = mocker.patch("src.logger.json.dump")
    mock_file = mocker.mock_open()
    mocker.patch("src.logger.open", mock_file)

    logger = Logger("/")
    logger._log_json(mock_data)
    mock_dump.assert_called_once_with(mock_data, mock_file())


######################
## Integration Test ##
######################


@pytest.mark.parametrize(
    "mock_data,file_name",
    [
        (
            Data(
                cpu=CPUData(per_cpu=[5.0, 30.4, 7.8, 6.7], total=15.2),
                mem=MemoryData(used="20.00 GB", total="40.00 GB", percent=40.0),
                disks=[
                    DiskData(
                        device="/dev/disk1",
                        mountpoint="/",
                        used="1.50 GB",
                        total="8.00 GB",
                        percent=70.0,
                    ),
                    DiskData(
                        device="/dev/disk2",
                        mountpoint="/data",
                        used="0.20 GB",
                        total="18.00 GB",
                        percent=98.0,
                    ),
                ],
            ),
            "123",
        ),
        (
            Data(
                cpu=CPUData(per_cpu=[], total=0.0),
                mem=MemoryData(used="0 GB", total="0 GB", percent=0.0),
                disks=[],
            ),
            "1",
        ),
    ],
)
def test_comp(mocker, mock_data: Data, file_name):
    path = f"log/test{file_name}"
    mock_data_dict: dict = asdict(mock_data)
    logger = Logger(path)
    logger.log(mock_data)

    with open(path, "r") as f:
        d = json.loads(f.readlines()[-1])
        for k, v in d.items():
            if k != "time":
                assert v == mock_data_dict[k]
