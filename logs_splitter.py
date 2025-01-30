import re
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from attr import dataclass


@dataclass
class Time:
    year: int = datetime.now().year
    month: int = datetime.now().month
    day: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
    second: Optional[int] = None


def parse_log_time(log_line: str) -> Optional[datetime]:
    """Extract timestamp from log line and convert to datetime object."""
    # Assuming log format contains timestamp like "2025-01-20 10:30:45"
    timestamp_pattern = r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}"
    match = re.search(timestamp_pattern, log_line)
    if match:
        timestamp_str = match.group(0)
        return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return None


class LogsSetup:
    def __init__(self, file_path, container_names: List[str]):
        self.log_lines = self._open_file_and_read(file_path)
        self.container_names = container_names
        self.log_map = None

    @staticmethod
    def _open_file_and_read(file_path):
        with open(file_path, "r") as f:
            return f.readlines()

    @staticmethod
    def _convert_time_to_datetime(from_time: Optional[Time] = None, to_time: Optional[Time] = None):
        if from_time is None:
            from_time = Time()
        if to_time is None:
            to_time = Time()

        # Convert Time objects to datetime objects with default values
        from_datetime = datetime(
            year=from_time.year,
            month=from_time.month,
            day=from_time.day or 1,
            hour=from_time.hour or 0,
            minute=from_time.minute or 0,
            second=from_time.second or 0
        )

        to_datetime = datetime(
            year=to_time.year,
            month=to_time.month,
            day=to_time.day or 31,  # Use end of month if day not specified
            hour=to_time.hour or 23,
            minute=to_time.minute or 59,
            second=to_time.second or 59
        )
        return from_datetime, to_datetime

    def _filter_logs_by_time(self, from_time: Optional[Time] = None, to_time: Optional[Time] = None) -> List[str]:
        """Filter logs based on time range."""
        from_datetime, to_datetime = self._convert_time_to_datetime(from_time, to_time)
        for log_map in self.log_map:
            filtered_logs = []
            for line in self.log_lines:
                log_time = parse_log_time(line)
                if log_time and from_datetime <= log_time <= to_datetime:
                    filtered_logs.append(line)

            self.log_map[log_map] = filtered_logs

    def _split_logs_to_files(self):
        log_map = {name: [] for name in self.container_names}
        not_specified_names = set()
        for line in self.log_lines:
            for container_name in self.container_names:
                if line.startswith(container_name):
                    log_map[container_name].append(line)
                else:
                    match = re.match(r"(\S+)\s+\|", line)
                    log_container_name = match.group(1)
                    if log_container_name not in self.container_names and log_container_name not in not_specified_names:
                        not_specified_names.add(log_container_name)
        if len(not_specified_names) > 0:
            print(f"Unspecified container names: {not_specified_names}")
        self.log_map = log_map

    def _save_to_files(self):
        Path("./processed")
        for container_name, log_lines in self.log_map.items():
            with open(f"./processed/{container_name}.log", "w") as f:
                f.writelines(log_lines)


class Logs(LogsSetup):
    def split_logs_to_files_and_save(self):
        self._split_logs_to_files()
        self._save_to_files()

    def filter_logs_to_files_and_save(self, from_time: Optional[Time] = None, to_time: Optional[Time] = None):
        self._split_logs_to_files()
        self._filter_logs_by_time(from_time, to_time)
        self._save_to_files()
