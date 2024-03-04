"""
MC Structure Cleaner
Tests tag removal logic for individual region files.
Uses a custom 1.15.2 region file
"""

import filecmp
import pytest
from structurecleaner.remove_tags import _remove_tags_region
from structurecleaner.errors import (
    InvalidRegionFileError,
    InvalidFileNameError,
    EmptyFileError,
)
from structurecleaner.removal_strategies import (
    ListRemovalStrategy,
    PurgeRemovalStrategy,
)
from tests.abstract_test import TEST_DIR
from pathlib import Path

TS = {
    "repurposed_structures:mineshaft_icy",
    "repurposed_structures:mineshaft_end",
}

tag_strategy = ListRemovalStrategy(TS)
purge_strategy = PurgeRemovalStrategy()
empty_strategy = ListRemovalStrategy(set())

test_data_path = f"{TEST_DIR}/tags_region"
file_name = "r.0.0.mca"


def test_empty_mca(tmp_path: Path) -> None:
    test_file = Path(f"{test_data_path}/input_empty/{file_name}")
    with pytest.raises(EmptyFileError):
        _remove_tags_region(empty_strategy, test_file, tmp_path)


def test_not_mca(tmp_path: Path) -> None:
    test_file = Path(f"{test_data_path}/input_wrong_filetype/r.0.0.txt")
    with pytest.raises(InvalidRegionFileError):
        _remove_tags_region(empty_strategy, test_file, tmp_path)


def test_too_short(tmp_path: Path) -> None:
    test_file = Path("./")
    with pytest.raises(InvalidFileNameError):
        _remove_tags_region(empty_strategy, test_file, tmp_path)


def test_mca_purge_empty(tmp_path: Path) -> None:
    test_file = Path(f"{test_data_path}/input/{file_name}")
    target_file = Path(f"{test_data_path}/output_purge/{file_name}")
    result = _remove_tags_region(purge_strategy, test_file, tmp_path)
    assert result != 0
    assert filecmp.cmp((tmp_path / file_name), target_file)


def test_mca_remove_empty(tmp_path: Path) -> None:
    test_file = Path(f"{test_data_path}/input/{file_name}")
    target_file = Path(f"{test_data_path}/output_remove_0/{file_name}")
    result = _remove_tags_region(empty_strategy, test_file, tmp_path)
    assert result == 0
    assert filecmp.cmp((tmp_path / file_name), target_file)


def test_mca_remove(tmp_path: Path) -> None:
    test_file = Path(f"{test_data_path}/input/{file_name}")
    target_file = Path(f"{test_data_path}/output_remove/{file_name}")
    result = _remove_tags_region(tag_strategy, test_file, tmp_path)
    assert result != 0
    assert filecmp.cmp((tmp_path / file_name), target_file)
