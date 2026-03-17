"""
Rendering logic (rich)
"""



from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich.panel import Panel
from rich.progress import Progress

import time
import threading


CPU_COLOR_TITLE = "red1"
DISK_COLOR_TITLE  = "orange1"
MEM_COLOR_TITLE = "yellow1"

CPU_COLOR = "red3"
DISK_COLOR  = "orange3"
MEM_COLOR = "yellow3"

class Display:
    def __init__(self,interval: float) -> None:
        self.__interval = interval
        self.__table: Table = Table()


    def ready(self):
        self.__live = Live(refresh_per_second=1)
        self.__live.start()
    
    
    def shutdown(self):
        try:
            self.__live.stop()
        except:
            pass
    
    def update(self, data: dict):
        self.build_table(data)
        self.__live.update(self.__table)
        

    def load_progress(self):
        with Progress() as p:
            task = p.add_task("Loading...",total=50)
            for _ in range(50):
                time.sleep(self.__interval / 50.0)
                p.update(task, advance=1)



    
    
    def build_table(self, data: dict):
        table = Table(title="System Metrics")
        table.add_column(Align(f"[{CPU_COLOR_TITLE}]CPU","center"))
        table.add_column(Align(f"[{DISK_COLOR_TITLE}]Disk","center"))
        table.add_column(Align(f"[{MEM_COLOR_TITLE}]Memory","center"))
        table.add_row(Panel(self.build_cpu_table(data["cpu"]),style=CPU_COLOR),
                        Panel(self.build_disk_table(data["disk"]),style=DISK_COLOR),
                        Panel(self.build_memory_table(data["mem"]),style=MEM_COLOR))
        
        ### Alternative design ###
        # table.add_row("CPU",self.build_cpu_table())
        # table.add_row("Memory",self.build_memory_table())
        # table.add_row("Disk",self.build_disk_table())

        self.__table = table
    
    def build_cpu_table(self,data:tuple[list[float],float]) -> Table:
        table = Table()
        table.add_column("Metric")
        table.add_column("Value")
        
        cpu_list, total = data
        for i, cpu in enumerate(cpu_list):
            table.add_row(f"CPU {i + 1}",str(cpu))
        table.add_row("Total", str(total))
        
        return table

    def build_memory_table(self,data) -> Table:
        table = Table()
        table.add_column("Metric")
        table.add_column("Value")
        mem_stats = data
        
        for key in mem_stats.keys():
            table.add_row(key, str(mem_stats[key]))
            
        return table

    
    def build_disk_table(self,data) -> Table:
        
        disks = data
        
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

    



