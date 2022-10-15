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
from structurecleaner.constants import VANILLA_STRUCTURES, SEP
from structurecleaner.errors import (
    InvalidRegionFileError, InvalidFileNameError,
    EmptyFileError,)


def _remove_tags_region_a(args: Tuple[Set[str], Path, Path, str]) -> int:
    """Wrapper for removing tags from a region file"""
    return _remove_tags_region(*args)


def _remove_tags_region(to_replace: Set[str], src: Path,
                        dst: Path, mode: str) -> int:
    """Remove tags in to_replace from the src region
    Write changes to dst/src.name"""
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

    # Lambda function for checking if a tag is valid
    if mode == "purge":
        def check_tag(_tag):
            return _tag.name.lower() not in VANILLA_STRUCTURES
    else:
        def check_tag(_tag):
            return _tag.name in to_replace

    # Check chunks
    for chunk_x, chunk_z in it.product(range(32), repeat=2):
        # Chunk Exists
        if region.chunk_location(chunk_x, chunk_z) != (0, 0):
            data = region.chunk_data(chunk_x, chunk_z)
            data_copy = region.chunk_data(chunk_x, chunk_z)

            if hasattr(data["Level"]["Structures"]["Starts"], 'tags'):
                for tag in data["Level"]["Structures"]["Starts"].tags:
                    if check_tag(tag):
                        del data_copy["Level"][
                            "Structures"]["Starts"][tag.name]
                        count += 1
                        removed_tags.add(tag.name)

            if hasattr(data["Level"]["Structures"]["References"], 'tags'):
                for tag in data["Level"]["Structures"]["References"].tags:
                    if check_tag(tag):
                        del data_copy["Level"][
                            "Structures"]["References"][tag.name]
                        count += 1
                        removed_tags.add(tag.name)

            # Add the modified chunk data to the new region
            new_region.add_chunk(anvil.Chunk(data_copy))

    # Save Region
    new_region.save(str((dst / src.name).resolve()))

    end: float = time.perf_counter()
    print(f"File {src}: {count} \
        instances of tags removed in {end - start:.3f} s")

    # Output for purge mode (removed non vanilla tags per file)
    if mode == "purge" and len(removed_tags) != 0:
        print(f"Non-vanilla tags found:\n{removed_tags}\nSEP")

    return count


def remove_tags(tags: Set[str],
                src: Path, dst: Path, jobs: int, mode: str) -> None:
    """Removes tags from src region files and writes them to dst"""
    with Pool(processes=jobs) as pool:
        start = time.perf_counter()
        data = zip(it.repeat(tags),
                   src.iterdir(),
                   it.repeat(dst),
                   it.repeat(mode))
        count = sum(pool.map(_remove_tags_region_a, data))
        end = time.perf_counter()

        print(SEP)

        if mode == "purge":
            print(f"Done!\nRemoved {count} instances of non-vanilla tags")
        else:
            print(f"Done!\nRemoved {count} instances of tags: {tags}")

        print(f"Took {end - start:.3f} seconds")
