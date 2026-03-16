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
    
    if not cpu_percent_list: 
        raise RuntimeError("Cores list is empty - psutil has failed for some reason")
    
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
    return {"used": used, "total": total, "percent": percent}
    

def get_disk() -> list[dict]:
    """
    Input: no input
    
    Output: List of every partition info (mountpoint, device, total, used, percent) (list[dict])
    """
    disk_list: list[dict] = []
    
    for disk_par in psutil.disk_partitions():
        usage = psutil.disk_usage(disk_par.mountpoint)

        
        disk_list.append({"mountpoint": disk_par.mountpoint, "device": disk_par.device ,"total": convert_to_GB(usage.total),
                            "used": convert_to_GB(usage.used), "percent": usage.percent})
        
    return disk_list


def convert_to_GB(num: float) -> str:
    return f"{num / 1024**3:.2f}GB"


if __name__ == "__main__":
    print("Warning, you are trying to run collector.py, that shouldn't be run directly. Are you sure you want to continue this action? (Y/N) (Useful only for dev testing)")
    if "Y" in input():
        print(get_cpu_usage(2))
        print(get_memory())
        print(get_disk())
    else:
        print("exiting...")