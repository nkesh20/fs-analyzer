import os
import sys

try:
    import magic
except ImportError:
    print(
        "Error: python-magic is not installed. Please install it using 'pip install python-magic-bin'."
    )
    sys.exit(1)

EXTENSION_MAP = {
    "Text": {
        ".txt",
        ".md",
        ".csv",
        ".log",
        ".json",
        ".xml",
        ".yaml",
        ".yml",
        ".ini",
        ".conf",
    },
    "Image": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
    "Video": {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg"},
    "Archive": {".zip", ".tar", ".gz", ".bz2", ".xz", ".rar", ".7z"},
    "Executable": {".exe", ".bin", ".bat", ".msi", ".run", ".app", ".out"},
}

MIME_CATEGORY_MAP = {
    "text": "Text",
    "image": "Image",
    "video": "Video",
    "audio": "Audio",
    "application/x-executable": "Executable",
    "application/x-sh": "Executable",
    "application/zip": "Archive",
    "application/x-tar": "Archive",
    "application/gzip": "Archive",
}


def categorize_file(path: str) -> str:
    # First, try categorizing by extension
    extension = os.path.splitext(path)[1].lower()
    for category, extensions in EXTENSION_MAP.items():
        if extension in extensions:
            return category

    # Fallback to magic detection if extension isn't helpful
    try:
        mime = magic.from_file(path, mime=True)
        if mime:
            main_type = mime.split("/")[0]
            if mime in MIME_CATEGORY_MAP:
                return MIME_CATEGORY_MAP[mime]
            elif main_type in MIME_CATEGORY_MAP:
                return MIME_CATEGORY_MAP[main_type]
    except Exception as e:
        print(f"[categorize_file] magic failed for {path}: {e}")

    return "Other" if extension else "Unknown"