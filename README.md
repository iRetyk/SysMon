# SysMon

SysMon is a small command-line utility that monitors system data in realtime, including:

- CPU usage (per core + total)
- Memory usage
- Disk usage (across mounted partitions)

## Features

- Live colored terminal dashboard (rich-based display)
- Optional JSON line logging for later analysis
- Cross-platform basic data via `psutil`

## Install

1. Clone repository:

```bash
git clone https://github.com/<iRetyk>/SysMon.git
cd SysMon
```

2. (Optinal but recommend) Create and activate a Python environment:

```bash
python -m venv .venv
source venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -U pip
pip install -e .
```

4. (Optional - Not for developers) To install without editable mode:

```bash
pip install .
```

## Usage

Run the app directly:

```bash
python -m src.main
```

You can also run the module path explicitly from project root:

```bash
python src/main.py
```

### CLI options

- `--interval`, `-i` : refresh interval in seconds for metric updates (default `2.0`, min `0.2` enforced)
- `--log`, `-l` : path for JSON logfile output

Example:

```bash
python -m src.main --interval 1.0 --log logs/sysmon.json
```

## Output

- Interactive terminal dashboard via `rich`
- Log file format is JSON lines (one object per line), containing `time`, `cpu`, `mem`, `disks`.

## Testing

Run tests with pytest:

```bash
pytest -q
```

## Documentation

System design and architecture details are maintained in `docs/design.md`.

