from abc import ABC, abstractmethod
from discord import Message
from typing import Type

from .client import client
from .settings import WatcherSettings, PluginSettings


class Plugin(ABC):
    name: str
    settings: Type[PluginSettings]

    def __init_subclass__(cls):
        super().__init_subclass__()
        registry.register(cls)


class Watcher(ABC):
    def __init__(self, settings: WatcherSettings):
        self.enabled = settings.enabled
        self.channel = client.get_channel(settings.channel_id)

    @abstractmethod
    def should_act(self, message: Message) -> bool:
        if not self.enabled:
            return False

        if self.channel and message.channel is not self.channel:
            return False

    @abstractmethod
    def act(self, message: Message):
        if not self.should_act(message):
            return

        pass


class PluginRegistry:
    def __init__(self):
        self.plugins: dict[str, Plugin] = []

    def register(self, plugin: Plugin):
        self.plugins[plugin.name] = plugin


registry = PluginRegistry()
