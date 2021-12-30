from typing import AsyncGenerator

import pytest

from tests.mailhog_client import MailHogClient
from treasurehunt.game.event_backend import QueueEventBackend
from treasurehunt.game.mail_gateway import SMTPlibMailGateway
from treasurehunt.game.repository import InMemoryTreasureHuntRepository
from treasurehunt.game.treasurehunt import TreasureHunt


@pytest.fixture
def treasurehunt_game() -> TreasureHunt:
    return TreasureHunt(
        repository=InMemoryTreasureHuntRepository(),
        mail_gateway=SMTPlibMailGateway(),
        event_backend=QueueEventBackend(),
    )


@pytest.fixture()
async def mailhog_client() -> AsyncGenerator[MailHogClient, None]:
    async with MailHogClient() as client:
        await client.delete_messages()
        yield client
        await client.delete_messages()
