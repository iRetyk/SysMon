"""
Argument Parsing
"""

import argparse

import threading

from logger import Logger
from display import Display
from collector import get_cpu_usage, get_memory, get_disk
from data_classes import Data


DATA: Data


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


def get_data(interval: float) -> Data:
    """Collect CPU, memory, and disk metrics and return a `Data` container."""
    # get_cpu_usage sleeps internally so this function sleeps internally
    global DATA
    DATA = Data(get_cpu_usage(interval), get_memory(), get_disk())
    return DATA


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
    
    try:
        t1 = threading.Thread(target=get_data, args=[interval], daemon=True)
        t1.start()
        app.load_progress()
        t1.join()

        data = DATA  # No need to use lock because t1.join was already called
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


if __name__ == "__main__":
    main()
