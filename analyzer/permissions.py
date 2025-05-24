import os
import stat


def get_permission_risks(mode: int) -> list[str]:
    """
    Return a list of reasons why the permission is risky.
    Empty list means no risks.
    """
    reasons = []

    # World-writable
    if mode & stat.S_IWOTH:
        reasons.append("World-writable")

    # Executable and writable by group or others
    exec_any = mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    write_group_others = mode & (stat.S_IWGRP | stat.S_IWOTH)
    if exec_any and write_group_others:
        reasons.append("Executable and writable by group/others")

    # Setuid or Setgid
    if mode & stat.S_ISUID:
        reasons.append("Setuid bit set")
    if mode & stat.S_ISGID:
        reasons.append("Setgid bit set")

    return reasons


def report_unusual_permissions(files: list[dict]) -> list[dict]:
    """
    Return a list of files with unusual (risky) permissions,
    each including a 'risk_reasons' list.
    """
    risky = []
    for file in files:
        if "error" in file:
            continue
        try:
            mode = os.stat(file["path"]).st_mode
            risks = get_permission_risks(mode)
            if risks:
                # Add risk reasons to the file info
                file_with_risks = file.copy()
                file_with_risks["risk_reasons"] = risks
                risky.append(file_with_risks)
        except Exception as e:
            risky.append({"path": file["path"], "error": str(e)})
    return risky
