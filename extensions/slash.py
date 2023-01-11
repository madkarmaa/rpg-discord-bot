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


#    @app_commands.command()
#    async def test1(self, interaction: Interaction):
#        """Test command 1."""
#        test = await self.bot._data_database_manager.get_weapons_specials(
#            "melee", "Axe"
#        )
#        # test = await self.bot._data_database_manager.get_weapons_specials("invalid", "test1")
#        await interaction.response.send_message(test)
#
#    @app_commands.command()  # ? See https://discordpy.readthedocs.io/en/stable/interactions/api.html#decorators
#    @app_commands.rename(weapon_name="weapon")
#    @app_commands.describe(
#        weapon_name="The base weapon to search its special variants from."
#    )
#    async def test2(self, interaction: Interaction, weapon_name: str):
#        """Test command 2."""
#        starting_page: int = 0
#        rows: list[
#            dict[str, Any]
#        ] = await self.bot._data_database_manager.get_weapons_specials(
#            "melee", weapon_name
#        )
#        embeds: list[discord.Embed] = []
#
#        if not rows:
#            raise InvalidItem(weapon_name)
#
#        for weapon in rows:
#            image_path: str = weapon.get("image_path")
#            main_image_color: tuple = ColorThief(f".\\{image_path}").get_color(1)
#
#            embed: discord.Embed = discord.Embed(
#                title=weapon.get("name"),
#                description=weapon.get("description"),
#                color=self.bot._data_database_manager.rgb_to_hex(main_image_color),
#            )
#
#            url: str = self.bot._data_database_manager.fix_urls(
#                f"https://raw.githubusercontent.com/madkarmaa/rpg-discord-bot/dev/{image_path}"
#            )
#
#            embed.set_image(
#                url=url
#            )  # TODO When on 'master' change the branch in the url
#
#            embeds.append(embed)  # FIXME Handle invalid column names
#
#        await interaction.response.send_message(
#            embed=embeds[starting_page],
#            view=EmbedPaginator(
#                interaction=interaction, pages=embeds, current_page=starting_page
#            ),
#        )
#
#    @test2.autocomplete("weapon_name")
#    async def test2_autocomplete(self, interaction: Interaction, current: str) -> list:
#        client: MyClient = interaction.client
#        weapons: dict = await client._data_database_manager.get_column_from_table(
#            "melee", "name"
#        )
#        names_list: list[str] = [name.get("name") for name in weapons]
#
#        all_choices: list[Choice] = [
#            Choice(name=weapon_name, value=weapon_name) for weapon_name in names_list
#        ]
#        startswith: list = [
#            c for c in all_choices if current.startswith(c.name.lower())
#        ]
#
#        return (startswith or all_choices)[:25]


async def setup(bot: MyClient):
    await bot.add_cog(Slash(bot))
