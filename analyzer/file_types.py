EXTENSION_MAP = {
    "Text": {".txt", ".md", ".csv", ".log", ".json", ".xml", ".yaml", ".yml", ".ini", ".conf"},
    "Image": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"},
    "Video": {".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg"},
    "Archive": {".zip", ".tar", ".gz", ".bz2", ".xz", ".rar", ".7z"},
    "Executable": {".exe", ".bin", ".sh", ".bat", ".msi", ".run", ".app", ".out"},
}

def categorize_file(extension: str) -> str:
    extension = extension.lower()
    for category, extensions in EXTENSION_MAP.items():
        if extension in extensions:
            return category
    return "Other" if extension else "Unknown"