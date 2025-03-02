from discord import Message

from client import client
from jobs import Watcher, registry
from log_util import logger
from settings import get_settings

from plugins.personal_bests import HandlePersonalBestsPlugin

message_handlers: list[Watcher] = []

settings = get_settings()

for plugin in registry.plugins.values():
    plugin.initialize(settings.plugins[plugin.name], client)
    message_handlers.extend(plugin.on_message)


@client.event
async def on_ready():
    logger.info(f"We have logged in as {client.user}")


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    for hook in message_handlers:
        if hook.should_act(message):
            await hook.act(message)


client.run(token=settings.api_token)
