from typing import Callable

import pytest
from fastapi import status
from httpx import AsyncClient

from treasurehunt.auth.repository import AuthRepository


@pytest.mark.asyncio
async def test_register_created(
    auth_repository: AuthRepository, treasurehunt_api_client: AsyncClient
):
    # given
    given_payload = {
        "username": "given_username",
        "password": "given_password",
    }
    # when
    received_response = await treasurehunt_api_client.post(
        "/register", json=given_payload
    )
    # then
    assert received_response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_register_conflict(
    user_factory: Callable[[str, str], None], treasurehunt_api_client: AsyncClient
):
    # given
    given_payload = {
        "username": "given_username",
        "password": "given_password",
    }
    user_factory(given_payload["username"], given_payload["password"])
    # when
    received_response = await treasurehunt_api_client.post(
        "/register", json=given_payload
    )
    # then
    assert received_response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
async def test_login_accepted(
    user_factory: Callable[[str, str], None], treasurehunt_api_client: AsyncClient
):
    # given
    given_payload = {
        "username": "given_username",
        "password": "given_password",
    }
    user_factory(given_payload["username"], given_payload["password"])
    # when
    received_response = await treasurehunt_api_client.post("/login", json=given_payload)
    # then
    assert received_response.status_code == status.HTTP_202_ACCEPTED


@pytest.mark.asyncio
async def test_login_unauthorized(
    auth_repository: AuthRepository, treasurehunt_api_client: AsyncClient
):
    # given
    given_payload = {
        "username": "given_username",
        "password": "given_password",
    }
    # when
    received_response = await treasurehunt_api_client.post("/login", json=given_payload)
    # then
    assert received_response.status_code == status.HTTP_401_UNAUTHORIZED
