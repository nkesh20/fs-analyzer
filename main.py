import argparse
import os
import sys
from analyzer import analyzer

def parse_args():
    parser = argparse.ArgumentParser(
        description="File System Analyzer: Analyze disk usage and file types in a directory."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="Path to the directory to analyze"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=100,  # Default size threshold in MB
        help="Size threshold in MB for large file detection (default: 100MB)"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing directory: {args.directory}")
    results = analyzer.analyze_directory(args.directory)

    print(f"Found {len(results)} files")
    for file in results:
        print(f"File: {file['path']} - Size: {file['size']} bytes - Permissions: {file['permissions']} - Modified: {file['modified']} - Extension: {file['extension']}")
        

if __name__ == "__main__":
    main()
    


