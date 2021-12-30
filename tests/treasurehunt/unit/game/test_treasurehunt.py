import pytest
from geopy import Point

from tests.mailhog_client import MailHogClient
from treasurehunt.game.schemas import Hunter
from treasurehunt.game.treasurehunt import TreasureHunt


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "given_location,expected_distance,expected_mail",
    [
        (Point(latitude=19.945704, longitude=50.051227), 0, True),
        (Point(latitude=19.945800, longitude=50.051200), 10, False),
        (Point(latitude=19.945704, longitude=50000.051227), 9278244, False),
    ],
)
async def test_hunt(
    mailhog_client: MailHogClient,
    treasurehunt_game: TreasureHunt,
    test_hunter: Hunter,
    given_location: Point,
    expected_distance: int,
    expected_mail: bool,
):
    # when
    received_distance = await treasurehunt_game.hunt(test_hunter, given_location)
    # then
    assert received_distance == expected_distance
    messages = await mailhog_client.get_messages()
    assert bool(messages.items) is expected_mail
