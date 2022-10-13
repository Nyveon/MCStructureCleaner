"""
MC Structure Cleaner
Helper function for tests
"""

from pathlib import Path


def to_file_list(path: Path | str) -> list:
    """Return a list of all files in path"""
    if isinstance(path, str):
        path = Path(path)
    return list(path.glob("*"))


def to_file_set(path: Path | str) -> set:
    """Return a set of all files in path"""
    if isinstance(path, str):
        path = Path(path)
    return set(path.glob("*"))
