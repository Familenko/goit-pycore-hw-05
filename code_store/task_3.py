import sys
import os
from collections import Counter


def parse_log_line(line: str) -> dict:
    """
    This function parses a log line into a dictionary with date, time, level, and message.
    """
    parts = line.strip().split()
    return {
        'date': parts[0], 
        'time': parts[1], 
        'level': parts[2], 
        'message': ' '.join(parts[3:])
        } if len(parts) >= 4 else {}


def load_logs(file_path: str) -> list:
    """
    This function loads logs from a file.
    """
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                log_entry = parse_log_line(line)
                if log_entry:
                    logs.append(log_entry)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit()
    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    This function filters logs by level.
    """
    return filter(lambda log: log['level'] == level, logs)


def count_logs_by_level(logs: list) -> dict:
    """
    This function counts logs by level.
    """
    levels = [log['level'] for log in logs]
    return Counter(levels)


def display_log_counts(counts: dict) -> None:
    """
    This function displays log counts in a formatted table.
    """
    print("Рівень логування | Кількість")
    print("-" * 32)
    for level, count in counts.items():
        print(f"{level:<16} | {count:>8}")


def main():
    """
    Main function to run the log analyzer.
    """
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <log_file> [<log_level>]")
        sys.exit()

    log_file = sys.argv[1]
    log_level = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.isfile(log_file):
        print(f"Error: File {log_file} does not exist.")
        sys.exit()

    logs = load_logs(log_file)

    if log_level:
        logs = filter_logs_by_level(logs, log_level)
        for log in logs:
            print(log)
    else:
        counts = count_logs_by_level(logs)
        display_log_counts(counts)

if __name__ == "__main__":
    main()
