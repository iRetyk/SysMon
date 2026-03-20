"""
Argument Parsing
"""

import argparse

import threading
import pickle
import os

from src.logger import Logger
from src.display import Display
from src.collector import get_cpu_usage, get_memory, get_disk
from src.data_classes import Data


def parse_args():
    """Parse and return command-line arguments for the SysMon app."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--interval",
        "-i",
        type=float,
        default=2.0,
        help="Specify the interval for the refresh rate in the display, in seconds. [Default - 2, values below 0.2 will be automatically rounded to 0.2]",
    )

    parser.add_argument(
        "--log", "-l", type=str, help="Specify the path for the logs. [Optional]"
    )

    return parser.parse_args()


def get_data(interval: float, save_to_file: bool = False, file_path: str = "") -> Data:
    """Collect CPU, memory, and disk metrics and return a `Data` container."""
    # get_cpu_usage sleeps internally so this function sleeps internally
    data = Data(get_cpu_usage(interval), get_memory(), get_disk())

    if save_to_file:
        with open(file_path, "wb") as f:
            pickle.dump(data, f)

    return data


def main():
    """Run the interactive display app and optional logger until user stops it."""
    # Project entry point
    args = parse_args()
    interval = max(args.interval, 0.2)  # values under 0.2, are rounded to 0.2.
    log_path = args.log
    log = log_path is not None

    app = Display(interval)
    if log:
        logger = Logger(log_path)

    data_file: str = "data.json"

    try:
        t1 = threading.Thread(
            target=get_data,
            args=[interval, True, data_file],
            daemon=True,
        )
        t1.start()
        app.load_progress()
        t1.join()

        with open(
            data_file, "rb"
        ) as f:  # No need to use lock because t1.join was already called
            data = pickle.load(f)
        os.remove(data_file)
        app.ready()

        # Main loop
        while True:
            if log:
                logger.log(data)  # type:ignore
            app.update(data)
            data = get_data(interval)  # This sleep internally
    except KeyboardInterrupt:
        app.shutdown()
        print("Exiting cleanly...")
    finally:
        app.shutdown()
        if os.path.exists(data_file):
            os.remove(data_file)


if __name__ == "__main__":
    main()
