import argparse
import os
import sys
from tabulate import tabulate
from analyzer.utils import truncate_text
from analyzer.analyzer import analyze_directory


def parse_args():
    parser = argparse.ArgumentParser(
        description="File System Analyzer: Analyze disk usage and file types in a directory."
    )
    parser.add_argument("directory", type=str, help="Path to the directory to analyze")
    parser.add_argument(
        "--threshold",
        type=int,
        default=100,  # Default size threshold in MB
        help="Size threshold in MB for large file detection (default: 100MB)",
    )
    return parser.parse_args()


def print_table(results):
    table_data = [
        [
            truncate_text(file["path"]),
            file["size"],
            file["permissions"],
            file["modified"],
            file["extension"],
            file["category"],
        ]
        for file in results
    ]
    headers = [
        "Path",
        "Size (bytes)",
        "Permissions",
        "Modified",
        "Extension",
        "Category",
    ]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def main():
    args = parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing directory: {args.directory}")
    results = analyze_directory(args.directory)

    print(f"Found {len(results)} files")
    print_table(results)


if __name__ == "__main__":
    main()
