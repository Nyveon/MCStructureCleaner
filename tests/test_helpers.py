"""
MC Structure Cleaner
Helper function for tests
"""

from pathlib import Path


def to_file_set(path: Path | str) -> set:
    """Return a set of all files in path"""
    if isinstance(path, str):
        path = Path(path)
    return set(path.glob("*"))
