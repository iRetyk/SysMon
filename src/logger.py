"""
File Logging
"""

import json
import datetime
import os
from dataclasses import asdict
from pathlib import Path

from src.data_classes import Data


class Logger:
    """Simple file logger for JSON-formatted metric snapshots."""

    def __init__(self, path: str) -> None:
        """Initialize logger with a destination file path.

        Args:
            path: Path to the log file.
        """
        self.__path = path.replace("\\", "/")

    def log(self, data: Data):
        """Log a Data object by appending a JSON line with timestamp."""
        # Change the order so that time shows first in json
        new_data = {}
        new_data["time"] = datetime.datetime.now().isoformat()
        for k, v in asdict(data).items():
            new_data[k] = v
        # Possibly support more than one file format
        self._log_json(new_data)

    def _log_json(self, data):
        """Write `data` as a newline-delimited JSON object to disk.

        Args:
            data: An object that is JSON serializable (e.g. dict from dataclasses.asdict).
        """
        Path(os.path.dirname(self.__path)).mkdir(parents=True, exist_ok=True)

        with open(self.__path, "a") as f:
            json.dump(data, f)
            f.write("\n")


if __name__ == "__main__":
    print(
        "Warning, you are trying to run collector.py, that shouldn't be run directly. Are you sure you want to continue this action? (Y/N) (Useful only for dev testing)"
    )
    if "Y" in input():
        # Whatever it is you want to test
        pass
    else:
        print("exiting...")
