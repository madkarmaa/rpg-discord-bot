"""
Custom module for `discord.Embed` message pagination.

`discord.py >= 2.0.0` or a fork with `discord.ui.View`, `discord.ui.Button` and `discord.Embed` is required.
"""

from __future__ import annotations

import discord
from discord.ext import commands
from discord.ui import Button, button, View
from discord import ButtonStyle, Emoji, PartialEmoji, Interaction
import logging
from typing import Optional, Union, Any, List


class EmbedPaginator(View):

    def __init__(self,
                 *,
                 interaction: Interaction,
                 pages: List[discord.Embed],
                 timeout: int = 60,
                 current_page: int = 0,
                 external_input: bool = False,
                 ephemeral: bool = False) -> None:

        self.external_input = external_input
        self.ephemeral = ephemeral
        self.pages = pages
        self.interaction = interaction
        self.current_page = current_page

        self.total_page_count = len(pages)
        self.page_counter = PageCounter(current_page=current_page, total_pages=len(pages))

        super().__init__(timeout=timeout)

        self.add_item(self.page_counter)  # TODO maybe move the button to the middle of the navigation buttons
        self._update_buttons()

    def _update_buttons(self) -> None:
        """`Method`\n
        Method to apply edits to buttons when other buttons are pressed.

        Example:
        ```
        _update_buttons()
        ```
        """
        self.first_button.disabled = (self.current_page == 0)
        self.previous_button.disabled = (self.current_page == 0)
        self.page_counter.label = f"{self.current_page + 1}/{self.total_page_count}"
        self.next_button.disabled = (self.current_page == self.total_page_count - 1)
        self.last_button.disabled = (self.current_page == self.total_page_count - 1)

    @button(label="<<", style=ButtonStyle.success)
    async def first_button(self, interaction: Interaction, button: Button):
        self.current_page = 0
        self._update_buttons()

        await interaction.response.defer()
        await self.interaction.edit_original_response(embed=self.pages[self.current_page], view=self)

    @button(label="<", style=ButtonStyle.primary)
    async def previous_button(self, interaction: Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
        self._update_buttons()

        await interaction.response.defer()
        await self.interaction.edit_original_response(embed=self.pages[self.current_page], view=self)

    @button(label=">", style=ButtonStyle.primary)
    async def next_button(self, interaction: Interaction, button: Button):
        if self.current_page < self.total_page_count - 1:
            self.current_page += 1
        self._update_buttons()

        await interaction.response.defer()
        await self.interaction.edit_original_response(embed=self.pages[self.current_page], view=self)

    @button(label=">>", style=ButtonStyle.success)
    async def last_button(self, interaction: Interaction, button: Button):
        self.current_page = self.total_page_count - 1
        self._update_buttons()

        await interaction.response.defer()
        await self.interaction.edit_original_response(embed=self.pages[self.current_page], view=self)


class PageCounter(Button):

    def __init__(self, style: ButtonStyle = ButtonStyle.grey, *, total_pages: int, current_page: int):
        super().__init__(label=f"{current_page + 1}/{total_pages}", style=style, disabled=True)
