from typing import Type

from treasurehunt.game.event_backend import (
    EventBackend,
    get_queue_event_backend_singleton,
)
from treasurehunt.game.mail_gateway import MailGateway, SMTPlibMailGateway
from treasurehunt.game.repository import (
    TreasureHuntRepository,
    get_in_memory_treasure_hunt_repository_singleton,
)
from treasurehunt.game.treasurehunt import TreasureHunt


class TreasureHuntFactory:
    def __init__(self):
        """
        Temporary solution,
        specific implementations should be provided from outside the factory.
        """
        self.__mail_gateway: Type[MailGateway] = SMTPlibMailGateway
        self.__repository: Type[
            TreasureHuntRepository
        ] = get_in_memory_treasure_hunt_repository_singleton  # type: ignore
        self.__event_backend: Type[
            EventBackend
        ] = get_queue_event_backend_singleton  # type: ignore

    def build(self) -> TreasureHunt:
        return TreasureHunt(
            repository=self.__repository(),
            mail_gateway=self.__mail_gateway(),
            event_backend=self.__event_backend(),
        )
