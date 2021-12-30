import time
from typing import Callable, Dict

import pytest
from httpx import AsyncClient
from starlette import status

from treasurehunt.game.schemas import Hunter


@pytest.mark.asyncio
async def test_post_treasure_hunt_ok(
    treasurehunt_api_client: AsyncClient, test_hunter: Hunter
):
    # given
    given_payload = {
        "latitude": 19.945800,
        "longitude": 50.051200,
    }
    given_params = {"email": test_hunter.email}
    expected_distance = 10
    # when
    received_response = await treasurehunt_api_client.post(
        "/treasure-hunt", params=given_params, json=given_payload
    )
    # then
    assert received_response.status_code == status.HTTP_202_ACCEPTED
    assert received_response.json().get("distance") == expected_distance


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "given_payload,given_params",
    [
        ({}, {}),
        ({"latitude": 19.945704, "longitude": 50.051227}, {"email": "not-an-email"}),
        ({"latitude": 19.945704}, {"email": "test@email.com"}),
    ],
)
async def test_post_treasure_hunt_unprocessable_entity(
    given_payload: Dict, given_params: Dict, treasurehunt_api_client: AsyncClient
):
    # when
    received_response = await treasurehunt_api_client.post(
        "/treasure-hunt", params=given_params, json=given_payload
    )
    # then
    assert received_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_post_treasure_hunt_too_many_requests(
    treasurehunt_api_client: AsyncClient,
):
    # given
    given_payload = {
        "latitude": 19.945800,
        "longitude": 50.051200,
    }
    given_params_too_many_requests = {"email": "too@many.requests"}
    given_params_normal_request = {"email": "very@normal.request"}
    # when
    for _ in range(20):
        await treasurehunt_api_client.post(
            "/treasure-hunt", params=given_params_too_many_requests, json=given_payload
        )
    received_too_many_requests_response = await treasurehunt_api_client.post(
        "/treasure-hunt", params=given_params_too_many_requests, json=given_payload
    )
    received_accepted_response = await treasurehunt_api_client.post(
        "/treasure-hunt", params=given_params_normal_request, json=given_payload
    )
    # then
    assert (
        received_too_many_requests_response.status_code
        == status.HTTP_429_TOO_MANY_REQUESTS
    )
    assert received_accepted_response.status_code == status.HTTP_202_ACCEPTED


@pytest.mark.asyncio
async def test_get_analytics_empty(
    treasurehunt_api_client: AsyncClient,
):
    # given
    given_params = {"start_time": time.time(), "end_time": time.time(), "radius": 0}
    # when
    received_response = await treasurehunt_api_client.get(
        "/analytics", params=given_params
    )
    # then
    assert received_response.status_code == status.HTTP_200_OK
    assert len(received_response.json().get("requests")) == 0


@pytest.mark.asyncio
async def test_get_analytics_ok(
    treasurehunt_api_client: AsyncClient,
    analytics_factory: Callable,
):
    # given
    given_number_of_requests = 5
    start_time = time.time()
    for _ in range(given_number_of_requests):
        analytics_factory(request_time=time.time(), distance_to_treasure=5)
        analytics_factory(distance_to_treasure=15)
        analytics_factory(request_time=start_time - 1)
        analytics_factory(request_time=start_time + 60)
    given_params = {"start_time": start_time, "end_time": time.time(), "radius": 10}
    # when
    received_response = await treasurehunt_api_client.get(
        "/analytics", params=given_params
    )
    # then
    assert received_response.status_code == status.HTTP_200_OK
    assert len(received_response.json().get("requests")) == given_number_of_requests
