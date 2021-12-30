from datetime import datetime, timedelta
from functools import lru_cache

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

from treasurehunt.settings import TREASUREHUNT_SETTINGS


class AuthHandler:
    __security_base = HTTPBearer()

    def __init__(self):
        self.__pw_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.__secret = TREASUREHUNT_SETTINGS.secret_key
        self.__algorithm = "HS256"

    def get_password_hash(self, password: str) -> str:
        return self.__pw_hasher.hash(password)

    def verify_password(self, password: str, hash: str) -> bool:
        return self.__pw_hasher.verify(password, hash)

    def encode_token(self, user_id: str) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, hours=1),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, self.__secret, algorithm=self.__algorithm)

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.__secret, algorithms=[self.__algorithm])
            user_id = payload.get("sub")
            assert isinstance(user_id, str), "Decoded token doesn't hold user_id."
            return user_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def get_user_id(
        self, auth: HTTPAuthorizationCredentials = Security(__security_base)
    ) -> str:
        return self.decode_token(auth.credentials)


@lru_cache(maxsize=1)
def get_auth_handler() -> AuthHandler:
    return AuthHandler()


AUTH_HANDLER = get_auth_handler()
