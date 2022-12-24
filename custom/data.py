"""
Custom module for database management.

`aiosqlite >= 0.18.0` is required.
"""

from __future__ import annotations

import aiosqlite
from os.path import abspath, isfile
from typing import Type, Any, Optional, List, Dict
import logging

DSLOGGER = logging.getLogger("discord")
# See https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner


def fix_urls(string: str) -> str:
    """`Method`\n
    Function to remove spaces and fix backslashes from an url string.

    Args:
        `string` (`str`): The incomplete/invalid url string.

    Returns:
        `str`: The valid url string.

    Example:
    ```
    fix_urls('https://example.com\wrong slash and spaces')
    ```
    """
    no_spaces: str = string.replace(" ", "%20")
    slashes: str = no_spaces.replace("\\", "/")
    return slashes


def rgb_to_hex(color: tuple) -> int:
    """`Method`\n
    Function to convert a RGB color (tuple of 3 items) into an hexadecimal color.

    Args:
        `color` (`tuple`): The tuple containing the 3 RGB values.

    Raises:
        `ValueError`: Raised if the RGB values are invalid (less than 0 or greater than 255).

    Returns:
        `int`: The hexadecimal color.

    Example:
    ```
    rgb_to_hex((12, 25, 38)) # Returns 0x0c1926
    ```
    """
    invalid_values = [val for val in color if val < 0 or val > 255]
    if invalid_values:
        raise ValueError(f'RGB values must be between 0 and 255 (invalid values: {invalid_values})')

    r, g, b = color

    hex_r = hex(r)[2:].zfill(2)
    hex_g = hex(g)[2:].zfill(2)
    hex_b = hex(b)[2:].zfill(2)

    hex_color = '0x' + hex_r + hex_g + hex_b

    return int(hex_color, 16)


class DatabaseManager:

    def __init__(self, *, database_file_path: str, database_schema_path: str | None = None):
        self.database_file_path: Type[str] = abspath(database_file_path)
        self.database_schema_path = abspath(database_schema_path) if database_schema_path is not None else None
        self._database_connection: aiosqlite.Connection | None = None
        self._is_connected: bool = False
        self._db_already_exists: bool = False

    async def __aenter__(self):
        DSLOGGER.log(logging.INFO, "Attempting connection to the database...")

        if isfile(self.database_file_path):
            self._db_already_exists = True

        if not self._is_connected:
            self._database_connection = await aiosqlite.connect(self.database_file_path)
            self._is_connected = True
        else:
            DSLOGGER.log(logging.WARN, "You're already connected to a database!")

        if self._is_connected:
            DSLOGGER.log(logging.INFO, f"Successfully connected to {self.database_file_path}")

        if self.database_schema_path is not None and not self._db_already_exists:
            DSLOGGER.log(logging.INFO, "Attempting to load schema...")
            await self.__load_schema(self.database_schema_path)
            DSLOGGER.log(logging.INFO, f"Successfully loaded {self.database_schema_path} schema.")

        elif self.database_schema_path is not None and self._db_already_exists:
            DSLOGGER.log(logging.WARN, "Database file already exists, skipping schema...")

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        DSLOGGER.log(logging.INFO, "Attempting to disconnect from the database...")

        if self._is_connected:
            await self._database_connection.close()
            self._is_connected = False
        else:
            DSLOGGER.log(logging.WARN, "You are not connected to any database!")

        if not self._is_connected:
            DSLOGGER.log(logging.INFO, "Successfully disconnected from the database.")

    async def _create_cursor(self) -> aiosqlite.Cursor:
        """`Async method`\n
        Create a new cursor using the given database connection.

        Returns:
            `aiosqlite.Cursor`: The new cursor to be used.

        Example:
        ```
        await _create_cursor()
        ```
        """
        cursor: aiosqlite.Cursor = await self._database_connection.cursor()
        return cursor

    async def _validate_table_name(self, table: str) -> None:
        """`Async method`\n
        Check if a table exists in the database, else throw an error.

        Args:
            `table` (`str`): The name of the table.

        Raises:
            `ValueError`: Raised if the table doesn't exist in the database.

        Example:
        ```
        await _validate_table_name('melee')
        ```
        """
        cursor: aiosqlite.Cursor = await self._create_cursor()

        await cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        table_names = [table_name[0] for table_name in await cursor.fetchall()]

        await cursor.close()

        if table not in table_names:
            raise ValueError(f"Invalid table name '{table}'")

    async def __load_schema(self, schema: str) -> None:
        """`Async method`\n
        Internal private method to load a given schema into a database.

        Args:
            schema (str): The path to the schema file.

        Example:
        ```
        await __load_schema('path\\to\\file\\schema.sql')
        ```
        """
        with open(schema) as s:
            _schema = s.read()

        await self._database_connection.executescript(_schema)
        await self._database_connection.commit()

    async def get_column_from_table(self, table_name: str, column_name: str) -> List[Dict[str, Any]]:

        cursor: aiosqlite.Cursor = await self._create_cursor()
        table: str = table_name.lower()
        column_n: str = column_name.lower()

        await self._validate_table_name(table)

        await cursor.execute(f"SELECT {column_n} FROM {table}")

        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in await cursor.fetchall()]

        await cursor.close()

        return rows


class ItemsDatabaseManager(DatabaseManager):

    def __init__(self, *, database_file_path: str, database_schema_path: str | None = None):
        super().__init__(database_file_path=database_file_path, database_schema_path=database_schema_path)

    async def get_weapons_specials(self, table_name: str, base_weapon_name: str) -> List[Dict[str, Any]]:
        """`Async method`\n
        Method to get all the special variants of a given base weapon.

        Args:
            `table` (`str`): The table to get the data from (melee, ranged, ...).
            
            `base_weapon` (`str`): The name of the base weapon to get all its special variants.

        Returns:
            `List[Dict[str, Any]]`: A list of data.

        Example:
        ```
        await get_weapon_specials('melee', 'axe')
        ```
        """

        cursor: aiosqlite.Cursor = await self._create_cursor()
        table: str = table_name.lower()
        base_weapon: str = base_weapon_name.title()

        await self._validate_table_name(table)

        await cursor.execute(
            f"""
            SELECT {table}_specials.* FROM {table}
            INNER JOIN {table}_specials
            ON {table}.id = {table}_specials.id_{table}
            WHERE {table}.name = ?
        """, (base_weapon, ))

        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in await cursor.fetchall()]

        await cursor.close()

        return rows