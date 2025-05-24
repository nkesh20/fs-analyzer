from tabulate import tabulate


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
        if "error" not in file
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


def print_permissions_report(risky_files: list):
    if not risky_files:
        print("No files with unusual permissions found.")
        return

    table_data = []
    for file in risky_files:
        if "error" in file:
            table_data.append(
                [
                    truncate_text(file["path"]),
                    "ERROR",
                    file.get("error", "Unknown error"),
                ]
            )
        else:
            # Join risk reasons list into a comma-separated string
            risk_reasons = ", ".join(file.get("risk_reasons", ["Unknown"]))
            table_data.append(
                [
                    truncate_text(file["path"]),
                    file.get("permissions", "N/A"),
                    risk_reasons,
                ]
            )

    headers = ["Path", "Permissions", "Risk Reasons or Error"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
