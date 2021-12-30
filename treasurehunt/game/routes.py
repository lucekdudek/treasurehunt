from fastapi import APIRouter, Body, Depends, Query, Request, WebSocket, status
from geopy import Point
from pydantic import EmailStr
from slowapi import Limiter

from treasurehunt.auth.handlers import AUTH_HANDLER
from treasurehunt.game.analytics import get_analytics_bucket
from treasurehunt.game.exceptions import TreasureHuntException
from treasurehunt.game.schemas import (
    APIGetAnalyticsOut,
    APIGetAnalyticsRequestOut,
    APILocationIn,
    APIMessageStatus,
    APIPostTreasureHuntOut,
    APIPostTreasureHuntOutError,
    Hunter,
    TreasureHuntAnalyticsData,
    TreasureHuntAnalyticsDataFilters,
)
from treasurehunt.game.treasurehunt_factory import TreasureHuntFactory

treasure_hunt_api_limiter = Limiter(key_func=lambda request: request.url)
treasure_hunt_router = APIRouter()


@treasure_hunt_router.post(
    "/treasure-hunt",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=APIPostTreasureHuntOut,
)
@treasure_hunt_api_limiter.limit("20/hour")
async def post_treasure_hunt(
    request: Request,
    user_id=Depends(AUTH_HANDLER.get_user_id),
    analytics_bucket=Depends(get_analytics_bucket),
    email: EmailStr = Query(...),
    current_location: APILocationIn = Body(...),
    treasure_hunt_factory: TreasureHuntFactory = Depends(TreasureHuntFactory),
):
    treasurehunt_game = treasure_hunt_factory.build()
    try:
        distance_to_treasure = await treasurehunt_game.hunt(
            hunter=Hunter(email=email),
            hunter_location=Point(
                latitude=current_location.latitude,
                longitude=current_location.longitude,
            ),
        )
    except TreasureHuntException as err:
        return APIPostTreasureHuntOutError(status=APIMessageStatus.OK, error=str(err))
    analytics_bucket.push_analytics_data(
        TreasureHuntAnalyticsData(
            request_time=request.state.time_started,
            user_id=user_id,
            hunter_email=email,
            hunter_location=current_location,
            distance_to_treasure=distance_to_treasure,
        )
    )
    return APIPostTreasureHuntOut(
        status=APIMessageStatus.OK, distance=distance_to_treasure
    )


@treasure_hunt_router.websocket("/ws/treasure-hunt")
async def follow_game(
    websocket: WebSocket,
    treasure_hunt_factory: TreasureHuntFactory = Depends(TreasureHuntFactory),
):
    treasurehunt_game = treasure_hunt_factory.build()
    await websocket.accept()
    async for message in treasurehunt_game.follow_hunt():
        await websocket.send_text(message)


@treasure_hunt_router.get(
    "/analytics",
    status_code=status.HTTP_200_OK,
    response_model=APIGetAnalyticsOut,
)
async def get_analytics(
    analytics_bucket=Depends(get_analytics_bucket),
    start_time: float = Query(...),
    end_time: float = Query(...),
    radius: int = Query(...),
):
    analytics_data = analytics_bucket.get_analytics_data(
        TreasureHuntAnalyticsDataFilters(
            time_from=start_time, time_to=end_time, radius=radius
        )
    )
    return APIGetAnalyticsOut(
        status=APIMessageStatus.OK,
        requests=[
            APIGetAnalyticsRequestOut(
                email=data.hunter_email,
                current_location=(
                    data.hunter_location.latitude,
                    data.hunter_location.longitude,
                ),
            )
            for data in analytics_data
        ],
    )
