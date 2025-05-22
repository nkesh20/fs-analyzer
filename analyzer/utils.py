def truncate_text(text, max_length=50):
    return text if len(text) <= max_length else "..." + text[-(max_length - 3) :]


def size_by_category(files: list[dict]) -> dict[str, int]:
    sizes = {}
    for f in files:
        category = f.get("category", "Unknown")
        size = f.get("size", 0)
        sizes[category] = sizes.get(category, 0) + size
    return sizes


def find_large_files(files: list[dict], threshold_mb: int) -> list[dict]:
    threshold_bytes = threshold_mb * 1024 * 1024
    return [f for f in files if f.get("size", 0) > threshold_bytes]
