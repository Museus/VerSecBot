from importlib.metadata import entry_points, distributions
from logging import getLogger, StreamHandler

from discord import Message
from versecbot_interface import PluginRegistry

from versecbot.client import client
from versecbot.settings import get_settings

logger = getLogger("discord").getChild("versecbot")

registry = PluginRegistry()


discovered_plugins = entry_points(group="versecbot.plugins")
for plugin in discovered_plugins:
    logger.info(f"Discovered plugin: {plugin.name}")
    loaded = plugin.load()
    registry.register(loaded)


settings = get_settings()


@client.event
async def on_ready():
    logger.info(f"We have logged in as {client.user}")
    logger.info("Initializing plugins...")
    logger.info(registry.plugins)

    for plugin in registry.plugins.values():
        logger.info("Initializing plugin:", plugin.name)
        plugin_settings = settings.plugins.get(plugin.name)
        logger.info("Plugin settings:", plugin_settings)
        if plugin_settings is None:
            logger.warning(
                f"Plugin {plugin.name} is not configured. Add a section to the config file to enable it."
            )
            continue
        logger.info("Calling initialize")
        plugin.initialize(settings.plugins[plugin.name], client)


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    for plugin in registry.plugins.values():
        for hook in plugin.get_watchers():
            if hook.should_act(message):
                await hook.act(message)


for entry_point in entry_points():
    print(entry_point)

client.run(token=settings.api_token, log_handler=StreamHandler(), log_level="INFO")
