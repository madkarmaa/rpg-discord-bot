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
from custom.data import DatabaseManager, ItemsDatabaseManager

load_dotenv()

rightNow = datetime.datetime.now()
rightNow = rightNow.strftime(r"LOG_date_{%d-%m-%Y}_started_at_{%H-%M-%S}")

setup_logging(
    handler=logging.FileHandler(
        filename=f"./logs/{rightNow}.log", encoding="utf-8", mode="w"
    ),
    level=logging.INFO,
)

client = MyClient(
    command_prefix=commands.when_mentioned_or(
        "my_message_content_perm_must_be_disabled"
    ),
    intents=discord.Intents.default(),
    _user_database_manager=DatabaseManager(  # TODO set real database manager
        database_file_path="./databases/users.db",
        database_schema_path="./databases/schemas/users_db_schema.sql",
    ),
    _data_database_manager=ItemsDatabaseManager(
        database_file_path="./databases/items.db",
        database_schema_path="./databases/schemas/items_db_schema.sql",
    ),
    _extensions_folders=["events", "extensions"],
    _is_testing=True,
    TEST_GUILD=discord.Object(environ["TEST_GUILD"]),
)


async def main() -> None:
    async with client, client._user_database_manager, client._data_database_manager:
        await client.start(environ["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
