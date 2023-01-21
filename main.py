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
rightNow = rightNow.strftime(r"LOG_date_{%d-%m-%Y}_started_at_{%H-%M-%S}")

setup_logging(
    handler=logging.FileHandler(
        filename=f"./logs/{rightNow}.log", encoding="utf-8", mode="w"
    ),
    level=logging.INFO,
)

mg = DatabaseManager(
    "./databases/test.db",
    database_schema_path="./databases/schemas/items_db_schema.sql",
    database_backups_path="./databases/backups/",
    logger=logging.getLogger("discord"),
)

client = MyClient(
    command_prefix=commands.when_mentioned_or(
        "my_message_content_perm_must_be_disabled"
    ),
    intents=discord.Intents.default(),
    database_manager=mg,
    _extensions_folders=["events", "extensions"],
    _is_testing=True,
    TEST_GUILD=discord.Object(environ["TEST_GUILD"]),
)


async def main() -> None:
    async with client:
        with client.database_manager:
            await client.start(environ["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
