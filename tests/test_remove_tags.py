"""
MC Structure Cleaner
Tests tag removal logic for 1.15.2 worlds
"""

import pytest
import filecmp
from pathlib import Path
from mcstructurecleaner.remove_tags import remove_tags
from mcstructurecleaner.constants import VANILLA_STRUCTURES as VS
from multiprocessing import cpu_count
from tests.test_helpers import to_file_set

TS = [
    "repurposed_structures:mineshaft_icy",
    "repurposed_structures:mineshaft_end"
]

DIMENSIONS = ["region", "DIM1/region", "DIM-1/region"]


@pytest.mark.parametrize(
    "version,region,mode,tags",
    [
        ("1.15.2", "region", "purge", VS),
        ("1.15.2", "DIM1/region", "purge", VS),
        ("1.15.2", "DIM-1/region", "purge", VS),
        #("1.15.2", "region", "remove", TS),
    ]
    )
def remove_tags_test(version: str, region: str, mode: str,
                     tags: list, tmp_path: Path) -> None:
    """
    General test for removing tags
    """
    jobs = cpu_count() // 2

    input_files = Path(f"test_files/{version}/input")
    assert input_files.exists(), f"{input_files} does not exist"

    target_files = Path(f"test_files/{version}/expected_{mode}")
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
        assert filecmp.cmp((dst / file.name), file), \
            f"{file.name} is not target"


@pytest.mark.parametrize("dimension", DIMENSIONS)
def test_rt_purge_1_15_2(dimension: str, tmp_path: Path) -> None:
    remove_tags_test("1.15.2", dimension, "purge", VS, tmp_path)


#def test_rt_remove_1_15_2(dimension: str, tmp_path: Path) -> None:
#    remove_tags_test("1.15.2", "region", "remove", TS, tmp_path)
