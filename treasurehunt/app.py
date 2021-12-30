from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from treasurehunt.auth.routes import auth_router
from treasurehunt.game.routes import (
    treasure_hunt_api_limiter,
    treasure_hunt_router,
)
from treasurehunt.middlewares import add_time_started_state

app = FastAPI()
app.state.limiter = treasure_hunt_api_limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.middleware("http")(add_time_started_state)

app.include_router(auth_router)
app.include_router(treasure_hunt_router)
