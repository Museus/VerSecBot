from discord import Message

from .client import client
from .jobs import Watcher, registry
from .log_util import logger
from .settings import get_settings

from importlib.metadata import entry_points

discovered_plugins = entry_points(group="versecbot.plugins")
for plugin in discovered_plugins:
    plugin.load()

message_handlers: list[Watcher] = []

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
        message_handlers.extend(plugin.on_message)


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    for hook in message_handlers:
        if hook.should_act(message):
            await hook.act(message)


client.run(token=settings.api_token, log_handler=None)
