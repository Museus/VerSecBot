from settings import PluginSettings, WatcherSettings


class HandlerSettings(WatcherSettings):
    enabled: bool
    emoji_id: int
    create_thread: bool


class HandlePersonalBestSettings(PluginSettings):
    handlers: list[HandlerSettings]
