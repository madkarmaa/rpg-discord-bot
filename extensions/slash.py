from __future__ import annotations
from typing import Any

import discord
from discord.ext import commands
from discord import Interaction, app_commands
from discord.app_commands import Choice
from colorthief import ColorThief

from custom.client import MyClient
from custom.paginator import EmbedPaginator
from custom.exceptions import InvalidItem


class Slash(commands.Cog):
    def __init__(self, bot: MyClient):
        self.bot = bot

    @app_commands.command()
    async def ping(self, interaction: Interaction):
        """Check the bot's latency."""
        await interaction.response.send_message(
            f"\U0001f4e1 My latency is **{round(self.bot.latency * 1000)}ms**"
        )


async def setup(bot: MyClient):
    await bot.add_cog(Slash(bot))
