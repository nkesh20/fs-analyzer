# File System Analyzer

A command-line tool that analyzes and reports on file system structure, usage, and security on Linux systems.

## Features

- **Directory Traversal**: Recursively scans directories to analyze file structure
- **File Type Categorization**: Classifies files by type (text, image, executable, etc.) using extensions and MIME detection
- **Size Analysis**: Calculates total size usage by file category
- **Security Analysis**: Identifies files with unusual permissions (world-writable, setuid, etc.)
- **Large File Detection**: Finds files above configurable size thresholds
- **Error Handling**: Gracefully handles permission errors and inaccessible files

## Installation

### Option 1: Install with pipx (Recommended)
```bash
pipx install git+https://github.com/nkesh20/fs-analyzer.git
```

### Option 2: Install with pip
```bash
pip install git+https://github.com/nkesh20/fs-analyzer.git
```

### Option 3: Development Installation
```bash
git clone https://github.com/nkesh20/fs-analyzer.git
cd fs-analyzer
pip install -e .
```

## Dependencies

- Python 3.7+
- `tabulate` - For formatted table output
- `python-magic` - For MIME type detection

Dependencies are automatically installed during setup.

## Usage

### Basic Usage

After installation:
```bash
# Analyze current directory
fs-analyzer .

# Analyze specific directory
fs-analyzer /home/user/documents

# Analyze with custom size threshold (50MB)
fs-analyzer /var/log --threshold 50
```

### Development Usage (without installation)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run from source
python -m analyzer.cli .


# Run tests
pip install -r requirements-dev.txt
python -m pytest tests/ # Unit tests
python tests/test_analyzer.py # Integration test on current directory + unit tests
```

### Command Line Options

```bash
fs-analyzer [DIRECTORY] [OPTIONS]
```

**Arguments:**
- `DIRECTORY` - Path to directory to analyze (required)

**Options:**
- `--threshold N` - Size threshold in MB for large file detection (default: 100)
- `--show-permissions` - Include permission analysis in standard output
- `--permissions-only` - Only show files with unusual permissions
- `--help` - Show help message

### Examples

```bash
# Basic analysis of home directory
fs-analyzer /home/user

# Find large files over 50MB
fs-analyzer /var --threshold 50

# Security audit - show only files with risky permissions
fs-analyzer /usr/local --permissions-only

# Full analysis including permissions
fs-analyzer /opt --show-permissions
```

## Sample Output

```
Analyzing directory: /home/user/documents
Found 1,247 files

┌─────────────────────────────────┬──────────────┬─────────────┬─────────────────────┬───────────┬──────────┐
│ Path                            │ Size (bytes) │ Permissions │ Modified            │ Extension │ Category │
├─────────────────────────────────┼──────────────┼─────────────┼─────────────────────┼───────────┼──────────┤
│ ...documents/report.pdf         │ 2,847,392    │ -rw-r--r--  │ 2024-03-15 14:23:01 │ .pdf      │ Document │
│ ...documents/script.py          │ 1,024        │ -rwxr-xr-x  │ 2024-03-16 09:15:32 │ .py       │ Text     │
└─────────────────────────────────┴──────────────┴─────────────┴─────────────────────┴───────────┴──────────┘

Total size by file category:
Text: 15.42 MB
Image: 128.73 MB
Document: 45.21 MB
Other: 2.14 MB

Files larger than 100 MB (3):
- /home/user/documents/video.mp4 (256.78 MB)
- /home/user/documents/backup.tar.gz (145.23 MB)
- /home/user/documents/dataset.csv (112.45 MB)

Files with unusual permissions (2):
┌─────────────────────────────────┬─────────────┬──────────────────────────────────┐
│ Path                            │ Permissions │ Risk Reasons                     │
├─────────────────────────────────┼─────────────┼──────────────────────────────────┤
│ ...documents/temp.txt           │ -rw-rw-rw-  │ World-writable                   │
│ ...documents/admin_tool         │ -rwsr-xr-x  │ Setuid bit set                   │
└─────────────────────────────────┴─────────────┴──────────────────────────────────┘
```

## File Categories

The tool categorizes files into the following types:

- **Text**: `.txt`, `.md`, `.csv`, `.log`, `.json`, `.xml`, `.py`, `.js`, etc.
- **Image**: `.jpg`, `.png`, `.gif`, `.svg`, `.webp`, etc.
- **Video**: `.mp4`, `.avi`, `.mov`, `.mkv`, etc.
- **Audio**: `.mp3`, `.wav`, `.flac`, `.ogg`, etc.
- **Archive**: `.zip`, `.tar`, `.gz`, `.rar`, `.7z`, etc.
- **Executable**: `.exe`, `.bin`, `.sh`, executables without extensions
- **Other**: Files with unrecognized extensions
- **Unknown**: Files without extensions that couldn't be categorized

## Security Checks

The tool identifies files with potentially risky permissions:

- **World-writable files**: Files that can be modified by any user
- **Setuid/Setgid files**: Files that run with elevated privileges
- **Executables writable by group/others**: Scripts or binaries that can be modified by non-owners

## Error Handling

The tool gracefully handles common issues:

- **Permission denied**: Continues analysis, reports inaccessible files
- **Broken symlinks**: Skips and continues
- **Large directories**: Provides progress feedback
- **Invalid paths**: Clear error messages

## Troubleshooting

### python-magic installation issues

On some systems, you may need to install system dependencies:

**Ubuntu/Debian:**
```bash
sudo apt-get install libmagic1
```

**CentOS/RHEL:**
```bash
sudo yum install file-libs
```

**macOS:**
```bash
brew install libmagic
```

### Permission errors

If you encounter permission errors, try:
- Running with appropriate privileges for the target directory
- Using `--permissions-only` to focus on security analysis
- Checking that the target directory exists and is accessible
