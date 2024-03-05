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
        if tag.name.lower() in VANILLA_STRUCTURES:
            return False

        if tag.name.lower().startswith("minecraft:"):
            return False

        return True

    def print_find(self, removed_tags: Set[str]) -> None:
        print(f"Found {len(removed_tags)} non-vanilla tags: {removed_tags}")

    def print_done(self, count: int) -> None:
        print(f"Done!\nRemoved {count} instances of non-vanilla tags")

    def get_name(self) -> str:
        return "purge"


class ListRemovalStrategy(RemovalStrategy):
    to_replace: Set[str]
    to_replace_specific: Set[str]
    to_replace_wildcard: Set[str]

    def __init__(self, to_replace: Set[str]):
        self.to_replace = to_replace
        self.to_replace_specific = set()
        self.to_replace_wildcard = set()

        for tag in to_replace:
            if tag.endswith("*"):
                self.to_replace_wildcard.add(tag)
            else:
                self.to_replace_specific.add(tag)

    def check_tag(self, tag: nbt.TAG) -> bool:
        if tag.name in self.to_replace_specific:
            return True

        for wildcard in self.to_replace_wildcard:
            if tag.name.startswith(wildcard[:-1]):
                return True

        return False

    def print_find(self, removed_tags: Set[str]) -> None:
        return

    def print_done(self, count: int) -> None:
        print(f"Done!\nRemoved {count} instances of tags: {self.to_replace}")

    def get_name(self) -> str:
        return "replace"
