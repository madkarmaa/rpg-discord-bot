"""
Custom module for exceptions.

`discord.py >= 2.0.0` or a fork with `discord.app_commands.errors.AppCommandError` is required.
"""

from __future__ import annotations
from discord.app_commands.errors import AppCommandError
from typing import Any


class InvalidItem(AppCommandError):
    """Raised when no item is found in the database."""

    def __init__(self, item: Any) -> None:
        self.item = item

    def __str__(self) -> str:
        return f"Cannot find '{self.item}'."


class InvalidRGBColor(AppCommandError):
    """Raised when the given RGB Color is invalid."""

    def __init__(self, color: Any) -> None:
        self.color = color

    def __str__(self) -> str:
        return f"RGB values must be between 0 and 255 (invalid values: {self.color})."


class UserNotFoundError(AppCommandError):
    """Raised when a user is not found in the database."""

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    def __str__(self) -> str:
        return f"User with ID '{self.user_id}' not found in the database."
