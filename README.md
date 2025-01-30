# Log Splitter

A Python utility for splitting and filtering container logs based on timestamps and container names. This tool helps manage and analyze log files by separating them into individual files per container and allowing time-based filtering.

## Features

- Split combined container logs into separate files by container name
- Filter logs by time range
- Automatic detection of unspecified container names
- Flexible time range specification with sensible defaults

## Installation

1. Clone the repository
2. Install the required dependency:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from logs_splitter import Logs, Time

# Initialize with log file path and container names
logs = Logs(
    filepath="./log_to_split.log",
    container_names=["nginx-1", "shortener-1", "redis-1"]
)

# Split logs into separate files (one per container)
logs.split_logs_to_files_and_save()
```

### Filtering by Time

```python
from logs_splitter import Logs, Time

logs = Logs("./log_to_split.log", ["nginx-1", "shortener-1", "redis-1"])

# Filter logs for specific time range
from_time = Time(day=30, hour=3)  # This year, this month, day 30 at 3:00
to_time = Time(day=30)            # This year, this month, day 30 at 23:59:59

logs.filter_logs_to_files_and_save(from_time, to_time)
```

## Time Specification

The `Time` class allows flexible specification of time ranges:

```python
# All fields are optional and default to current year/month
Time(
    year=2025,          # Optional: defaults to current year
    month=1,           # Optional: defaults to current month
    day=30,            # Optional: defaults to 1 for start time, 31 for end time
    hour=3,            # Optional: defaults to 0 for start time, 23 for end time
    minute=30,         # Optional: defaults to 0 for start time, 59 for end time
    second=45          # Optional: defaults to 0 for start time, 59 for end time
)
```

## Log Format

The utility expects logs with timestamps in the format:
```
CONTAINER_NAME | YYYY-MM-DD HH:MM:SS [Additional log content]
```

Example:
```
nginx-1 | 2025-01-30 03:45:22 [INFO] Handling request...
```

## Output

- Processed logs are saved in the `./processed` directory
- Each container's logs are saved in a separate file named `{container_name}.log`
- If logs are found for containers not specified in `container_names`, their names will be printed to stdout

## Requirements

- Python 3.6+
- attrs==25.1.0

## File Structure

```
.
├── README.md
├── requirements.txt
├── logs_splitter.py
└── main.py
```