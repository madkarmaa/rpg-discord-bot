"""
Custom module for exceptions.

`discord.py >= 2.0.0` or a fork with `discord.app_commands.errors.AppCommandError` is required.
"""

from __future__ import annotations
from discord.app_commands.errors import AppCommandError


class InvalidItem(AppCommandError):
    """Raised when no item is found in the database."""

    def __init__(self, item):
        self.item = item

    def __str__(self):
        return f"Cannot find '{self.item}'."
