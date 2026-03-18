from src import Logger
from unittest.mock import MagicMock
import pytest


##############
## Test log ##
##############


@pytest.mark.parametrize(
    "mock_data,mock_time",
    [
        (
            {
                "cpu": ([5.0, 30.4, 7.8, 6.7], 15.2),
                "mem": {
                    "used": 20 * (1024**3),
                    "total": 40 * (1024**3),
                    "percent": 40.0,
                },
                "disk": [
                    {"used": 1.5 * (1024**3), "total": 8 * (1024**3), "percent": 70.0},
                    {"used": 0.2 * (1024**3), "total": 18 * (1024**3), "percent": 98.0},
                ],
            },
            "2026-03-18T15:42:10.123456",
        ),
        ({"1": 1, "2": 2, "3": 4}, "0000"),
        ({"AAAA": 80}, "123-456"),
    ],
)
def test_log(mocker, mock_data, mock_time):
    # mock all function calls inside Logger.log
    mock_dt = mocker.patch("src.logger.datetime.datetime")
    mock_dt.now.return_value.isoformat.return_value = mock_time
    mock_log_json: MagicMock = mocker.patch("src.logger.Logger.log_json")

    logger = Logger("/")

    logger.log(mock_data)

    # Making a hard copy is necessary - If making shallow copy or using the same object the test doesn't detect some failures.
    mock_data_copy = {k: v for k, v in mock_data.items()}
    mock_data_copy["time"] = mock_time

    mock_log_json.assert_called_once_with(mock_data_copy)


###################
## Test log_json ##
###################


@pytest.mark.parametrize(
    "mock_data", ["AAA", [{"ABC": 123, "@@": 22}, 14, None, [None, 15.5, [None]]]]
)
def test_log_json(mocker, mock_data):
    mock_dump: MagicMock = mocker.patch("src.logger.json.dump")
    mock_file = mocker.mock_open()
    mocker.patch("src.logger.open", mock_file)

    logger = Logger("/")

    logger.log_json(mock_data)

    mock_dump.assert_called_once_with(mock_data, mock_file())


######################
## Integration Test ##
######################


@pytest.mark.parametrize(
    "mock_data", ["AAA", [{"ABC": 123, "@@": 22}, 14, None, [None, 15.5, [None]]]]
)
def comp_test(mocker, mock_data):
    path = "/log/test"
    logger = Logger(path)

    logger.log(mock_data)
