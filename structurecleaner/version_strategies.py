from abc import ABC, abstractmethod
from nbt import nbt
from typing import Set

from structurecleaner.removal_strategies import RemovalStrategy


class VersionStrategy(ABC):
    removal_strategy: RemovalStrategy

    def __init__(self, removal_strategy: RemovalStrategy):
        self.removal_strategy = removal_strategy

    @abstractmethod
    def remove_tags(
        self, data: nbt.NBTFile, data_copy: nbt.NBTFile, removed_tags: Set[str]
    ) -> int:
        pass


class OldDataVersion(VersionStrategy):
    def remove_tags(self, data, data_copy, removed_tags: Set[str]) -> int:
        count = 0

        if hasattr(data["Level"]["Structures"]["Starts"], "tags"):
            for tag in data["Level"]["Structures"]["Starts"].tags:
                if self.removal_strategy.check_tag(tag):
                    del data_copy["Level"]["Structures"]["Starts"][tag.name]
                    count += 1
                    removed_tags.add(tag.name)

        if hasattr(data["Level"]["Structures"]["References"], "tags"):
            for tag in data["Level"]["Structures"]["References"].tags:
                if self.removal_strategy.check_tag(tag):
                    del data_copy["Level"]["Structures"]["References"][
                        tag.name
                    ]
                    count += 1
                    removed_tags.add(tag.name)

        return count


class NewDataVersion(VersionStrategy):
    def remove_tags(self, data, data_copy, removed_tags: Set[str]) -> int:
        count = 0

        if hasattr(data["structures"]["starts"], "tags"):
            for tag in data["structures"]["starts"].tags:
                if self.removal_strategy.check_tag(tag):
                    del data_copy["structures"]["starts"][tag.name]
                    count += 1
                    removed_tags.add(tag.name)

        if hasattr(data["structures"]["References"], "tags"):
            for tag in data["structures"]["References"].tags:
                if self.removal_strategy.check_tag(tag):
                    del data_copy["structures"]["References"][
                        tag.name
                    ]
                    count += 1
                    removed_tags.add(tag.name)

        return count
