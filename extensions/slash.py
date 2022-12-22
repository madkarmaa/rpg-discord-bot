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
    async def test1(self, interaction: Interaction):
        """Test command 1."""
        test = await self.bot._data_database_manager.get_weapons_specials("melee", "Axe")
        # test = await self.bot._data_database_manager.get_weapons_specials("invalid", "test1")
        await interaction.response.send_message(test)

    @app_commands.command()
    async def test2(self, interaction: Interaction):
        """Test command 2."""
        starting_page: int = 0
        embeds = [
            discord.Embed(description="test 1"),
            discord.Embed(description="test 2"),
            discord.Embed(description="test 3"),
            discord.Embed(description="test 4"),
            discord.Embed(description="test 5")
        ]

        await interaction.response.send_message(embed=embeds[starting_page],
                                                view=EmbedPaginator(interaction=interaction,
                                                                    pages=embeds,
                                                                    current_page=starting_page))


async def setup(bot: MyClient):
    await bot.add_cog(Slash(bot))
