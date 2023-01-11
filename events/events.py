from __future__ import annotations

import discord
from discord.ext import commands
import colorama
from colorama import Fore, Back, Style
import logging
import asyncio
import json
import os

from custom.client import MyClient

colorama.init()
DSLOGGER = logging.getLogger("discord")


class Events(commands.Cog):
    def __init__(self, bot: MyClient):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        DSLOGGER.log(logging.INFO, f"Logged in as {self.bot.user}")
        print(
            f"{Fore.CYAN}Logged in as {Fore.BLACK}{Back.CYAN}{self.bot.user}{Style.RESET_ALL}"
        )

    async def cog_load(self):
        self.task_change_status = self.bot.loop.create_task(self.loop_change_status())

    async def cog_unload(self):
        self.task_change_status.cancel()

    async def loop_change_status(self) -> None:
        await self.bot.wait_until_ready()

        statuses: list[str] = ["slash commands!", "your mom :)"]

        while not self.bot.is_closed():
            for status in statuses:
                await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching, name=status
                    ),
                    status=discord.Status.idle,
                )
                await asyncio.sleep(10)


async def setup(bot: MyClient):
    await bot.add_cog(Events(bot))
