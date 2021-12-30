import time
from typing import Callable, Optional

import pytest

from treasurehunt.game.analytics import AnalyticsBucket, get_analytics_bucket
from treasurehunt.game.schemas import APILocationIn, TreasureHuntAnalyticsData


@pytest.fixture
def analytics_bucket():
    bucket = get_analytics_bucket()
    bucket._InMemoryAuthRepository__bucket = []  # type: ignore
    yield bucket
    bucket._InMemoryAuthRepository__bucket = []  # type: ignore


@pytest.fixture
def analytics_factory(
    analytics_bucket: AnalyticsBucket,
) -> Callable:
    def create_analytics(
        request_time: Optional[float] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        distance_to_treasure: Optional[int] = None,
    ) -> None:
        analytics_bucket.push_analytics_data(
            TreasureHuntAnalyticsData(
                request_time=request_time or time.time(),
                user_id="user_id",
                hunter_email="foo@bar.com",
                hunter_location=APILocationIn(
                    latitude=latitude or 0, longitude=longitude or 0
                ),
                distance_to_treasure=distance_to_treasure or 5,
            )
        )

    return create_analytics
