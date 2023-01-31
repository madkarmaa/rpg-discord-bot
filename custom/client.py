"""
Custom module for a Discord client.

`discord.py >= 2.0.0` or a fork with `discord.ext.commands.Bot` is required.
"""

from __future__ import annotations

import discord
from discord import Intents
from discord.ext.commands import Bot
from typing import Any, List, Type, Union, Optional
import os
import logging
import colorama
from colorama import Fore, Back, Style
import glob

from .database import DatabaseManager

LOGGER = logging.getLogger(__name__)
colorama.init()


class MyClient(Bot):
    """Subclass of `discord.ext.commands.Bot`

    Args added:

        Constructor-required:

            `database_manager` (`DatabaseManager`): (Required) The connection to the users database.

            `extensions_folders` (`List[str]`): (Required) A list of folders to include in the extensions loading.

        Not needed to pass in the constructor:

            `is_testing` (`bool`): (Optional) Default is `False`. Whether the client should copy its commands to a testing guild.

            `TEST_GUILD` (`Type[discord.Object]`): (Optional) Default is `None`. If `is_testing` is `True`, then it's required. The guild where the client will copy its commands.
    """

    def __init__(
        self,
        *,
        intents: Intents,
        database_manager: DatabaseManager,
        extensions_folders: List[str],
        is_testing: bool = False,
        test_guild: Optional[discord.Object] = None,
        **options: Any,
    ) -> None:
        # Constructor-required
        self.database_manager = database_manager
        self.extensions_folders = extensions_folders

        # Optional
        self.is_testing = is_testing
        self.TEST_GUILD = test_guild

        return super().__init__(intents=intents, **options)

    async def setup_hook(self) -> None:

        for folder in self.extensions_folders:
            for file_path in glob.glob(os.path.join(folder, "*.py")):

                extension = os.path.basename(file_path).replace(".py", "")
                await self.load_extension(f"{folder}.{extension}")

                LOGGER.log(logging.INFO, f"Loaded {folder}.{extension}")

        self.check_testing()

        await self.tree.sync(guild=self.TEST_GUILD if self.is_testing else None)

        LOGGER.log(logging.INFO, "Synced commands.")
        print(f"{Fore.GREEN}Synced commands{Style.RESET_ALL}")

    def check_testing(self) -> None:
        """Checks whether the bot should be in testing mode or not.

        Raises:
            `IncompleteTestingError`: Raised if the testing parameters are incomplete/missing.
        """

        if self.is_testing and self.TEST_GUILD is not None:
            self.tree.copy_global_to(guild=self.TEST_GUILD)

            LOGGER.log(logging.WARN, "The bot is in testing mode.")
            print(f"{Fore.BLACK}{Back.RED}The bot is in testing mode.{Style.RESET_ALL}")

        elif self.is_testing and self.TEST_GUILD is None:
            raise IncompleteTestingError(1)

        elif not self.is_testing and self.TEST_GUILD is not None:
            raise IncompleteTestingError(2)

    async def close(self) -> None:
        LOGGER.log(logging.WARN, "The bot has been turned off.")
        print(f"{Fore.WHITE}{Back.RED}The bot has been turned off.{Style.RESET_ALL}")
        return await super().close()


class IncompleteTestingError(Exception):
    """Bot testing setup error.

    Args:
        `option` (`int`, optional): 1 or 2, the message to display. Defaults to 0 (generic message).

    Message formats:
        `option = 1`: Missing 'TEST_GUILD' parameter. Please make 'is_testing' False or provide a 'TEST_GUILD' parameter.

        `option = 2`: Unnecessary 'TEST_GUILD' parameter. Please make 'is_testing' True or make 'TEST_GUILD' None.
    """

    def __init__(self, option: int = 0) -> None:
        self.option = option

    def __str__(self) -> str:
        if self.option == 1:
            return "Missing 'TEST_GUILD' parameter. Please make 'is_testing' False or provide a 'TEST_GUILD' parameter."
        elif self.option == 2:
            return "Unnecessary 'TEST_GUILD' parameter. Please make 'is_testing' True or make 'TEST_GUILD' None."
        else:
            return "Something went wrong but wasn't specified."
