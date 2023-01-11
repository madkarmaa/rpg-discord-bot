from __future__ import annotations

import discord
from discord import Intents
from discord.ext.commands import Bot
from typing import Any, List, Type, Union
import os
import logging
import colorama
from colorama import Fore, Back, Style

from .data import DatabaseManager, ItemsDatabaseManager

DSLOGGER = logging.getLogger("discord")


class MyClient(Bot):
    """Subclass of `discord.ext.commands.Bot`

    Args added:

        Constructor-required:

            `_user_database_manager` (`Type[DatabaseManager]`): (Required) The connection to the users database.

            `_data_database_manager` (`Type[DatabaseManager]`): (Required) The connection to the data (items, ...) database.

            `_extensions_folders` (`List[str]`): (Required) A list of folders to include in the extensions loading.

        Not needed to pass in the constructor:

            `_is_testing` (`bool`): (Optional) Default is `False`. Whether the client should copy its commands to a testing guild.

            `TEST_GUILD` (`Type[discord.Object]`): (Optional) Default is `None`. If `_is_testing` is `True`, then it's required. The guild where the client will copy its commands.
    """

    def __init__(
        self,
        *,
        intents: Intents,
        _user_database_manager: Type[
            DatabaseManager
        ],  # TODO Change to specific database manager
        _data_database_manager: ItemsDatabaseManager,
        _extensions_folders: List[str],
        _is_testing: bool = False,
        TEST_GUILD: Type[discord.Object] | None = None,
        **options: Any,
    ) -> None:
        # Constructor-required
        self._user_database_manager: Type[DatabaseManager] = _user_database_manager
        self._data_database_manager: ItemsDatabaseManager = _data_database_manager
        self._extensions_folders: List[str] = _extensions_folders

        # Optional
        self._is_testing: bool = _is_testing
        self.TEST_GUILD: Type[discord.Object] | None = TEST_GUILD

        super().__init__(intents=intents, **options)

    async def setup_hook(self) -> None:

        for folder in self._extensions_folders:
            for extension in [
                file.replace(".py", "")
                for file in os.listdir(folder)
                if os.path.isfile(os.path.join(folder, file))
            ]:
                await self.load_extension(f"{folder}.{extension}")
                DSLOGGER.log(logging.INFO, f"Loaded {folder}.{extension}")

        if self._is_testing and self.TEST_GUILD is not None:
            DSLOGGER.log(logging.WARN, "The bot is in testing mode.")
            print(f"{Fore.BLACK}{Back.RED}The bot is in testing mode.{Style.RESET_ALL}")
            self.tree.copy_global_to(guild=self.TEST_GUILD)

        elif self._is_testing and self.TEST_GUILD is None:
            raise TypeError(
                "Missing 'TEST_GUILD' parameter. Please make '_is_testing' False or provide a 'TEST_GUILD' parameter."
            )

        elif not self._is_testing and self.TEST_GUILD is not None:
            raise TypeError(
                "Unnecessary 'TEST_GUILD' parameter. Please make '_is_testing' True or make 'TEST_GUILD' None."
            )

        await self.tree.sync(guild=self.TEST_GUILD)
        DSLOGGER.log(logging.INFO, "Synced commands.")
        print(f"{Fore.GREEN}Synced commands{Style.RESET_ALL}")

    async def close(self) -> None:
        DSLOGGER.log(logging.WARN, "The bot has been turned off.")
        print(f"{Fore.WHITE}{Back.RED}The bot has been turned off.{Style.RESET_ALL}")
        return await super().close()
