import typer
from pydantic import SecretStr
from rich.table import Table

from discord_utils.client import DiscordClient
from discord_utils.console import console
from discord_utils.enums import CommandType
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

app = typer.Typer()

commands_app = typer.Typer()
app.add_typer(commands_app, name="commands")


@commands_app.command("ls")
def list_commands():
    discord_commands = client.commands()

    table = Table(title="Commands")
    table.add_column("id")
    table.add_column("name")
    table.add_column("description")

    for command in discord_commands:
        table.add_row(command.id, command.name, command.description)

    console.print(table)


@commands_app.command("add")
def add_command(name: str, type_: CommandType, description: str = ""):
    data = {
        "name": name,
        "type": int(type_),
    }

    if type_ == CommandType.CHAT_INPUT:
        data["description"] = description

    console.print(client.add_command(data))


@commands_app.command("rm")
def delete_command(id_: str):
    client.delete_command(id_)
    console.print("ok!")


app()
