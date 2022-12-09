import logging
import traceback
from io import BytesIO, StringIO
from typing import Any

from discord import Embed, File, Interaction
from discord.app_commands.errors import AppCommandError, CommandNotFound
from discord.ext import commands

from custom.client import MyClient

DSLOGGER = logging.getLogger("discord")


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

    async def app_command_error(self, interaction: Interaction, error: AppCommandError): # TODO Do more tests for discord.py exceptions.
        embed = None

        # exception_list = traceback.format_exception(type(error), error, error.__traceback__)
        # exception_string = "".join(exception_list).encode("utf-8")

        # if isinstance(error, ):
        #     embed = Embed(description=str(error))

        if embed is not None:
            return await self.send(interaction)(embed=embed)

        elif not isinstance(error, CommandNotFound):
            buffer = StringIO()
            embed = Embed(
                title="It seems like I've ran into a problem.",
                color=0xff0000
            )

            traceback.print_exception(
                type(error), error, error.__traceback__, file=buffer
            )

            buffer.seek(0)
            buffer = BytesIO(buffer.getvalue().encode("utf-8"))

            await self.send(interaction)(
                embed=embed,
                file=File(buffer, "traceback.txt"),
            )

            DSLOGGER.error('Unhandled exception:', exc_info=(type(error), error, error.__traceback__))


async def setup(bot: MyClient):
    await bot.add_cog(Errors(bot))