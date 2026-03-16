"""
Collect the metrics displayed to user
"""

import psutil

def get_cpu_usage(interval: float) -> tuple[list[float],float]:
    """
    NOTE: this function sleeps for interval many seconds
    Input: interval (float)
    
    Output: Usage per-core, total (tuple[list[float],float])
    """
    cpu_percent_list = psutil.cpu_percent(interval,percpu=True)
    total_cpu_percent = round(sum(cpu_percent_list) / len(cpu_percent_list), 1) # Average percent rounded to one decimal point
    return cpu_percent_list,total_cpu_percent


def get_memory() -> dict[str,int | float]:
    """
    Input: no input
    
    Output: Memory stats of used, total, percent (dict[str,int | float])
    """
    mem_stats = psutil.virtual_memory()
    total = mem_stats.total # Total 
    available = mem_stats.available # Memory that can be given by the os immediately 
    percent = mem_stats.percent # total - available / total * 100
    used = mem_stats.used # Memory currently in use
    free = mem_stats.free
    return {"used":used, "total":total, "percent":percent}
    

def get_disk():
    """
    Input:
    
    Output: Disk usage (int)
    """
    pass

if __name__ == "__main__":
    print("Warning, you are trying to run collector.py, that shouldn't be run directly. Are you sure you want to continue this action? (Y/N) (Useful only for dev testing)")
    if input() == "Y":
        # print(get_cpu_usage(2))
        print(get_memory())
        # print(get_disk())
    else:
        print("exiting...")