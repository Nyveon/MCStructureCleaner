"""
MC Structure cleaner
By: Nyveon

v: 1.1
Modded structure cleaner for minecraft. Removes all references to non-existent structures to allow for
clean error logs and chunk saving.
"""

# Imports
import anvil  # anvil-parser by matcool
import time  # for progress messages


# Efficient iteration
import itertools

# Argument parsing
from argparse import ArgumentParser, Namespace

# Filesystem interaction
from pathlib import Path

# Multiprocessing
from multiprocessing import Pool

version = "1.2"


def sep():
    print("----------------------------------")


# Functions
def remove_tags(to_replace: set[str], src: Path, dst: Path) -> int:
    start: float = time.perf_counter()
    count: int = 0

    coords = src.name.split(".")
    region = anvil.Region.from_file(str(src.resolve()))
    new_region = anvil.EmptyRegion(int(coords[1]), int(coords[2]))

    # Check chunks
    for chunk_x, chunk_z in itertools.combinations_with_replacement(range(32), 2):
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


def setup_environment(new_region: Path) -> bool:
    if new_region.exists():
        print(f"{new_region.resolve()} already exists, this may cause problems!")
        proceed = input("Do you want to preceed regardless? [y/N] ")

        return proceed.starts_with("y")
    else:
        new_region.mkdir()
        print(f"Saving newly generated region files to {new_region.resolve()}")

        return True


#  CLI
def get_args() -> Namespace:
    prog_msg = f"MC Structure cleaner\nBy: Nyveon\nVersion: {version}"
    tag_help = "The EXACT structure tag name you want removed (Use NBTExplorer to find the name)"
    jobs_help = "The number of processes to run (default 4)"
    parser = ArgumentParser()

    parser.add_argument("-t", "--tag", type=str, help=tag_help, required=True)
    parser.add_argument("-j", "--jobs", type=int, help=jobs_help, default=4)

    return parser.parse_args()


def main() -> None:
    args = get_args()

    to_replace = args.tag
    new_region = Path("new_region")
    world_region = Path("world/region")
    num_processes = args.jobs

    print("Replacing", to_replace, "in all region files.")
    sep()

    if not world_region.exists():
        print(f"Couldn't find {world_region.resolve()}")
        return None

    if not setup_environment(new_region):
        print("Aborted, nothing was done")
        return None

    to_process = list(world_region.iterdir())
    n_to_process = len(to_process)

    with Pool(processes=num_processes) as p:
        count = sum(
            p.map(lambda f: remove_tags({to_replace}, f, new_region), to_process)
        )
        print(f"Done!\nRemoved {count} instances of tags: {to_replace}")

    print("Processed {n_to_process} files")
    print("You can now replace {world_region} with {new_region}")


if __name__ == "__main__":
    main()
