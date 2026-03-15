# SysMon – System Monitoring CLI Tool

**Language:** Python  

---

## Overview

Build a command-line tool that tracks CPU, memory, and disk usage in real time. The tool should display live metrics in the terminal with a clean, colored interface, log historical data to a file, and optionally generate daily summary reports.

This project tests your ability to work with system-level APIs, handle periodic I/O, structure a CLI application, and write testable Python code.


## What You're Building

A terminal application called `sysmon` that:

1. **Reads system metrics** — CPU usage (per-core and aggregate), memory (used/total/percent), and disk usage (per-partition) at a configurable polling interval.
2. **Displays live stats** — Renders a continuously-updating terminal dashboard with color-coded indicators (green/yellow/red based on thresholds).
3. **Logs to file** — Appends timestamped readings to a structured log file (CSV or JSON).
4. **Generates reports** *(stretch goal)* — Produces a daily summary with averages, peaks, and any threshold breaches.


## Requirements

### Core (must-have)

- Poll CPU, memory, and disk metrics using `psutil`.
- Print a live-updating terminal display using `rich`. The display should refresh in place (no scrolling wall of text).
- Accept a `--interval` flag to set the polling frequency (default: 2 seconds).
- Accept a `--log` flag to specify a log file path. When set, append each reading as a CSV or JSON line.
- Graceful shutdown on `Ctrl+C` — flush the log and print a clean exit message.

### Extended (pick at least one)

- **Threshold alerts:** Accept `--cpu-warn` and `--mem-warn` flags. When a metric exceeds the threshold, change its color to red and optionally trigger a desktop notification.
- **Daily report:** A `sysmon report --date 2026-03-11` subcommand that reads a log file and prints min/avg/max for each metric on that day.
- **Network monitoring:** Add upload/download speed tracking to the dashboard.
- **Export formats:** Support `--format csv` or `--format json` for the log output.


## Repo Structure

```
sysmon/
├── README.md
├── .gitignore
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── main.py          # Entry point, CLI argument parsing
│   ├── collector.py     # Functions that gather CPU/mem/disk metrics
│   ├── display.py       # Terminal rendering logic (rich tables/panels)
│   ├── logger.py        # File logging (CSV/JSON line writer)
│   └── report.py        # (stretch) Daily report generator
├── tests/
│   ├── test_collector.py
│   ├── test_logger.py
│   └── test_report.py
└── docs/
    └── design.md         # Your architecture notes and decisions
```


## Technical Guidance

### System metrics with `psutil`

`psutil` is a cross-platform library for retrieving CPU, memory, disk, and network data. Key functions you'll need:

- `psutil.cpu_percent(interval, percpu)` — returns CPU utilization as a percentage.
- `psutil.virtual_memory()` — returns a named tuple with `total`, `used`, `available`, `percent`.
- `psutil.disk_usage('/')` — returns `total`, `used`, `free`, `percent` for a given mount point.
- `psutil.disk_partitions()` — lists all mounted partitions.

Keep your collector module thin: each function should return a plain dict or dataclass, not print anything. This makes testing straightforward.

### Terminal UI with `rich`

`rich` gives you colored text, tables, panels, progress bars, and a `Live` context manager that redraws content in place. A basic live dashboard looks like:

```python
from rich.live import Live
from rich.table import Table
import time

with Live(refresh_per_second=1) as live:
    while True:
        table = Table(title="System Metrics")
        table.add_column("Metric")
        table.add_column("Value")
        # ... populate with data from collector ...
        live.update(table)
        time.sleep(2)
```

Use `rich.console.Console` for one-off styled output (reports, error messages).

### Testing

Use `pytest`. For the collector module, you can mock `psutil` calls to return known values and verify your functions shape the data correctly. For the logger, write to a temp file and assert the contents. Avoid tests that depend on actual system state — they'll be flaky across machines.


## What We're Looking For

- **Clean separation of concerns** — collecting, displaying, and logging should be independent modules that don't know about each other's internals.
- **Sensible error handling** — what happens if a disk partition is unmounted mid-run? If the log file path is invalid?
- **Readable code** — clear naming, docstrings on public functions, no 200-line god functions.
- **Working tests** — at least the collector and logger modules should have meaningful test coverage.
- **A README that helps someone run your tool** — install steps, usage examples, a screenshot or gif of the live display.


## Reference & Learning

| Topic | Resource |
|---|---|
| psutil API | [psutil docs](https://psutil.readthedocs.io/) · [GitHub repo](https://github.com/giampaolo/psutil) |
| Terminal UI | [Rich docs](https://rich.readthedocs.io/en/latest/introduction.html) · [GitHub repo](https://github.com/Textualize/rich) |
| Testing | [pytest — Getting Started](https://docs.pytest.org/en/stable/getting-started.html) · [Real Python pytest tutorial](https://realpython.com/pytest-python-testing/) |
| CLI argument parsing | [argparse docs](https://docs.python.org/3/library/argparse.html) |
| Project packaging | [Python Packaging Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/) |
