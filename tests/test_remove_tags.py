"""
MC Structure Cleaner
Tests tag removal logic for 1.15.2 worlds
"""

import pytest
from pathlib import Path
from structurecleaner.constants import VANILLA_STRUCTURES as VS, DIMENSIONS
from tests.abstract_test import remove_tags_test


TS = {
    "repurposed_structures:mineshaft_icy",
    "repurposed_structures:mineshaft_end"
}


@pytest.mark.parametrize("dimension", DIMENSIONS)
def test_rt_purge_1_15_2(dimension: str, tmp_path: Path) -> None:
    """
    Test purge mode for 1.15.2
    Expected behaviour: All modded tags are removed
    """
    remove_tags_test("1.15.2", dimension, "purge", VS, tmp_path)


def test_rt_remove_1_15_2(tmp_path: Path) -> None:
    """
    Test remove mode for 1.15.2
    Expected behaviour: Only tags in TS are removed
    """
    remove_tags_test("1.15.2", "region", "remove", TS, tmp_path)


# def test_rt_purge_1_18_2(tmp_path: Path) -> None:
#    """
#    Test purge mode for 1.15.2
#    Expected behaviour: All modded tags are removed
#    """
#    remove_tags_test("1.18.2", "region", "purge", VS, tmp_path)
