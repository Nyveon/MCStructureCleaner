from typing import Set
from nbt import nbt
from abc import ABC, abstractmethod
from structurecleaner.constants import VANILLA_STRUCTURES


class RemovalStrategy(ABC):
    @abstractmethod
    def check_tag(self, tag: nbt.TAG) -> bool:
        pass

    @abstractmethod
    def print_find(self, removed_tags: Set[str]) -> None:
        pass

    @abstractmethod
    def print_done(self, count: int) -> None:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class PurgeRemovalStrategy(RemovalStrategy):
    def check_tag(self, tag: nbt.TAG) -> bool:
        return tag.name.lower() not in VANILLA_STRUCTURES

    def print_find(self, removed_tags: Set[str]) -> None:
        print(f"Found {len(removed_tags)} non-vanilla tags: {removed_tags}")

    def print_done(self, count: int) -> None:
        print(f"Done!\nRemoved {count} instances of non-vanilla tags")

    def get_name(self) -> str:
        return "purge"


class ListRemovalStrategy(RemovalStrategy):
    to_replace: Set[str]

    def __init__(self, to_replace: Set[str]):
        self.to_replace = to_replace

    def check_tag(self, tag: nbt.TAG) -> bool:
        return tag.name in self.to_replace

    def print_find(self, removed_tags: Set[str]) -> None:
        return

    def print_done(self, count: int) -> None:
        print(f"Done!\nRemoved {count} instances of tags: {self.to_replace}")

    def get_name(self) -> str:
        return "replace"
