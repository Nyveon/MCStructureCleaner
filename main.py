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
from structurecleaner.constants import SEP
from structurecleaner.remove_tags import remove_tags
from typing import Tuple

try:
    from gooey import Gooey, GooeyParser  # type: ignore
except ImportError:
    Gooey = None

# Information
NAME = "MC Structure Cleaner"
VERSION = "1.7"
DESCRIPTION = f"By: Nyveon\nVersion: {VERSION}"
HELP_JOBS = (
    "The number of processes to run. "
    "Going over your CPU count may "
    "slow things down. The default is recommendable"
)
HELP_TAG = (
    "You can leave this blank to remove all non-vanilla structures. \n"
    "Or you can write a list of: \n"
    "- The exact structure tag you want removed. \n"
    "- A (*) as a wildcard for a prefix (see github) \n"
    "Separate tags by spaces. Use \"\" if the names have space characters. "
)
HELP_PATH = "The path of the world you wish to process"
HELP_OUTPUT = "The path of the folder you wish to save the new region files to"
HELP_REGION = (
    "The name of the region folder (dimension) "
    " | Overworld: (blank) | Nether: DIM-1 | End: DIM1"
)

# Configuration
DEFAULT_PATH = "world"
DEFAULT_OUTPUT = "./"


# Environment
def setup_environment(new_region: Path) -> bool:
    """Try to create new_region folder
    This is the folder where the new region files will be saved

    Args:
        new_region (Path): Path to new region folder

    Returns:
        bool: True if successful, False otherwise
    """
    if new_region.exists():
        if Gooey:
            raise FileExistsError(
                f"{new_region} already exists, please delete"
                " it or choose a different folder."
            )
        else:
            print(f"{new_region.resolve()} exists, this may cause problems")
            proceed = input("Do you want to proceed regardless? [y/N] ")
            print(SEP)
            return proceed.startswith("y")

    new_region.mkdir()
    print(f"Saving newly generated region files to {new_region.resolve()}")

    return True


def get_default_jobs() -> int:
    """Get default number of jobs

    Returns:
        int: The number of CPU cores in the device
    """
    return cpu_count() // 2


def get_cli_args() -> Namespace:
    """Get CLI Arguments

    Returns:
        Namespace: The parsed arguments
    """
    jobs = get_default_jobs()
    jobs_help = f"{HELP_JOBS} (default: {jobs})"
    path_help = f"{HELP_PATH} (default: '{DEFAULT_PATH}')"
    output_help = f"{HELP_OUTPUT} (default: '{DEFAULT_OUTPUT}')"

    parser = ArgumentParser(prog=f"{NAME}\n{DESCRIPTION}")

    parser.add_argument(
        "-t", "--tag", type=str, help=HELP_TAG, default="", nargs="*"
    )
    parser.add_argument("-j", "--jobs", type=int, help=jobs_help, default=jobs)
    parser.add_argument(
        "-p", "--path", type=str, help=path_help, default="world"
    )
    parser.add_argument(
        "-o", "--output", type=str, help=output_help, default="./"
    )
    parser.add_argument(
        "-r", "--region", type=str, help=HELP_REGION, default=""
    )

    return parser.parse_args()


# GUI (Only if Gooey is installed)
if Gooey:

    @Gooey(
        program_name=NAME,
        program_description=DESCRIPTION,
        header_bg_color="#6dd684",
        default_size=(610, 610),
        image_dir="./images",
        menu=[
            {
                "name": "About",
                "items": [
                    {
                        "type": "AboutDialog",
                        "menuTitle": "About",
                        "name": NAME,
                        "description": DESCRIPTION,
                        "version": VERSION,
                        "website": "https://github.com/Nyveon/MCStructureCleaner",
                    }
                ],
            },
            {
                "name": "Help",
                "items": [
                    {
                        "type": "Link",
                        "menuTitle": "Information",
                        "url": "https://github.com/Nyveon/MCStructureCleaner",
                    },
                    {
                        "type": "Link",
                        "menuTitle": "Report an issue",
                        "url": "https://github.com/Nyveon/MCStructureCleaner/issues",
                    },
                ],
            },
        ],
    )
    def get_gui_args() -> Namespace:
        """Get GUI Arguments

        Returns:
            Namespace: The parsed arguments
        """
        jobs = get_default_jobs()
        parser = GooeyParser()

        parser.add_argument(
            "-t", "--tag", type=str, help=HELP_TAG, default="", nargs="*"
        )
        parser.add_argument(
            "-j",
            "--jobs",
            type=int,
            help=HELP_JOBS,
            default=jobs,
            widget="IntegerField",
            gooey_options={"min": 1, "max": jobs * 2},
        )
        parser.add_argument(
            "-p",
            "--path",
            type=str,
            help=HELP_PATH,
            default="./world",
            widget="DirChooser",
        )
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            help=HELP_OUTPUT,
            default="./",
            widget="DirChooser",
        )
        parser.add_argument(
            "-r", "--region", type=str, help=HELP_REGION, default=""
        )

        return parser.parse_args()


def process_args(args: Namespace) -> Tuple[set, Path, Path, int]:
    """Process CLI or GUI Arguments

    Args:
        args (Namespace): Parsed CLI or GUI arguments

    Returns:
        Tuple[set, Path, Path, int]: Processed arguments:
            1. A set of tags (strings)
            2. The output path
            3. The input path
            4. The job
    """
    return (
        set(args.tag),
        Path(f"{args.output}/new_region{args.region}"),
        Path(f"{args.path}/{args.region}/region"),
        args.jobs,
    )


def main() -> None:
    """The main program"""
    # CLI or GUI arguments
    args = get_gui_args() if Gooey else get_cli_args()
    to_replace, new_region, world_region, num_processes = process_args(args)

    # Force purge mode if no tag is given, otherwise normal.
    mode = "purge" if not to_replace else "normal"
    if mode == "purge":
        print("No tag given, will run in purge mode.")
        print(
            f"Replacing all non-vanilla structures in \
            all region files in {world_region}."
        )
    else:
        print("Tag(s) given, will run in normal mode.")
        print(f"Replacing {to_replace} in all region files in {world_region}.")

    print(SEP)

    # Check if world exists
    if not world_region.exists():
        raise FileNotFoundError(f"Couldn't find {world_region.resolve()}")

    # Check if output already exists
    if not setup_environment(new_region):
        raise SystemExit("Aborted, nothing was done")

    n_to_process = len(list(world_region.iterdir()))
    remove_tags(to_replace, world_region, new_region, num_processes, mode)

    # End output
    print(f"{SEP}\nProcessed {n_to_process} files")
    print(f"You can now replace {world_region} with {new_region}")
    return None


if __name__ == "__main__":
    main()
