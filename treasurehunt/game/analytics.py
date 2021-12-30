from functools import lru_cache
from typing import List

from treasurehunt.game.schemas import (
    TreasureHuntAnalyticsData,
    TreasureHuntAnalyticsDataFilters,
)


class AnalyticsBucket:
    __bucket: List[TreasureHuntAnalyticsData] = []

    def push_analytics_data(self, data: TreasureHuntAnalyticsData) -> None:
        self.__bucket.append(data)

    def get_analytics_data(
        self, filters: TreasureHuntAnalyticsDataFilters
    ) -> List[TreasureHuntAnalyticsData]:
        return [data for data in self.__bucket if self.__filter(data, filters)]

    def __filter(
        self, data: TreasureHuntAnalyticsData, filters: TreasureHuntAnalyticsDataFilters
    ) -> bool:
        return (
            filters.time_from <= data.request_time <= filters.time_to
            and data.distance_to_treasure <= filters.radius
        )


@lru_cache(maxsize=1)
def get_analytics_bucket() -> AnalyticsBucket:
    return AnalyticsBucket()
