"""
Rendering logic (rich)
"""

from collector import get_cpu_usage,get_memory,get_disk

from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich.panel import Panel
import time

CPU_COLOR_TITLE = "red1"
DISK_COLOR_TITLE  = "orange1"
MEM_COLOR_TITLE = "yellow1"

CPU_COLOR = "red3"
DISK_COLOR  = "orange3"
MEM_COLOR = "yellow3"

class App:
    def __init__(self,interval: int) -> None:
        self.__interval = interval

    
    def run(self):
        with Live(refresh_per_second=1) as live:
            while True:
                # ... populate with data from collector ...
                live.update(self.build_table())

    
    def build_table(self) -> Table:
        table = Table(title="System Metrics")
        table.add_column(Align(f"[{CPU_COLOR_TITLE}]CPU","center"))
        table.add_column(Align(f"[{DISK_COLOR_TITLE}]Disk","center"))
        table.add_column(Align(f"[{MEM_COLOR_TITLE}]Memory","center"))
        table.add_row(Panel(self.build_cpu_table(),style=CPU_COLOR),
                        Panel(self.build_disk_table(),style=DISK_COLOR),
                        Panel(self.build_memory_table(),style=MEM_COLOR))
        
        ### Alternative design ###
        # table.add_row("CPU",self.build_cpu_table())
        # table.add_row("Memory",self.build_memory_table())
        # table.add_row("Disk",self.build_disk_table())

        return table
    
    def build_cpu_table(self) -> Table:
        table = Table()
        table.add_column("Metric")
        table.add_column("Value")
        
        cpu_list, total = get_cpu_usage(self.__interval) ## Reminder - this functions sleeps for interval many seconds
        for i, cpu in enumerate(cpu_list):
            table.add_row(f"CPU {i + 1}",str(cpu))
        table.add_row("Total", str(total))
        
        return table

    def build_memory_table(self) -> Table:
        table = Table()
        table.add_column("Metric")
        table.add_column("Value")
        mem_stats = get_memory()
        
        for key in mem_stats.keys():
            table.add_row(key, str(mem_stats[key]))
            
        return table

    
    def build_disk_table(self) -> Table:
        
        disks = get_disk()
        
        tables: list[Table] = []
        
        for disk in disks:
            disk_table = Table(title=disk["device"]) #type:ignore
            disk_table.add_column("Metric")
            disk_table.add_column("Value")
            for k,v in disk.items():
                if k != "device":
                    disk_table.add_row(k, str(v))
            tables.append(disk_table)
        
        
        # After constructing the table for each disk, Organize it neatly in rows of 3 for readability
        """
        0  1  2 
        3  4  5 
        6  7
        
        """
        
        table = Table(show_header=False)
        i = 0
        while i < len(tables):
            table.add_row(*tables[i:i+3])
            i += 3
        
        return table

    



