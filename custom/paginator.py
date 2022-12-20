from __future__ import annotations

import discord
from discord.ext import commands


class PaginatorPageCounter(discord.ui.Button):

    def __init__(self, style: discord.ButtonStyle = discord.ButtonStyle.grey, *, total_pages: int, initial_page: int):
        super().__init__(label=f"{initial_page + 1}/{total_pages}", style=style, disabled=True)


class EmbedPaginator(discord.ui.View):

    def __init__(self,
                 *,
                 timeout: int = 60,
                 previous_button: discord.ui.Button = discord.ui.Button(label="<", style=discord.ButtonStyle.primary),
                 next_button: discord.ui.Button = discord.ui.Button(label=">", style=discord.ButtonStyle.primary),
                 first_button: discord.ui.Button = discord.ui.Button(label="<<", style=discord.ButtonStyle.success),
                 last_button: discord.ui.Button = discord.ui.Button(label=">>", style=discord.ButtonStyle.success),
                 initial_page: int = 0,
                 external_input: bool = False,
                 ephemeral: bool = False) -> None:

        self.previous_button = previous_button
        self.next_button = next_button
        self.first_button = first_button
        self.last_button = last_button
        self.initial_page = initial_page
        self.external_input = external_input
        self.ephemeral = ephemeral

        self.pages = None
        self.ctx = None
        self.message = None
        self.current_page = None
        self.page_counter = None
        self.total_page_count = None

        super().__init__(timeout=timeout)

    async def start(self, ctx: discord.Interaction | commands.Context, pages: list[discord.Embed]):

        if isinstance(ctx, discord.Interaction):  # ? What is this?
            ctx = await commands.Context.from_interaction(ctx)

        self.pages = pages
        self.total_page_count = len(pages)
        self.ctx = ctx
        self.current_page = self.initial_page

        self.previous_button.callback = self.previous_button_callback
        self.next_button.callback = self.next_button_callback
        self.first_button.callback = self.first_button_callback
        self.last_button.callback = self.last_button_callback

        self.page_counter = PaginatorPageCounter(total_pages=self.total_page_count, initial_page=self.initial_page)

        self.add_item(self.first_button)
        self.add_item(self.previous_button)
        self.add_item(self.page_counter)
        self.add_item(self.next_button)
        self.add_item(self.last_button)

        self.message = await ctx.send(embed=self.pages[self.initial_page], view=self, ephemeral=self.ephemeral)

    async def previous(self):
        if self.current_page == 0:
            self.current_page = self.total_page_count - 1
        else:
            self.current_page -= 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def next(self):
        if self.current_page == self.total_page_count - 1:
            self.current_page = 0
        else:
            self.current_page += 1

        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.current_page], view=self)

    async def first(self):
        self.current_page = 0
        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[0], view=self)

    async def last(self):
        self.current_page = self.total_page_count - 1
        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        await self.message.edit(embed=self.pages[self.total_page_count - 1], view=self)

    async def next_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author and self.external_input:
            embed = discord.Embed(description="You cannot control this pagination because you did not execute it.",
                                  color=0xff0000)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.next()
        await interaction.response.defer()

    async def previous_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author and self.external_input:
            embed = discord.Embed(description="You cannot control this pagination because you did not execute it.",
                                  color=0xff0000)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.previous()
        await interaction.response.defer()

    async def first_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author and self.external_input:
            embed = discord.Embed(description="You cannot control this pagination because you did not execute it.",
                                  color=0xff0000)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.first()
        await interaction.response.defer()

    async def last_button_callback(self, interaction: discord.Interaction):
        if interaction.user != self.ctx.author and self.external_input:
            embed = discord.Embed(description="You cannot control this pagination because you did not execute it.",
                                  color=0xff0000)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        await self.last()
        await interaction.response.defer()
