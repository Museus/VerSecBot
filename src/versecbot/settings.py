from os import getenv
from typing import Tuple, Type, Optional
from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


IS_CONTAINER = getenv("IS_CONTAINER", False)

if IS_CONTAINER:
    CONFIG_FILE = "/app/config.toml"
    ENV_FILE = "/app/.env"
else:
    CONFIG_FILE = "../deploy/config.toml"
    ENV_FILE = "../deploy/.env"


class PluginSettings(BaseModel):
    model_config = SettingsConfigDict(extra="allow")
    enabled: bool


class WatcherSettings(PluginSettings):
    enabled: bool
    channel_id: int | None


@lru_cache()
def get_settings() -> "Settings":
    return Settings()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        env_prefix="bot_",
        extra="ignore",
        toml_file=CONFIG_FILE,
    )

    api_token: str
    plugins: Optional[dict[str, PluginSettings]]

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls),
        )


settings = Settings()
