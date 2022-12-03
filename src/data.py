import aiosqlite
import discord
from os.path import abspath, isfile
from typing import Type, Any, Optional
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


    async def __create_cursor(self) -> aiosqlite.Cursor:
        """`Async method`\n
        Internal private method to create a new cursor using the given database connection.

        Returns:
            `aiosqlite.Cursor`: The new cursor to be used.
        """
        cursor: aiosqlite.Cursor = await self._database_connection.cursor()
        return cursor


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


class UserDatabaseManager(DatabaseManager):
    def __init__(self, *, database_file_path: str):
        super().__init__(database_file_path=database_file_path)

    async def add_user(self, user: int | discord.user.User | discord.member.Member) -> bool:
        """`Async method`\n
        Create a new user in the database.

        Args:
            `user` (`int | discord.user.User | discord.member.Member`): The user to add to the database.


        Returns:
            `bool`: `True` if successful.
        """
        if isinstance(user, (discord.user.User, discord.member.Member)):
            user = user.id

        async with self.database_connection:
            with await self.__create_cursor() as cursor:
                await cursor.execute('INSERT INTO inventory (user_id) VALUES (:user_id)', {'user_id': user})

        return True


    async def remove_user(self, user: int | discord.user.User | discord.member.Member) -> bool:
        """`Async method`\n
        Remove a user from the database.

        Args:
            `user` (`int | discord.user.User | discord.member.Member`): The user to be removed from the database.

        Returns:
            `bool`: `True` if successful.
        """

        if isinstance(user, (discord.user.User, discord.member.Member)):
            user = user.id

        async with self.database_connection:
            with await self.__create_cursor() as cursor:
                await cursor.execute('DELETE from inventory WHERE user_id = :user_id', {'user_id': user})

        return True


    async def fetch(self, user: int | discord.User, items: list[str]) -> dict:
        """
        Function to fetch a user's item/s from the database.

        Parameters
        ----------

        user: `int` | `discord.user.User` | `discord.member.Member`
            The user to check in the database.

        Returns
        -------
        `dict`:
            The items you've searched and their values.

        Raises
        ------
        `sqlite3.OperationalError` | `aiosqlite.OperationalError`:
            Raised if a column is not found.

        `TypeError`:
            Raised if the user row is not found.

        Example
        -------
        `await fetch(user=user_id, items=['item1', 'item2', 'item3', ...])`
        """

        if isinstance(user, (discord.user.User, discord.member.Member)):
            user = user.id

        # TODO check item = db columns to prevent SQL injections.

        data: dict = {}

        for item in items:
            await self._cursor.execute(f"SELECT {' ,'.join(items)} FROM inventory WHERE user_id = :user_id", {'user_id': user})
            item: dict = {item: (await self._cursor.fetchone())[0]}
            data |= item

        return data


    async def update(self, user: int | discord.user.User | discord.member.Member, **args) -> bool:
        """
        Function to update a user's item/s in the database.

        Parameters
        ----------

        user: `int` | `discord.user.User` | `discord.member.Member`
            The user to be updated in the database.

        Returns
        -------
        `True` if the function has worked.

        Raises
        ------
        `sqlite3.OperationalError` | `aiosqlite.OperationalError`:
            Raised if a column is not found.

        `TypeError`:
            Raised if no arguments are provided (`**args`).

        Example
        -------
        `await update(user=user_id, item1=100, item2=200, item3=300, ...)`
        """

        if isinstance(user, (discord.user.User, discord.member.Member)):
            user = user.id

        if not args:
            raise TypeError(
                'Provide at least 1 argument (read the docs for an example)')

        # TODO check args = db columns to prevent SQL injections.

        for arg, value in args.items():
            await self._cursor.execute(f'UPDATE inventory SET {arg} = :value WHERE user_id = :user_id', {'user_id': user, 'value': value})

        await self.database_connection.commit()

        return True