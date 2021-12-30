from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Dict, Optional

from treasurehunt.auth.exceptions import AuthException
from treasurehunt.auth.schemas import AuthDetails


class AuthRepository(ABC):
    @abstractmethod
    async def create_user(self, auth_details: AuthDetails) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read_user(self, user_id: str) -> Optional[AuthDetails]:
        raise NotImplementedError


class InMemoryAuthRepository(AuthRepository):
    __users: Dict[str, AuthDetails] = {}

    async def create_user(self, auth_details: AuthDetails) -> None:
        if auth_details.user_id in self.__users:
            raise AuthException("User with this id already exists")
        self.__users[auth_details.user_id] = auth_details

    async def read_user(self, user_id: str) -> Optional[AuthDetails]:
        return self.__users.get(user_id)


@lru_cache(maxsize=1)
def get_in_memory_auth_repository_singleton() -> InMemoryAuthRepository:
    return InMemoryAuthRepository()
