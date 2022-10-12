from types import SimpleNamespace

import typer
from pydantic import SecretStr

from discord_utils.client import DiscordClient
from discord_utils.commands.commands import app as commands_app
from discord_utils.settings import CustomBaseSettings


class Settings(CustomBaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: SecretStr
    SCOPE: str

    class Config:
        parameter_path = "/discord"
        env_file = ".env"


settings = Settings()

client = DiscordClient(settings.CLIENT_ID, settings.CLIENT_SECRET.get_secret_value(), settings.SCOPE)

context_obj = SimpleNamespace(client=client)

app = typer.Typer(context_settings={"obj": context_obj})

app.add_typer(commands_app, name="commands")

app()
