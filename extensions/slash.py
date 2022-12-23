from __future__ import annotations

import discord
from discord.ext import commands
from discord import Interaction, app_commands

from custom.client import MyClient
from custom.paginator import EmbedPaginator
from custom.data import fix_urls


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

    @app_commands.command()  # ? See https://discordpy.readthedocs.io/en/stable/interactions/api.html#decorators
    @app_commands.rename(weapon_name="weapon")
    @app_commands.describe(weapon_name="The base weapon to search its special variants from.")
    async def test2(self, interaction: Interaction, weapon_name: str):
        """Test command 2."""
        starting_page: int = 0
        embeds: list[discord.Embed] = []
        for weapon in await self.bot._data_database_manager.get_weapons_specials("melee", weapon_name):

            embed: discord.Embed = discord.Embed(title=weapon.get("name"), description=weapon.get("description"))

            image_path: str = weapon.get("image_path")
            url: str = fix_urls(f"https://raw.githubusercontent.com/madkarmaa/rpg-discord-bot/dev/{image_path}")

            embed.set_image(url=url)  # TODO When on 'master' change the branch in the url

            embeds.append(embed)

        await interaction.response.send_message(embed=embeds[starting_page],
                                                view=EmbedPaginator(interaction=interaction,
                                                                    pages=embeds,
                                                                    current_page=starting_page))


async def setup(bot: MyClient):
    await bot.add_cog(Slash(bot))
