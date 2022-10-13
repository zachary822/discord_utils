import json
from typing import Optional

import requests
import typer
from rich.table import Table

from discord_utils.console import console
from discord_utils.enums import CommandType

app = typer.Typer()


@app.command("ls")
def list_commands(ctx: typer.Context):
    discord_commands = ctx.obj.client.commands()

    table = Table(title="Commands")
    table.add_column("id")
    table.add_column("name")
    table.add_column("type")
    table.add_column("description")

    for command in discord_commands:
        table.add_row(command.id, command.name, str(command.type), command.description)

    console.print(table)


@app.command("add")
def add_command(
    ctx: typer.Context,
    name: str,
    type_: CommandType = typer.Argument(..., metavar="TYPE"),
    description: str = typer.Argument(""),
    options: Optional[str] = typer.Option(None),
):
    data = {
        "name": name,
        "type": int(type_),
    }

    if options:
        data["options"] = json.loads(options)

    if type_ == CommandType.CHAT_INPUT:
        data["description"] = description

    try:
        console.print(ctx.obj.client.add_command(data))
    except requests.HTTPError as e:
        console.print(e.response.text)


@app.command("rm")
def delete_command(ctx: typer.Context, id_: str):
    ctx.obj.client.delete_command(id_)
    console.print("ok!")
