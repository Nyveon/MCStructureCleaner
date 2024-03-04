"""
MC Structure Cleaner
Tests tag removal logic for individual region files.
Uses a custom 1.15.2 region file
"""

from pathlib import Path
from structurecleaner.remove_tags import _remove_tags_region_task
from tests.abstract_test import TEST_DIR

TS = {
    "repurposed_structures:mineshaft_icy",
    "repurposed_structures:mineshaft_end",
}

test_data_path = f"{TEST_DIR}/tags_region"
file_name = "r.0.0.mca"


def test_remove_tags_region_task(tmp_path: Path) -> None:
    test_file = Path(f"{test_data_path}/input/{file_name}")
    result = _remove_tags_region_task((TS, test_file, tmp_path, "remove"))
    assert result != 0


def test_empty_mca(tmp_path: Path) -> None:
    test_file = Path(f"{test_data_path}/input_empty/{file_name}")
    result = _remove_tags_region_task((TS, test_file, tmp_path, "remove"))
    assert result == 0


def test_not_mca(tmp_path: Path) -> None:
    test_file = Path(f"{test_data_path}/input_wrong_filetype/r.0.0.txt")
    result = _remove_tags_region_task((TS, test_file, tmp_path, "remove"))
    assert result == 0


def test_too_short(tmp_path: Path) -> None:
    test_file = Path("./")
    result = _remove_tags_region_task((TS, test_file, tmp_path, "remove"))
    assert result == 0
