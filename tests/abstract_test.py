"""
MC Structure Cleaner
Helper functions for tests
"""

import filecmp
from pathlib import Path
from multiprocessing import cpu_count
from structurecleaner.remove_tags import remove_tags

TEST_DIR = "tests/data"


def to_file_set(path: Path | str) -> set:
    """Return a set of all files in path

    Args:
        path (Path | str): The name of a path or a path

    Returns:
        set: A set of filenames
    """
    if isinstance(path, str):
        path = Path(path)
    return set(path.glob("*"))


def remove_tags_test(
    version: str, region: str, mode: str, tags: set, tmp_path: Path
) -> None:
    """Abstract testing for remove_tags
    Sets up the directories, runs the command, and then checks equality.

    Args:
        version (str): The version number ID of the test data
        region (str): The region name
        mode (str): Purge or Remove
        tags (set): Set of tags (strings)
        tmp_path (Path): The current testing tmp_path
    """
    jobs = cpu_count() // 2

    input_files = Path(f"{TEST_DIR}/{version}/input")
    assert input_files.exists(), f"{input_files} does not exist"

    target_files = Path(f"{TEST_DIR}/{version}/expected_{mode}")
    assert target_files.exists(), f"{target_files} does not exist"

    region_files = to_file_set(f"{input_files}/{region}")
    assert region_files, f"{region_files} is empty"

    region_target_files = to_file_set(target_files / f"{region}")
    assert region_target_files, f"{region_target_files} is empty"

    print(target_files / f"{region}")
    print("\n\n", region_target_files, "\n\n")

    src = Path(f"{input_files}/{region}")
    dst = tmp_path / f"{version}_{mode}_{region}"
    dst.mkdir(parents=True)
    assert (dst).exists(), "Output folder was not created"

    # Run remove_tags
    remove_tags(tags, src, dst, jobs, mode)

    for file in region_files:
        assert (dst / file.name).exists(), f"{file.name} was not created"
        assert (dst / file.name).stat().st_size > 0, f"{file.name} is empty"

    for file in region_target_files:
        print("\n\n", file, "\n\n")
        assert filecmp.cmp(
            (dst / file.name), file
        ), f"{file.name} is not target"
