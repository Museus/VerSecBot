from src.jobs import Plugin

from .settings import HandlePersonalBestSettings


class HandlePersonalBests(Plugin):
    name: str = "personal_bests"
    settings = HandlePersonalBestSettings
