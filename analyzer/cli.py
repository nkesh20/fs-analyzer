import argparse
import os
import sys
from analyzer.utils import (
    print_table,
    size_by_category,
    find_large_files,
    print_permissions_report,
)
from analyzer.analyzer import analyze_directory
from analyzer.permissions import report_unusual_permissions


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
    parser.add_argument(
        "--show-permissions",
        action="store_true",
        help="Show permissions of files",
    )
    parser.add_argument(
        "--permissions-only",
        action="store_true",
        help="Only report files with unusual permissions",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing directory: {args.directory}")
    results = analyze_directory(args.directory)

    risky_files = []
    if args.show_permissions or args.permissions_only:
        risky_files = report_unusual_permissions(results)

    if args.permissions_only:
        print(f"Found {len(risky_files)} files with unusual permissions")
        print_permissions_report(risky_files)
        return

    # print all files
    print(f"Found {len(results)} files")
    print_table(results)

    # size by category
    sizes = size_by_category(results)
    print("\nTotal size by file category:")
    for category, total_size in sizes.items():
        print(f"{category}: {total_size / (1024*1024):.2f} MB")

    # large files
    large_files = find_large_files(results, args.threshold)
    print(f"\nFiles larger than {args.threshold} MB ({len(large_files)}):")
    for f in large_files:
        print(f"- {f['path']} ({f['size'] / (1024*1024):.2f} MB)")

    # errors
    errors = [f for f in results if "error" in f]
    if errors:
        print(f"\nErrors encountered ({len(errors)} files):")
        for e in errors:
            print(f"- {e['path']}: {e['error']}")

    if args.show_permissions:
        print(f"\nFiles with unusual permissions ({len(risky_files)}):")
        print_permissions_report(risky_files)


if __name__ == "__main__":
    main()
