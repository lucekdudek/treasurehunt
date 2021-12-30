from datetime import datetime
from typing import List

from aiohttp import ClientSession
from pydantic import BaseModel, Field

from treasurehunt.settings import TREASUREHUNT_SETTINGS


class MailHogMessageRaw(BaseModel):
    sender: str = Field(..., alias="From")
    recipients: List[str] = Field(..., alias="To")
    data: str = Field(..., alias="Data")


class MailHogMessage(BaseModel):
    id: str = Field(..., alias="ID")
    created: datetime = Field(..., alias="Created")
    raw: MailHogMessageRaw = Field(..., alias="Raw")


class MailHogResponse(BaseModel):
    items: List[MailHogMessage]


class MailHogClient:
    __session: ClientSession

    async def __aenter__(self):
        self.__session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__session.close()

    async def get_messages(self) -> MailHogResponse:
        async with self.__session.get(
            f"http://{TREASUREHUNT_SETTINGS.smtp_host}:8025/api/v2/messages"
        ) as response:
            response_json = await response.json(content_type="text/json")
            return MailHogResponse(**response_json)

    async def delete_messages(self) -> None:
        res = await self.__session.delete(
            f"http://{TREASUREHUNT_SETTINGS.smtp_host}:8025/api/v1/messages"
        )
        assert res.status == 200, "Cannot delete MailHog messages"
