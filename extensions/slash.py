import discord
from discord.ext import commands
from discord import Interaction, app_commands

from custom.client import MyClient
from custom.paginator import EmbedPaginator


class Slash(commands.Cog):

    def __init__(self, bot: MyClient):
        self.bot = bot

    @app_commands.command()
    async def ping(self, interaction: Interaction):
        """Check the bot's latency."""
        await interaction.response.send_message(f'\U0001f4e1 My latency is **{round(self.bot.latency * 1000)}ms**')

    @app_commands.command()
    async def test(self, interaction: Interaction):
        """Test command."""
        test = await self.bot._data_database_manager.get_weapons_specials("melee", "Axe")
        # test = await self.bot._data_database_manager.get_weapons_specials("invalid", "test1")
        await interaction.response.send_message(test)

    @app_commands.command()
    async def test2(self, interaction: Interaction):
        embeds = [
            discord.Embed(description="test 1"),
            discord.Embed(description="test 2"),
            discord.Embed(description="test 3")
        ]

        await EmbedPaginator().start(ctx=interaction, pages=embeds)


async def setup(bot: MyClient):
    await bot.add_cog(Slash(bot))
