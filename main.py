"""
MC Structure Cleaner
By: Nyveon and DemonInTheCloset
Thanks: lleheny0
Special thanks: panchito, tomimi, puntito,
and everyone who has reported bugs and given feedback.

Modded structure cleaner for minecraft. Removes all references to non-existent
structures to allow for clean error logs and chunk saving.

Project structure:
    main.py - Command Line Interface
    remove_tags.py - Main logic
    tests - Unit tests
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path
from multiprocessing import cpu_count
from mcsc.constants import SEP
from mcsc.remove_tags import remove_tags

VERSION = "1.6"


# Environment
def setup_environment(new_region: Path) -> bool:
    """Try to create new_region folder"""
    if new_region.exists():
        print(f"{new_region.resolve()} exists, this may cause problems")
        proceed = input("Do you want to proceed regardless? [y/N] ")
        print(SEP)
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
    path_help = "The path of the world you wish to process (default: 'world')"
    output_help = "The path where you wish to save the output (default: './'"
    region_help = "The name of the region folder (dimension) \
            you wish to process (default: "")"

    parser = ArgumentParser(prog=prog_msg)

    parser.add_argument("-t", "--tag",
                        type=str,
                        help=tag_help,
                        default="",
                        nargs="*")
    parser.add_argument("-j", "--jobs",
                        type=int,
                        help=jobs_help,
                        default=jobs)
    parser.add_argument("-p", "--path",
                        type=str,
                        help=path_help,
                        default="world")
    parser.add_argument("-o", "--output",
                        type=str,
                        help=output_help,
                        default="./")
    parser.add_argument("-r", "--region",
                        type=str,
                        help=region_help,
                        default="")

    return parser.parse_args()


def process_args(args: Namespace):
    """Process CLI Arguments"""
    processed = []
    processed.append(set(args.tag))
    processed.append(Path(f"{args.output}/new_region{args.region}"))
    processed.append(Path(f"{args.path}/{args.region}/region"))
    processed.append(args.jobs)
    return processed


def main() -> None:
    args = process_args(get_args())
    to_replace, new_region, world_region, num_processes = args

    print(SEP)

    # Force purge mode if no tag is given, otherwise normal.
    mode = "purge" if not to_replace else "normal"
    if mode == "purge":
        print("No tag given, will run in purge mode.")
        print(f"Replacing all non-vanilla structures in \
            all region files in {world_region}.")
    else:
        print("Tag(s) given, will run in normal mode.")
        print(f"Replacing {to_replace} in all region files in {world_region}.")

    print(SEP)

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
    print(f"{SEP}\nProcessed {n_to_process} files")
    print(f"You can now replace {world_region} with {new_region}")
    return None


if __name__ == "__main__":
    main()
