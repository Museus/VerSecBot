import logging

logger = logging.getLogger("discord")


def get_plugin_logger(plugin_name: str) -> logging.Logger:
    plugin_logger = logger.getChild(plugin_name)
    plugin_logger.info("Initialized logger for plugin %s", plugin_name)
    return plugin_logger
