"""
Argument Parsing
"""

import argparse
from display import App




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

def main():
    # Project entry point
    args = parse_args()
    interval = max(args.interval, 0.2) # values under 0.2, are rounded to 0.2.
    log_path = args.log
    
    log = log_path is not None
    try:
        app = App(interval)
        app.run()
    except KeyboardInterrupt:
        print("Exiting...")

def debug_main():
    app = App(2)
    app.run()

if __name__ == "__main__":
    debug = False
    if debug:
        debug_main()
    else:
        main()