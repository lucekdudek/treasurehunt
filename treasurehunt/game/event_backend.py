import asyncio
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import AsyncGenerator, List

from treasurehunt.game.schemas import HuntingEvent


class EventBackend(ABC):
    @abstractmethod
    async def subscribe(self) -> AsyncGenerator[HuntingEvent, None]:
        raise NotImplementedError
        yield

    @abstractmethod
    async def publish(self, event: HuntingEvent):
        raise NotImplementedError


class QueueEventBackend(EventBackend):
    def __init__(self):
        self.__queues: List[asyncio.Queue] = []

    async def subscribe(self) -> AsyncGenerator[HuntingEvent, None]:
        q: asyncio.Queue = asyncio.Queue()
        self.__queues.append(q)
        try:
            while True:
                event = await q.get()
                yield event
                q.task_done()
        finally:
            self.__queues.remove(q)

    async def publish(self, event: HuntingEvent):
        [await q.put(event) for q in self.__queues]


@lru_cache(maxsize=1)
def get_queue_event_backend_singleton() -> QueueEventBackend:
    return QueueEventBackend()
