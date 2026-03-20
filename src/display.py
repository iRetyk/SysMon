"""
Rendering logic (rich)
"""

from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich.progress import Progress

import time

from src.data_classes import Data, CPUData, MemoryData, DiskData, convert_to_GB


CPU_COLOR_TITLE = "grey11"
DISK_COLOR_TITLE = "grey35"
MEM_COLOR_TITLE = "grey50"

GOOD_COLOR = "green"
OK_COLOR = "yellow"
BAD_COLOR = "red"


class Display:
    """Render system metrics in a live terminal view using rich."""

    def __init__(self, interval: float) -> None:
        """Create a Display widget instance.

        Args:
            interval: Refresh interval in seconds for the progress/loading animation.
        """
        self.__interval = interval
        self.__table: Table = Table()

    def ready(self):
        """Initialize the live display before updating metrics."""
        self.__live = Live(refresh_per_second=5)
        self.__live.start()

    def shutdown(self):
        """Stop the live display if it is running."""
        try:
            self.__live.stop()
        except Exception:
            pass

    def update(self, data: Data):
        """Update the live display with freshly collected data."""
        self._build_table(data)
        self.__live.update(self.__table)

    def load_progress(self):
        """Show a loading progress bar for the startup phase."""
        with Progress() as p:
            task = p.add_task("Loading...", total=50)
            for _ in range(50):
                time.sleep(self.__interval / 50.0)
                p.update(task, advance=1)

    def _build_table(self, data: Data):
        """Build the main metrics table from the current data snapshot."""
        table = Table(title="System Metrics")
        table.add_column(Align(f"[{CPU_COLOR_TITLE}]CPU", "center"))
        table.add_column(Align(f"[{DISK_COLOR_TITLE}]Disk", "center"))
        table.add_column(Align(f"[{MEM_COLOR_TITLE}]Memory", "center"))
        table.add_row(
            self._build_cpu_table(data.cpu),
            self._build_disk_table(data.disks),
            self._build_memory_table(data.mem),
        )

        ### Alternative design ###
        # table.add_row("CPU",self.build_cpu_table())
        # table.add_row("Memory",self.build_memory_table())
        # table.add_row("Disk",self.build_disk_table())

        self.__table = table

    def _build_cpu_table(self, data: CPUData) -> Table:
        """Build a table for CPU usage metrics.

        Args:
            data: CPUData instance with per-core and total CPU usage.

        Returns:
            Table with one row per core and a total row.
        """
        table = Table()
        table.add_column("Metric")
        table.add_column("Value")

        cpu_list, total = data.per_cpu, data.total

        cpu_list_colored = self._color_cpu(cpu_list)
        total_colored = self._color_cpu([total])[0]

        for i, cpu in enumerate(cpu_list_colored):
            table.add_row(f"CPU {i + 1}", cpu)
        table.add_row("Total", total_colored)

        return table

    def _build_memory_table(self, data: MemoryData) -> Table:
        """Build a table for memory usage metrics."""
        table = Table()
        table.add_column("Metric")
        table.add_column("Value")
        mem_stats = data

        mem_stats_colored_list = self._color_mem(data)

        mem_stats_colored = {
            k: v for k, v in zip(mem_stats.to_dict().keys(), mem_stats_colored_list)
        }

        for key in mem_stats_colored.keys():
            table.add_row(key, mem_stats_colored[key])

        return table

    def _build_disk_table(self, data: list[DiskData]) -> Table:
        """Build table(s) for disk usage metrics across partitions."""
        disks = data

        tables: list[Table] = []

        for disk in disks:
            disk_table = Table(title=disk.device)  # type:ignore
            disk_table.add_column("Metric")
            disk_table.add_column("Value")

            colored_disk_list: list[str] = self._color_disk(disk)

            colored_disk = {
                k: v for k, v in zip(disk.to_dict().keys(), colored_disk_list)
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

    def _color_cpu(self, values: list[float]) -> list[str]:
        """Colorize CPU values according to defined thresholds."""
        to_return: list[str] = []

        for val in values:
            to_return.append(self._color_according_to_range(val, 15.0, 60.0))

        return to_return

    def _color_mem(self, data: MemoryData) -> list[str]:
        """Colorize memory values and return colored values for display."""
        to_return: list[str] = []

        to_return.append(
            self._color_according_to_range(
                data.used, 10 * (1024**3), 100 * (1024**3), format="GB"
            )
        )
        to_return.append(
            self._color_according_to_range(
                data.total, 10 * (1024**3), 100 * (1024**3), format="GB"
            )
        )
        to_return.append(self._color_according_to_range(data.percent, 20.0, 85.0, True))

        return to_return

    def _color_disk(self, data: DiskData) -> list[str]:
        """Colorize disk values and return output list for display."""
        to_return: list[str] = [data.mountpoint, data.device]
        to_return.append(
            self._color_according_to_range(
                data.used, 10 * (1024**3), 100 * (1024**3), format="GB"
            )
        )
        to_return.append(
            self._color_according_to_range(
                data.total, 10 * (1024**3), 100 * (1024**3), format="GB"
            )
        )
        to_return.append(self._color_according_to_range(data.percent, 20.0, 85.0, True))

        return to_return

    def _color_according_to_range(
        self, val: float, min: float, max: float, reverse=False, format: str = ""
    ) -> str:
        """
        return formatted string according to the value.

        good color if val < min
        ok color if min < val < max
        bad color if max < val

        reverse if the bigger the value the better.

        """

        format_val = convert_to_GB(val) if format else val

        if reverse:
            bad_color, good_color = GOOD_COLOR, BAD_COLOR
        else:
            good_color, bad_color = GOOD_COLOR, BAD_COLOR

        if val > max:
            return f"[{bad_color}]{format_val}"
        elif val < min:
            return f"[{good_color}]{format_val}"
        else:
            return f"[{OK_COLOR}]{format_val}"


if __name__ == "__main__":
    print(
        "Warning, you are trying to run collector.py, that shouldn't be run directly. Are you sure you want to continue this action? (Y/N) (Useful only for dev testing)"
    )
    if "Y" in input():
        # Whatever it is you want to test
        pass
    else:
        print("exiting...")
