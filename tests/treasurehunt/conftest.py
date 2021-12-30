import pytest

from treasurehunt.game.schemas import Hunter
from treasurehunt.settings import TREASUREHUNT_SETTINGS


@pytest.fixture(autouse=True, scope="session")
def test_settings():
    TREASUREHUNT_SETTINGS.smtp_host = "localhost"


@pytest.fixture
def test_hunter() -> Hunter:
    return Hunter(email="test@hunter.game")
