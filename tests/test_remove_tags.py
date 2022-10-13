"""
MC Structure Cleaner
Tests tag removal logic for 1.15.2 worlds
"""

import filecmp
from pathlib import Path
from mcstructurecleaner.remove_tags import remove_tags
from mcstructurecleaner.constants import VANILLA_STRUCTURES as VS
from multiprocessing import cpu_count
from tests.test_helpers import to_file_set


def remove_tags_test(version: str, region: str, mode: str,
                     tags: list, tmp_path: Path) -> None:
    """
    General test for removing tags
    """
    jobs = cpu_count() // 2
    input_files = f"test_files/{version}/input"
    target_files = f"test_files/{version}/expected_{mode}"
    region_files = to_file_set(f"{input_files}/{region}")
    region_target_files = to_file_set(f"{target_files}/{region}")

    src = Path(f"{input_files}/{region}")
    dst = tmp_path / f"{version}_{mode}_{region}"
    dst.mkdir(parents=True)
    assert (dst).exists(), "Output folder was not created"

    remove_tags(tags, src, dst, jobs, mode)

    print((dst).glob("*"))

    for file in region_files:
        assert (dst / file.name).exists(), f"{file.name} was not created"
        assert (dst / file.name).stat().st_size > 0, f"{file.name} is empty"

    for file in region_target_files:
        assert filecmp.cmp((dst / file.name), file), \
            f"{file.name} is not target"


def test_remove_tags_1_15_2_region_purge(tmp_path: Path) -> None:
    remove_tags_test("1.15.2", "region", "purge", VS, tmp_path)


def test_remove_tags_1_15_2_nether_purge(tmp_path: Path) -> None:
    remove_tags_test("1.15.2", "DIM-1/region", "purge", VS, tmp_path)


def test_remove_tags_1_15_2_end_purge(tmp_path: Path) -> None:
    remove_tags_test("1.15.2", "DIM1/region", "purge", VS, tmp_path)


def test_remove_tags_1_15_2_region_remove(tmp_path: Path) -> None:
    remove_tags_test("1.15.2", "region", "remove", VS, tmp_path)
