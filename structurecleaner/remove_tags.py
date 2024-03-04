"""
MC Structure Cleaner
Tag removal logic
"""

import time
import os
import itertools as it
import anvil  # type: ignore
from multiprocessing import Pool
from pathlib import Path
from typing import Set, Tuple
from structurecleaner.constants import (
    SEP,
    NEW_DATA_VERSION,
)
from structurecleaner.errors import (
    InvalidRegionFileError,
    InvalidFileNameError,
    EmptyFileError,
)

from structurecleaner.removal_strategies import (
    RemovalStrategy,
    PurgeRemovalStrategy,
    ListRemovalStrategy,
)


def _remove_tags_region_task(args: Tuple[Set[str], Path, Path, str]) -> int:
    """Wrapper for removing tags from a region file"""
    try:
        return _remove_tags_region(*args)
    except (InvalidRegionFileError, InvalidFileNameError, EmptyFileError):
        return 0


def _remove_tags_region(
    removal_strategy: RemovalStrategy, src: Path, dst: Path
) -> int:
    """Remove tags in to_replace from the src region

    Args:
        removal_strategy (RemovalStrategy): The strategy to use (Purge, List)
        src (Path): The source region file
        dst (Path): Where changes are written to

    Raises:
        InvalidRegionFileError: If the file is not a valid region file
        InvalidFileNameError: If the file is not a valid path
        EmptyFileError: If the file is empty
        NotImplementedError: If the file is a newer version than 1.17

    Returns:
        int: The number of times any tag was removed
    """
    start: float = time.perf_counter()
    count: int = 0

    # Check if it's even an .mca file
    print("Checking file:", src)
    if len(str(src)) > 4:
        if str(src)[-1:-5:-1] != "acm.":
            print(f"{src} is not a valid region file.")
            raise InvalidRegionFileError
    else:
        print(f"{src} is not a valid path.")
        raise InvalidFileNameError

    # Check if file isn't empty
    if os.path.getsize(src) == 0:
        print(f"{src} is empty.")
        raise EmptyFileError

    coords = src.name.split(".")
    region = anvil.Region.from_file(str(src.resolve()))
    new_region = anvil.EmptyRegion(int(coords[1]), int(coords[2]))
    removed_tags = set()

    # Check chunks
    for chunk_x, chunk_z in it.product(range(32), repeat=2):
        # Chunk Exists
        if region.chunk_location(chunk_x, chunk_z) != (0, 0):
            data = region.chunk_data(chunk_x, chunk_z)
            data_copy = region.chunk_data(chunk_x, chunk_z)

            if int(data["DataVersion"].value) > NEW_DATA_VERSION:
                raise NotImplementedError("Version 1.18 is not supported yet.")

            if hasattr(data["Level"]["Structures"]["Starts"], "tags"):
                for tag in data["Level"]["Structures"]["Starts"].tags:
                    if removal_strategy.check_tag(tag):
                        del data_copy["Level"]["Structures"]["Starts"][
                            tag.name
                        ]
                        count += 1
                        removed_tags.add(tag.name)

            if hasattr(data["Level"]["Structures"]["References"], "tags"):
                for tag in data["Level"]["Structures"]["References"].tags:
                    if removal_strategy.check_tag(tag):
                        del data_copy["Level"]["Structures"]["References"][
                            tag.name
                        ]
                        count += 1
                        removed_tags.add(tag.name)

            # Add the modified chunk data to the new region
            new_region.add_chunk(anvil.Chunk(data_copy))

    # Save Region
    new_region.save(str((dst / src.name).resolve()))

    end: float = time.perf_counter()
    print(
        f"File {src}: {count} \
        instances of tags removed in {end - start:.3f} s"
    )

    removal_strategy.print_find(removed_tags)

    return count


def remove_tags(
    tags: Set[str], src: Path, dst: Path, jobs: int, mode: str
) -> None:
    """Removes tags from src region files and writes them to dst

    Args:
        tags (Set[str]): Tags to be removed
        src (Path): The source region files
        dst (Path): The destination folder
        jobs (int): Number of processes to use
        mode (str): Purge or remove strategy
    """
    if mode == "purge":
        removal_strategy = PurgeRemovalStrategy()
    else:
        removal_strategy = ListRemovalStrategy(tags)

    with Pool(processes=jobs) as pool:
        start = time.perf_counter()
        data = zip(it.repeat(removal_strategy), src.iterdir(), it.repeat(dst))
        count = sum(pool.map(_remove_tags_region_task, data))
        end = time.perf_counter()

        print(SEP)
        removal_strategy.print_done(count)
        print(f"Took {end - start:.3f} seconds")
