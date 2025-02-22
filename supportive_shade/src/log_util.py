import logging

logger = logging.getLogger("discord")


def get_plugin_logger(plugin_name: str) -> logging.Logger:
    return logger.getChild(plugin_name)
