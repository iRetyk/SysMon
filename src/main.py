"""
Argument Parsing
"""

import argparse

import threading
import traceback

from logger import Logger
from display import Display
from collector import get_cpu_usage,get_memory,get_disk

DATA = {}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval","-i",
                        type=float
                        ,default = 2.0,
                        help="Specify the interval for the refresh rate in the display, in seconds. [Default - 2, values below 0.2 will be automatically rounded to 0.2]"
                        )

    parser.add_argument("--log","-l",
                        type=str,
                        help = f"Specify the path for the logs. [Optional]"
                        )
    
    return parser.parse_args()


def get_data(interval: float) -> dict:
    """
    Returns a dict with all the data, in this format:
    
    {"cpu": <cpu_data>, "mem":<mem_data>, "disk":<disk_data>}
        cpu_data: (<per_cpu_percent>,<total>)
            per_cpu_percent: list[float]
            total: float
        mem_data: {"used":<used>,"total":<total>,"percent":<percent>}
            used: str
            total: str
            percent: float
        disk_data: [<disk_dict0>,<disk_dict1>...]
            disk_dict: {"mountpoint":<mountpoint>, "device":<device>, "used":<used>,"total":<total>,"percent":<percent>}
                mountpoint: str
                device : str
                used: str
                total: str
                percent: float
    """
    
    # get_cpu_usage sleeps internally so this function sleeps internally
    global DATA
    DATA = {"cpu":get_cpu_usage(interval),"mem":get_memory(),"disk":get_disk()}
    return DATA

def main():
    # Project entry point
    args = parse_args()
    interval = max(args.interval, 0.2) # values under 0.2, are rounded to 0.2.
    log_path = args.log
    log = log_path is not None
    
    app = Display(interval)
    if log:
        logger = Logger(log_path)
    t1 = threading.Thread(target=get_data,args=[interval],daemon=True)
    t1.start()
    app.load_progress()
    t1.join()
        
    data = DATA # No need to use lock because t1.join was already called
    app.ready()
    
    # Main loop
    try:
        while True:
            if log:
                try:
                    logger.log(data) #type:ignore
                except Exception as e:
                    traceback.print_exc()
                    print("An error occurred when trying to log. Will continue without logging")
                    log = False
            
            app.update(data)
            data = get_data(interval) # This sleep internally

    except KeyboardInterrupt:
        app.shutdown()
        print("Exiting cleanly...")
    finally:
        app.shutdown()


def debug_main():
    data = get_data(2)
    logger = Logger("../log/json_test.json")
    logger.log(data)
    
    
if __name__ == "__main__":
    debug = False
    if debug:
        debug_main()
    else:
        main()