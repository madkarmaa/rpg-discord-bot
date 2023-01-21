"""
Custom module for database management.
"""

from __future__ import annotations

import sqlite3
import colorama
from colorama import Fore, Back, Style
import os
import shutil
import glob
from typing import Type, Any, Optional, List, Dict, Union
import logging
import datetime
import traceback


colorama.init()
# See https://stackoverflow.com/questions/12179271/meaning-of-classmethod-and-staticmethod-for-beginner


class DatabaseManager:
    def __init__(
        self,
        database_file_path: str,
        *,
        database_schema_path: Optional[str] = None,
        database_backups_path: Optional[str] = None,
        LOGGER: Optional[Union[logging.Logger, str]] = None,
    ):
        self.database_file_path = os.path.normpath(database_file_path)
        self.database_schema_path = (
            os.path.normpath(database_schema_path) if database_schema_path else None
        )
        self.database_backups_path = (
            os.path.normpath(database_backups_path) if database_backups_path else None
        )
        self.LOGGER = self.check_logging(LOGGER)

        self.db_already_exists: bool = self.check_database_exists()
        self.is_connected: bool = False
        self.connection = None

    def __enter__(self):
        if not self.is_connected:
            self.connection = self.connect()
            self.load_schema()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_connected:
            self.disconnect()

    def check_logging(
        self, logger: Optional[Union[logging.Logger, str]] = None
    ) -> Optional[logging.Logger]:
        """`Method`\n
        Adds a logger.

        Args:
            `logger` (`Optional[Union[logging.Logger, str]]`): The logger. It can be either the `logger.Logger` instance or the name of the logger. If `NoneType`, prints to console. Defaults to `None`.

        Raises:
            `TypeError`: Raised if the `logger` parameter type isn't `logging.Logger`, `str` or `NoneType`.

        Returns:
            `Optional[logging.Logger]`: The logger, or `NoneType` if not specified.

        Example:
        ```python
        check_logging('my_logger')
        ```
        """
        if logger is None:
            print(f"{Fore.WHITE}{Back.RED}LOGGING TO CONSOLE.{Style.RESET_ALL}")
            return None
        elif isinstance(logger, str):
            return logging.getLogger(logger)
        elif isinstance(logger, logging.Logger):
            return logger
        else:
            raise TypeError(
                f"Logger should be of type {logging.Logger}, {str} or NoneType, got {type(logger)}"
            )

    def log(
        self,
        message: str,
        *,
        level: Optional[int] = None,
        error: Optional[Exception] = None,
    ) -> None:
        """`Method`\n
        Logs a message.

        Args:
            `message` (`str`): The message to log.

            `level` (`int`, optional): The severity level of the log message. Defaults to `None`.

            `error` (`Exception`, optional): The exception that you can provide when `level` is `logging.ERROR`. Defaults to `None`.

        Example:
        ```python
        log("This is a warning.", level=logging.WARNING)
        ```
        """
        right_now = datetime.datetime.now()
        right_now = right_now.strftime(r"[%H-%M-%S]")

        if self.LOGGER is not None:

            if level == logging.ERROR:
                self.LOGGER.log(
                    level,
                    message,
                    exc_info=(type(error), error, error.__traceback__)
                    if error is not None
                    else None,
                )

            else:
                self.LOGGER.log(level, message)

        else:

            if error is not None:
                print(
                    f"{Fore.RED}{right_now}: {Fore.WHITE}{Back.RED}{message}{Back.RESET}{Fore.RED}"
                )
                traceback.print_exception(type(error), error, error.__traceback__)
                print(Style.RESET_ALL)

            else:
                print(f"{Fore.GREEN}{right_now}{Style.RESET_ALL}: {message}")

    def connect(self) -> sqlite3.Connection:
        """`Method`\n
        Connects to the database.

        Raises:
            `sqlite3.Error`: Raised if the connection fails.

        Returns:
            `sqlite3.Connection`: The connection to the database.

        Example:
        ```python
        connect()
        ```
        """
        self.log("Attempting connection to the database...", level=logging.INFO)

        try:
            conn: sqlite3.Connection = sqlite3.connect(self.database_file_path)
            self.db_already_exists = self.check_database_exists()
            self.is_connected = True
            return conn

        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            self.is_connected = False
            self.log("Error connecting to the database.", level=logging.ERROR, error=e)
            raise e

        finally:
            if self.is_connected:
                self.log(
                    f"Successfully connected to {self.database_file_path}",
                    level=logging.INFO,
                )

    def disconnect(self) -> None:
        """`Method`\n
        Disconnects from the database.

        Raises:
            `sqlite3.Error`: Raised if the disconnection fails.

        Example:
        ```python
        disconnect()
        ```
        """
        self.log("Attempting to disconnect from the database...", level=logging.INFO)

        try:
            self.connection.commit()
            self.connection.close()

        except sqlite3.Error as e:
            self.log(
                "Error disconnecting from the database.", level=logging.ERROR, error=e
            )
            raise e

        finally:
            self.is_connected = False

            if not self.is_connected:
                self.log(
                    "Successfully disconnected from the database.", level=logging.INFO
                )

    def check_database_exists(self) -> bool:
        """`Method`\n
        Checks if the database file already exists.

        Returns:
            `bool`: `True` if present, `False` otherwise.

        Example:
        ```python
        check_database_exists()
        ```
        """
        return os.path.isfile(self.database_file_path)

    def load_schema(self, *, overwrite: bool = False) -> None:
        """`Method`\n
        Loads the schema given in the constructor.

        Args:
            `overwrite` (`bool`, optional): Creates a backup file of the database and then overwrites the main database schema. USE WITH CAUTION, it can lead to corruption/data loss. Defaults to `False`.

        Example:
        ```python
        load_schema(overwrite=True)
        ```
        """
        if self.database_schema_path is None or (
            not overwrite and self.db_already_exists
        ):
            self.log(
                "No database schema was provided, or overwrite is disabled. Skipping this step."
            )
            return

        if overwrite and self.db_already_exists:
            self.log(
                "Database schema overwrite is enabled, PROCEED WITH CAUTION!",
                level=logging.WARNING,
            )
            self.backup()

        elif self.db_already_exists:
            self.log("Loading database schema for the first time.", level=logging.INFO)

        with open(self.database_schema_path) as s:
            schema = s.read()

        self.connection.executescript(schema)
        self.connection.commit()

        self.log(
            f"Successfully loaded {self.database_schema_path} schema.",
            level=logging.INFO,
        )

    def backup(self) -> None:
        """`Method`\n
        Creates a backup file of the database.

        Example:
        ```python
        backup()
        ```
        """
        self.log("Creating a database backup...", level=logging.INFO)
        right_now = datetime.datetime.now()
        right_now = right_now.strftime(r"[%d-%m-%Y]_-_[%H-%M-%S]")

        file_name = os.path.basename(self.database_file_path)

        backup_path = os.path.normpath(
            os.path.join(self.database_backups_path, f"{right_now}_-_{file_name}.bak")
        )

        self.disconnect()

        shutil.copy2(self.database_file_path, backup_path)
        self.log("Database backup complete.", level=logging.INFO)

        self.connection = self.connect()

    def recover(self) -> None:
        """`Method`\n
        Restores the database using the last backup file.\n
        Note that this method will overwrite the current database file, so use it with caution.

        Example:
        ```python
        recover()
        ```
        """
        self.log("Recovering the latest database backup...", level=logging.INFO)

        backup_files = glob.glob(os.path.join(self.database_backups_path, "*.bak"))
        if not backup_files:
            self.log("No backup files found!", level=logging.WARNING)
            return

        backup_file = max(backup_files, key=os.path.getctime)

        self.disconnect()

        # DEBUG: self.database_file_path -> "./databases/recovery.db"
        shutil.copy2(backup_file, self.database_file_path)
        self.log("Database recovery complete.", level=logging.INFO)

        self.connection = self.connect()


class TableNotFoundError(Exception):
    def __init__(self, table: str):
        self.table = table

    def __str__(self) -> str:
        return f"Table '{self.table}' not found in the database."
