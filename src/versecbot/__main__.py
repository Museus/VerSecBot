from importlib.metadata import entry_points

from discord import Message
from versecbot_interface import Watcher, PluginRegistry

from .client import client
from .log_util import logger
from .settings import get_settings


registry = PluginRegistry()

plugins = ["smile_back", "personal_bests"]

discovered_plugins = entry_points(group="versecbot.plugins")
for plugin in (p for p in discovered_plugins if p.name in plugins):
    loaded = plugin.load()
    registry.register(loaded)


settings = get_settings()


@client.event
async def on_ready():
    logger.info(f"We have logged in as {client.user}")
    logger.info("Initializing plugins...")

    for plugin in registry.plugins.values():
        plugin_settings = settings.plugins.get(plugin.name)
        if plugin_settings is None:
            logger.warning(
                f"Plugin {plugin.name} is not configured. Add a section to the config file to enable it."
            )
            continue
        plugin.initialize(settings.plugins[plugin.name], client)


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    for plugin in registry.plugins.values():
        for hook in plugin.get_watchers():
            if hook.should_act(message):
                await hook.act(message)


client.run(token=settings.api_token, log_handler=None)
