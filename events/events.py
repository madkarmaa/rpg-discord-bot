import discord
from discord.ext import commands
import colorama
from colorama import Fore, Back, Style
import logging

from custom.client import MyClient

colorama.init()
DSLOGGER = logging.getLogger("discord")


class Events(commands.Cog):
    def __init__(self, bot: MyClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="slash commands!"),
            status=discord.Status.idle
        )

        DSLOGGER.log(logging.INFO, f"Logged in as {self.bot.user}")
        print(f"{Fore.CYAN}Logged in as {Fore.BLACK}{Back.CYAN}{self.bot.user}{Style.RESET_ALL}")


async def setup(bot: MyClient):
    await bot.add_cog(Events(bot))