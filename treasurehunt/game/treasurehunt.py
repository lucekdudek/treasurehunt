import logging
from typing import AsyncGenerator

from geopy import Point, distance

from treasurehunt.game.event_backend import EventBackend
from treasurehunt.game.exceptions import (
    MailGatewayException,
    WinnerAlreadyExists,
)
from treasurehunt.game.mail_gateway import MailGateway
from treasurehunt.game.repository import TreasureHuntRepository
from treasurehunt.game.schemas import Hunter, HuntingEvent

logger = logging.getLogger("treasurehunt.treasurehunt")


class TreasureHunt:
    __winning_message_subject = """Hey, message from TreasureHunt"""
    __winning_message = """Hey, you’ve found a treasure, congratulations!
You are {nth} treasure hunter who has found the treasure.
Treasure location: {treasure_location}"""
    __hunting_event_message = (
        "{hunter_email} reached {location_str}. "
        "Hunter is {remaining_distance} meters away from the treasure."
    )

    def __init__(
        self,
        repository: TreasureHuntRepository,
        mail_gateway: MailGateway,
        event_backend: EventBackend,
    ):
        self.__repository = repository
        self.__mail_gateway = mail_gateway
        self.__event_backend = event_backend

    async def hunt(self, hunter: Hunter, hunter_location: Point) -> int:
        treasure_location = await self.__repository.read_treasure_location()
        remaining_distance = self.__mesure_distance_meters(
            hunter_location, treasure_location
        )
        is_winning = self.__hunter_is_winning(remaining_distance)
        if is_winning:
            try:
                await self.__repository.save_winner(hunter.email)
                await self.__inform_hunter_about_victory(
                    hunter, treasure_location=treasure_location
                )
            except WinnerAlreadyExists:
                pass
        await self.__event_backend.publish(
            HuntingEvent(
                hunter=hunter,
                location_str=hunter_location.format_unicode(),
                remaining_distance=remaining_distance,
                is_winning=is_winning,
            )
        )
        return remaining_distance

    def __mesure_distance_meters(self, distance_from: Point, distance_to: Point) -> int:
        return int(distance.distance(distance_from, distance_to).meters)

    def __hunter_is_winning(self, remaining_distance: int) -> bool:
        return remaining_distance <= 5

    async def __inform_hunter_about_victory(
        self, hunter: Hunter, treasure_location: Point
    ) -> None:
        winner_count = await self.__repository.read_winner_count()
        try:
            await self.__mail_gateway.send_mail(
                recipient=hunter.email,
                message=self.__winning_message.format(
                    nth=winner_count,
                    treasure_location=treasure_location.format_unicode(),
                ),
                subject=self.__winning_message_subject,
            )
        except MailGatewayException:
            logger.error(
                "Cannot inform a hunter about victory.",
                extra=dict(hunter_email=hunter.email),
                exc_info=True,
            )

    async def follow_hunt(self) -> AsyncGenerator[str, None]:
        async for event in self.__event_backend.subscribe():
            yield self.__hunting_event_message.format(
                hunter_email=event.hunter.email,
                location_str=event.location_str,
                remaining_distance=event.remaining_distance,
            )
