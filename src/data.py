import re
import aiosqlite
import discord
from os.path import abspath, isfile
from typing import Type, Any, Optional, List, Dict
import logging

DSLOGGER = logging.getLogger("discord")
# See https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner

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
        """
        with open(schema) as s:
            _schema = s.read()

        await self._database_connection.executescript(_schema)
        await self._database_connection.commit()


class ItemsDatabaseManager(DatabaseManager):
    def __init__(self, *, database_file_path: str, database_schema_path: str | None = None):
        super().__init__(database_file_path=database_file_path, database_schema_path=database_schema_path)


    async def get_weapons_specials(self, table: str, base_weapon: str) -> List[Dict[str, Any]]:
        """`Async method`\n
        Function to get all the special variants of a given base weapon.

        Args:
            `table` (`str`): The table to get the data from (melee, ranged, ...).
            
            `base_weapon` (`str`): The name of the base weapon to get all its special variants.

        Returns:
            `List[Dict[str, Any]]`: A list of data.
        """

        cursor: aiosqlite.Cursor = await self._create_cursor()

        await self._validate_table_name(table)

        await cursor.execute(f"""
            SELECT {table}_specials.* FROM {table}
            INNER JOIN {table}_specials
            ON {table}.id = {table}_specials.is_from
            WHERE {table}.name = ?
        """, (base_weapon,))

        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in await cursor.fetchall()]

        await cursor.close()

        return rows