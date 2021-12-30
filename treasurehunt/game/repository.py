from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Set

from geopy import Point

from treasurehunt.game.exceptions import WinnerAlreadyExists


class TreasureHuntRepository(ABC):
    @abstractmethod
    async def read_treasure_location(self) -> Point:
        raise NotImplementedError

    @abstractmethod
    async def save_winner(self, winner: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read_winner_count(self) -> int:
        """
        Separating `save_winner` and `read_winner_count` might cause wrong winner count.
        To fix this, include a timestamp and save when a hunter become a winner.
        """
        raise NotImplementedError


class InMemoryTreasureHuntRepository(TreasureHuntRepository):
    __winners: Set[str] = set()
    __treasure_location = Point(latitude=19.945704, longitude=50.051227)

    async def read_treasure_location(self) -> Point:
        return self.__treasure_location

    async def save_winner(self, winner: str) -> None:
        if winner in self.__winners:
            raise WinnerAlreadyExists(f"{winner} is already a winner.")
        self.__winners.add(winner)

    async def read_winner_count(self) -> int:
        return len(self.__winners)


@lru_cache(maxsize=1)
def get_in_memory_treasure_hunt_repository_singleton() -> InMemoryTreasureHuntRepository:
    return InMemoryTreasureHuntRepository()
