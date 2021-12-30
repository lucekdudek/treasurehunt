import time

from fastapi import Request


async def add_time_started_state(request: Request, call_next):
    request.state.time_started = time.time()
    response = await call_next(request)
    return response
