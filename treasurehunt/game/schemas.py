from enum import Enum
from typing import List, Tuple

from pydantic import BaseModel, EmailStr


class Hunter(BaseModel):
    email: EmailStr


class HuntingEvent(BaseModel):
    hunter: Hunter
    location_str: str
    remaining_distance: int  # meters
    is_winning: bool


class APILocationIn(BaseModel):
    latitude: float
    longitude: float


class APIMessageStatus(Enum):
    OK = "ok"
    ERROR = "error"


class APIPostTreasureHuntOut(BaseModel):
    status: APIMessageStatus
    distance: int = -1


class APIPostTreasureHuntOutError(APIPostTreasureHuntOut):
    error: str


class APIGetAnalyticsRequestOut(BaseModel):
    email: EmailStr
    current_location: Tuple[float, ...]


class APIGetAnalyticsOut(BaseModel):
    status: APIMessageStatus
    requests: List[APIGetAnalyticsRequestOut]


class TreasureHuntAnalyticsData(BaseModel):
    request_time: float
    user_id: str
    hunter_email: EmailStr
    hunter_location: APILocationIn
    distance_to_treasure: int


class TreasureHuntAnalyticsDataFilters(BaseModel):
    time_from: float
    time_to: float
    radius: int
