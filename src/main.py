"""
Argument Parsing
"""

import argparse



DEFAULT_PATH = "log/log.json"

def digest_input(from_user: str):
    """
    Args: from_user (str) - the input user gave
    
    Returns: 
    """

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval","-i",
                        type=int
                        ,default = 2.0,
                        help="Specify the interval for the refresh rate in the display, in seconds. [Default - 2]"
                        )

    parser.add_argument("--log","-l",
                        type=str,
                        default = DEFAULT_PATH,
                        help = f"Specify the path for the logs. [Default - ~/log/log.json]"
                        )
    
    return parser.parse_args()

def main():
    # Project entry point
    args = parse_args()



if __name__ == "__main__":
    main()