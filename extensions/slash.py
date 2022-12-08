import discord
from discord.ext import commands
from discord import Interaction, app_commands

from src.client import MyClient


class Slash(commands.Cog):
    def __init__(self, bot: MyClient):
        self.bot = bot

    @app_commands.command()
    async def ping(self, interaction: Interaction):
        """Check the bot's latency."""
        await interaction.response.send_message(f'\U0001f4e1 My latency is **{round(self.bot.latency * 1000)}ms**')

    
    @app_commands.command()
    async def test(self, interaction: Interaction):
        test = await self.bot._data_database_manager.get_weapons_specials("melee", "test1")
        # test = await self.bot._data_database_manager.get_weapons_specials("invalid", "test1")
        await interaction.response.send_message(test)


async def setup(bot: MyClient):
    await bot.add_cog(Slash(bot))
