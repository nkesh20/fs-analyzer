import os
import stat
from datetime import datetime
from analyzer.file_types import categorize_file

def analyze_directory(path: str) -> list[dict]:
    """
        Analyze the given directory and return a list of file information.
    """
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            info = get_file_info(full_path)
            files.append(info)
    return files



def get_file_info(path: str) -> dict:
    """
        Get file information from the given path.
    """
    try:
        stat_info = os.stat(path)
        return {
            "path": path,
            "size": stat_info.st_size,
            "permissions": stat.filemode(stat_info.st_mode),
            "modified": datetime.fromtimestamp(stat_info.st_mtime),
            "extension": os.path.splitext(path)[1].lower(),
            "category": categorize_file(os.path.splitext(path)[1])
        }
    except Exception as e:
        return {
            "path": path,
            "error": str(e)
        }
