"""
MC Structure Cleaner
Wraps the tag removal logic using an anvil parser for version >= 1.18
"""

from structurecleaner.remove_tags import remove_tags as remove_tags_old

from pathlib import Path
from typing import Set


# --rewrite code goes here--
def remove_tags(tags: Set[str],
                src: Path, dst: Path, jobs: int, mode: str) -> None:
    """
    Decorator for the real remove_tags, that override anvil parser for
    1.17+ support
    """
    # anvil override logic here
    remove_tags_old(tags, src, dst, jobs, mode)
