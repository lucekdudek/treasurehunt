from typing import AsyncGenerator, Callable, Generator

import pytest
from httpx import AsyncClient

from treasurehunt.app import app
from treasurehunt.auth.handlers import AUTH_HANDLER
from treasurehunt.auth.repository import (
    InMemoryAuthRepository,
    get_in_memory_auth_repository_singleton,
)
from treasurehunt.auth.schemas import AuthDetails


@pytest.fixture
def auth_repository() -> Generator[InMemoryAuthRepository, None, None]:
    in_memory_auth = get_in_memory_auth_repository_singleton()
    in_memory_auth._InMemoryAuthRepository__users = {}  # type: ignore
    yield in_memory_auth
    in_memory_auth._InMemoryAuthRepository__users = {}  # type: ignore


@pytest.fixture
def user_factory(
    auth_repository: InMemoryAuthRepository,
) -> Callable[[str, str], None]:
    def create_user(username: str, password: str):
        auth_repository._InMemoryAuthRepository__users[  # type: ignore
            username
        ] = AuthDetails(user_id=username, hash=AUTH_HANDLER.get_password_hash(password))

    return create_user


@pytest.fixture
def auth_token(user_factory) -> str:
    user_factory("username", "password")
    return AUTH_HANDLER.encode_token("username")


@pytest.fixture
async def treasurehunt_api_client(auth_token: str) -> AsyncGenerator[AsyncClient, None]:
    client = AsyncClient(
        app=app,
        base_url="http://test",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    yield client
    await client.aclose()
