import discord
import logging

discord.utils.setup_logging(level=logging.INFO)

logger = logging.getLogger("discord")
plugin_root_logger = logger.getChild("plugins")


def get_plugin_logger(plugin_name: str) -> logging.Logger:
    plugin_logger = plugin_root_logger.getChild(plugin_name)
    plugin_logger.debug("Initialized logger for plugin %s", plugin_name)
    return plugin_logger
