from __future__ import annotations

import asyncio
import discord
import logging
import datetime
from dotenv import load_dotenv
from os import environ
from pyfiglet import figlet_format
from discord.ext import commands
from discord.utils import setup_logging

from custom.client import MyClient
from custom.database import DatabaseManager

load_dotenv()

rightNow = datetime.datetime.now()
rightNow = rightNow.strftime(r"%d-%m-%Y_%H-%M-%S")
file_handler: logging.Handler = logging.FileHandler(
    filename=f"./logs/log_{rightNow}.log", encoding="utf-8", mode="w"
)

setup_logging(
    handler=file_handler,
    level=logging.INFO,
)

mg = DatabaseManager(
    "./databases/test.db",
    database_schema_path="./databases/schemas/schema.sql",
    database_backups_path="./databases/backups/",
)

mg.logging_setup(  # FIXME I don't know why this creates duplicate log messages
    handler=file_handler,
)

client = MyClient(
    command_prefix=commands.when_mentioned_or(
        "my_message_content_perm_must_be_disabled"
    ),
    intents=discord.Intents.default(),
    database_manager=mg,
    extensions_folders=["events", "extensions"],
    is_testing=True,
    test_guild=discord.Object(environ["TEST_GUILD"]),
)


async def main() -> None:
    async with client, client.database_manager:
        await client.start(environ["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
