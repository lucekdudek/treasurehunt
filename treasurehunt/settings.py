from functools import lru_cache

from pydantic import BaseSettings


class TreasureHuntSettings(BaseSettings):
    secret_key: str = "SECRET"
    tresurehunt_email: str = "tresure@hunt.game"
    smtp_host: str = "mailhog"
    smtp_port: int = 1025

    class Config:
        env_prefix = "TREASUREHUNT_"


@lru_cache(maxsize=1)
def get_treasurehunt_settings():
    return TreasureHuntSettings()


TREASUREHUNT_SETTINGS = get_treasurehunt_settings()
