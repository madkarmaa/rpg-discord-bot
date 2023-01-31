from __future__ import annotations

import logging
import traceback
from io import BytesIO, StringIO
from typing import Any
import datetime
from discord import Embed, File, Interaction
from discord.app_commands.errors import AppCommandError, CommandNotFound
from discord.ext import commands

from custom.client import MyClient
from custom.exceptions import InvalidItem

LOGGER = logging.getLogger(__name__)


class Errors(commands.Cog):
    def __init__(self, bot: MyClient):
        self.bot = bot
        self.hidden = True
        bot.tree.error(self.app_command_error)

    def send(self, interaction: Interaction):
        if interaction.response.is_done():
            return interaction.followup.send
        else:
            return interaction.response.send_message

    async def app_command_error(
        self, interaction: Interaction, error: AppCommandError
    ):  # TODO Do more tests for discord.py exceptions.
        embed: Embed | None = None
        rightNow = datetime.datetime.now()
        rightNow = rightNow.strftime("Date: **%d/%m/%Y**\nTime: **%H:%M:%S**")

        if isinstance(error, InvalidItem):
            embed = Embed(title=str(error), color=0xFF0000)

        if embed is not None:
            return await self.send(interaction)(embed=embed)

        elif not isinstance(error, CommandNotFound):
            buffer = StringIO()
            embed = Embed(
                title="Unhandled exception",
                color=0xFF0000,
                description=f"Command: **/{interaction.command.name}**\nUsed by: **[{interaction.user}](https://discord.com/users/{interaction.user.id})**\n{rightNow}",
            )

            traceback.print_exception(
                type(error), error, error.__traceback__, file=buffer
            )

            buffer.seek(0)
            buffer = BytesIO(buffer.getvalue().encode("utf-8"))

            owner_appdetails = await interaction.client.application_info()
            await owner_appdetails.owner.send(
                embed=embed, file=File(buffer, "traceback.txt")
            )

            embed = Embed(
                title="It seems like I've ran into a problem. I've already reported the issue to the developer.",
                color=0xFF0000,
            )

            await self.send(interaction)(embed=embed)

            LOGGER.error(
                "Unhandled exception:",
                exc_info=(type(error), error, error.__traceback__),
            )


async def setup(bot: MyClient):
    await bot.add_cog(Errors(bot))
