"""
MC Structure cleaner
By: Nyveon

v: 1.1
Modded structure cleaner for minecraft. Removes all references to non-existent
structures to allow for clean error logs and chunk saving.
"""

# Using Python 3.9 annotations
from __future__ import annotations

# Imports
import time  # for progress messages


# Efficient iteration
import itertools

# Argument parsing
from argparse import ArgumentParser, Namespace

# Filesystem interaction
from pathlib import Path

# Multiprocessing
from multiprocessing import Pool

import anvil  # anvil-parser by matcool

VERSION = "1.2"


def sep():
    """Print separator line"""
    print("----------------------------------")


# Removing Tags
def _remove_tags_region(args: tuple[set[str], Path, Path]) -> int:
    return remove_tags_region(*args)


def remove_tags_region(to_replace: set[str], src: Path, dst: Path) -> int:
    """Remove tags in to_replace from the src region
    Write changes to dst/src.name"""
    start: float = time.perf_counter()
    count: int = 0

    coords = src.name.split(".")
    region = anvil.Region.from_file(str(src.resolve()))
    new_region = anvil.EmptyRegion(int(coords[1]), int(coords[2]))

    # Check chunks
    for chunk_x, chunk_z in itertools.product(range(32), repeat=2):
        # Chunk Exists
        if region.chunk_location(chunk_x, chunk_z) != (0, 0):
            data = region.chunk_data(chunk_x, chunk_z)

            for tag in data["Level"]["Structures"]["Starts"].tags:
                if tag.name in to_replace:
                    del data["Level"]["Structures"]["Starts"][tag.name]
                    count += 1

            for tag in data["Level"]["Structures"]["References"].tags:
                if tag.name in to_replace:
                    del data["Level"]["Structures"]["References"][tag.name]
                    count += 1

            # Add the modified chunk data to the new region
            new_region.add_chunk(anvil.Chunk(data))

    # Save Region
    new_region.save(str((dst / src.name).resolve()))

    end: float = time.perf_counter()
    print(f"{count} instances of tags removed in {end - start:.3f} s")

    return count


def remove_tags(tags: set[str], src: Path, dst: Path, jobs: int) -> None:
    """Removes tags from src region files and writes them to dst"""
    with Pool(processes=jobs) as pool:
        start = time.perf_counter()

        count = sum(
            pool.map(
                _remove_tags_region,
                zip(
                    itertools.repeat(tags),
                    src.iterdir(),
                    itertools.repeat(dst),
                ),
            )
        )

        end = time.perf_counter()

        sep()
        print(f"Done!\nRemoved {count} instances of tags: {tags}")
        print(f"Took {end - start:.3f} seconds")


# Environment
def setup_environment(new_region: Path) -> bool:
    """Try to create new_region folder"""
    if new_region.exists():
        print(f"{new_region.resolve()} exists, this may cause problems")
        proceed = input("Do you want to proceed regardless? [y/N] ")

        return proceed.startswith("y")

    new_region.mkdir()
    print(f"Saving newly generated region files to {new_region.resolve()}")

    return True


#  CLI
def get_args() -> Namespace:
    """Get CLI Arguments"""
    prog_msg = f"MC Structure cleaner\nBy: Nyveon\nVersion: {VERSION}"
    tag_help = "The EXACT structure tag name you want removed (Use NBTExplorer\
            to find the name)"
    jobs_help = "The number of processes to run (default 4)"
    parser = ArgumentParser(prog=prog_msg)

    parser.add_argument("-t", "--tag", type=str, help=tag_help, required=True)
    parser.add_argument("-j", "--jobs", type=int, help=jobs_help, default=4)

    return parser.parse_args()


def _main() -> None:
    args = get_args()

    to_replace = args.tag
    new_region = Path("new_region")
    world_region = Path("world/region")
    num_processes = args.jobs

    print(f"Replacing {to_replace} in all region files.")
    sep()

    if not world_region.exists():
        print(f"Couldn't find {world_region.resolve()}")
        return None

    if not setup_environment(new_region):
        print("Aborted, nothing was done")
        return None

    n_to_process = len(world_region.iterdir())

    remove_tags({to_replace}, world_region, new_region, num_processes)

    sep()
    print(f"Processed {n_to_process} files")
    print(f"You can now replace {world_region} with {new_region}")

    return None


if __name__ == "__main__":
    _main()
