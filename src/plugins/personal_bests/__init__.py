from jobs import Plugin
from discord import Intents

from .settings import HandlePersonalBestSettings, HandlerSettings
from .main import HandlePersonalBest
from .logging import logger


class HandlePersonalBestsPlugin(Plugin):
    name: str = "personal_bests"
    settings = HandlePersonalBestSettings
    intents = [Intents.guild_messages]

    on_message = list

    def __init__(self):
        self.on_message = []

    def initialize(self, settings: HandlePersonalBestSettings, client):
        logger.info(
            "Initializing Personal Best Reactions plugin...",
        )

        # Register Personal Best Reactions
        for handler_settings_raw in settings.handlers:
            handler_settings = HandlerSettings.model_validate(handler_settings_raw)
            if not handler_settings.enabled:
                continue

            try:
                pb_handler = HandlePersonalBest(client, handler_settings)
            except Exception:
                logger.exception(
                    "Failed to initialize Personal Bests handler for channel %s",
                    handler_settings.channel_id,
                )
            else:
                self.on_message.append(pb_handler)
                logger.info(
                    "Handling personal bests in #%s with Emoji: %s",
                    pb_handler.channel,
                    pb_handler.emoji,
                )

        logger.debug("Personal Bests initialized")
