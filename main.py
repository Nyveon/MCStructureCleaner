"""
MC Structure cleaner
By: Nyveon and DemonInTheCloset
Thanks: lleheny0
Special thanks: panchito, tomimi, puntito,
and everyone who has reported bugs and given feedback.

Modded structure cleaner for minecraft. Removes all references to non-existent
structures to allow for clean error logs and chunk saving.
"""

import time
import os
import anvil
import itertools as it
from argparse import ArgumentParser, Namespace
from pathlib import Path
from multiprocessing import Pool, cpu_count
from typing import Set, Tuple

# --- Constants ---

VERSION = "1.6"

VANILLA_STRUCTURES = {
    "bastion_remnant",
    "buried_treasure",
    "desert_pyramid",
    "endcity",
    "fortress",
    "igloo",
    "jungle_pyramid",
    "mansion",
    "mineshaft",
    "monument",
    "nether_fossil",
    "ocean_ruin",
    "pillager_outpost",
    "ruined_portal",
    "shipwreck",
    "stronghold",
    "swamp_hut",
    "village",
}

# Data version difference between 1.17.1 and 1.18 snapshots+
NEW_DATA_VERSION = 2800


# Print separator
def sep():
    """Print separator line"""
    print("----------------------------------")


# Removing Tags
def _remove_tags_region(args: Tuple[Set[str], Path, Path, str]) -> int:
    """Wrapper for removing tags from a region file"""
    return remove_tags_region(*args)


def remove_tags_region(to_replace: Set[str],
                       src: Path, dst: Path, mode: str) -> int:
    """Remove tags in to_replace from the src region
    Write changes to dst/src.name"""
    start: float = time.perf_counter()
    count: int = 0

    print("Checking file:", src)

    # Check if it's even an .mca file
    print(src)
    if len(str(src)) > 4:
        if str(src)[-1:-5:-1] != "acm.":
            print(f"{src} is not a valid region file.")
            return 0
    else:
        print(f"{src} is not a valid file.")
        return 0

    # Check if file isn't empty
    if os.path.getsize(src) == 0:
        print(f"{src} is empty.")
        return 0

    coords = src.name.split(".")
    region = anvil.Region.from_file(str(src.resolve()))
    new_region = anvil.EmptyRegion(int(coords[1]), int(coords[2]))
    removed_tags = set()

    # Lambda function for checking if a tag is valid
    if mode == "purge":
        def check_tag(_tag):
            return _tag.name not in VANILLA_STRUCTURES
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
        print("Non-vanilla tags found:")
        print(removed_tags)
        sep()

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
        count = sum(pool.map(_remove_tags_region, data))

        end = time.perf_counter()

        sep()
        if mode == "purge":
            print(f"Done!\nRemoved {count} instances of non-vanilla tags")
        else:
            print(f"Done!\nRemoved {count} instances of tags: {tags}")

        print(f"Took {end - start:.3f} seconds")


# Environment
def setup_environment(new_region: Path) -> bool:
    """Try to create new_region folder"""
    if new_region.exists():
        print(f"{new_region.resolve()} exists, this may cause problems")
        proceed = input("Do you want to proceed regardless? [y/N] ")
        sep()
        return proceed.startswith("y")

    new_region.mkdir()
    print(f"Saving newly generated region files to {new_region.resolve()}")

    return True


#  CLI
def get_args() -> Namespace:
    """Get CLI Arguments"""
    jobs = cpu_count() // 2

    prog_msg = f"MC Structure cleaner\nBy: Nyveon\nVersion: {VERSION}"
    tag_help = "The EXACT structure tag name you want removed (Use \
            NBTExplorer to find the name), default is an empty \
            string (for use in purge mode)"
    jobs_help = f"The number of processes to run (default: {jobs})"
    world_help = "The name of the world you wish to process (default: 'world')"
    region_help = "The name of the region folder (dimension) \
            you wish to process (default: "")"

    parser = ArgumentParser(prog=prog_msg)

    parser.add_argument("-t", "--tag", type=str,
                        help=tag_help, default="", nargs="*")
    parser.add_argument("-j", "--jobs", type=int, help=jobs_help, default=jobs)
    parser.add_argument("-w", "--world", type=str,
                        help=world_help, default="world")
    parser.add_argument("-r", "--region", type=str,
                        help=region_help, default="")

    return parser.parse_args()


def main() -> None:
    args = get_args()

    to_replace = set(args.tag)
    new_region = Path("new_" + args.region + "region")
    world_region = Path(args.world + "/" + args.region + "/region")
    num_processes = args.jobs

    sep()

    # Force purge mode if no tag is given, otherwise normal.
    mode = "normal"
    if args.tag == "":
        print("No tag given, will run in purge mode.")
        mode = "purge"
    else:
        print("Tag(s) given, will run in normal mode.")

    # Feedback as to what the program is about to do.
    if mode == "normal":
        print(f"Replacing {to_replace} in all region files in {world_region}.")
    elif mode == "purge":
        print(f"Replacing all non-vanilla structures in \
            all region files in {world_region}.")
    sep()

    # Check if world exists
    if not world_region.exists():
        print(f"Couldn't find {world_region.resolve()}")
        return None

    # Check if output already exists
    if not setup_environment(new_region):
        print("Aborted, nothing was done")
        return None

    n_to_process = len(list(world_region.iterdir()))

    remove_tags(to_replace, world_region, new_region, num_processes, mode)

    # End output
    sep()
    print(f"Processed {n_to_process} files")
    print(f"You can now replace {world_region} with {new_region}")
    return None


# When running
if __name__ == "__main__":
    main()
