"""
Rendering logic (rich)
"""

from data_classes import Data, CPUData, MemoryData, DiskData

from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich.progress import Progress

import time
from dataclasses import asdict

CPU_COLOR_TITLE = "grey11"
DISK_COLOR_TITLE = "grey35"
MEM_COLOR_TITLE = "grey50"

GOOD_COLOR = "green"
OK_COLOR = "yellow"
BAD_COLOR = "red"


class Display:
    def __init__(self, interval: float) -> None:
        self.__interval = interval
        self.__table: Table = Table()

    def ready(self):
        self.__live = Live(refresh_per_second=5)
        self.__live.start()

    def shutdown(self):
        try:
            self.__live.stop()
        except Exception:
            pass

    def update(self, data: Data):
        self.build_table(data)
        self.__live.update(self.__table)

    def load_progress(self):
        with Progress() as p:
            task = p.add_task("Loading...", total=50)
            for _ in range(50):
                time.sleep(self.__interval / 50.0)
                p.update(task, advance=1)

    def build_table(self, data: Data):
        table = Table(title="System Metrics")
        table.add_column(Align(f"[{CPU_COLOR_TITLE}]CPU", "center"))
        table.add_column(Align(f"[{DISK_COLOR_TITLE}]Disk", "center"))
        table.add_column(Align(f"[{MEM_COLOR_TITLE}]Memory", "center"))
        table.add_row(
            self.build_cpu_table(data.cpu),
            self.build_disk_table(data.disks),
            self.build_memory_table(data.mem),
        )

        ### Alternative design ###
        # table.add_row("CPU",self.build_cpu_table())
        # table.add_row("Memory",self.build_memory_table())
        # table.add_row("Disk",self.build_disk_table())

        self.__table = table

    def build_cpu_table(self, data: CPUData) -> Table:
        table = Table()
        table.add_column("Metric")
        table.add_column("Value")

        cpu_list, total = data.per_cpu, data.total

        cpu_list_colored = self.color_cpu(cpu_list)
        total_colored = self.color_cpu([total])[0]

        for i, cpu in enumerate(cpu_list_colored):
            table.add_row(f"CPU {i + 1}", cpu)
        table.add_row("Total", total_colored)

        return table

    def build_memory_table(self, data: MemoryData) -> Table:
        table = Table()
        table.add_column("Metric")
        table.add_column("Value")
        mem_stats = data

        mem_stats_colored_list = self.color_mem(data)

        mem_stats_colored = {
            k: v for k, v in zip(asdict(mem_stats).keys(), mem_stats_colored_list)
        }

        for key in mem_stats_colored.keys():
            table.add_row(key, mem_stats_colored[key])

        return table

    def build_disk_table(self, data: list[DiskData]) -> Table:
        disks = data

        tables: list[Table] = []

        for disk in disks:
            disk_table = Table(title=disk.device)  # type:ignore
            disk_table.add_column("Metric")
            disk_table.add_column("Value")

            colored_disk_list: list[str] = self.color_disk(disk)

            colored_disk = {
                k: v for k, v in zip(asdict(disk).keys(), colored_disk_list)
            }

            for k, v in colored_disk.items():
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
            table.add_row(*tables[i : i + 3])
            i += 3

        return table

    def color_cpu(self, values: list[float]) -> list[str]:
        to_return: list[str] = []

        for val in values:
            to_return.append(self.color_according_to_range(val, 15.0, 60.0))

        return to_return

    def color_mem(self, data: MemoryData) -> list[str]:
        to_return: list[str] = []

        used = data.used
        total = data.total
        percent = data.percent

        to_return.append(
            self.color_according_to_range(float(used[:-2]), 1.5, 6.0) + "GB"
        )
        to_return.append(total)
        to_return.append(self.color_according_to_range(percent, 20.0, 85.0, True))

        return to_return

    def color_disk(self, data: DiskData) -> list[str]:
        to_return: list[str] = [data.mountpoint, data.device]

        used = data.used
        total = data.total
        percent = data.percent

        to_return.append(
            self.color_according_to_range(float(used[:-2]), 1.5, 6.0) + "GB"
        )
        to_return.append(total)
        to_return.append(self.color_according_to_range(percent, 20.0, 85.0, True))

        return to_return

    def color_according_to_range(
        self, val: float, min: float, max: float, reverse=False
    ) -> str:
        """
        return formatted string according to the value.

        good color if val < min
        ok color if min < val < max
        bad color if max < val

        reverse if the bigger the value the better.

        """
        if reverse:
            bad_color, good_color = GOOD_COLOR, BAD_COLOR
        else:
            good_color, bad_color = GOOD_COLOR, BAD_COLOR

        if val > max:
            return f"[{bad_color}]{val}"
        elif val < min:
            return f"[{good_color}]{val}"
        else:
            return f"[{OK_COLOR}]{val}"
