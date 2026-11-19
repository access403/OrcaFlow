"""FastAPI dependency providers."""

import sqlite3
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Request

from backend.agents.manager_orca import ManagerOrca
from backend.database.database import SQLiteDatabase
from backend.providers.freellmapi import FreeLLMAPIProvider
from backend.settings import Settings


def get_manager(request: Request) -> ManagerOrca:
    """Retrieve the configured manager from the application container."""
    return request.app.state.manager


def get_settings(request: Request) -> Settings:
    """Retrieve application settings from the app container."""
    return request.app.state.settings


def get_freellmapi(request: Request) -> FreeLLMAPIProvider:
    """Retrieve the configured FreeLLMAPI provider."""
    return request.app.state.freellmapi


def get_database(request: Request) -> SQLiteDatabase:
    """Retrieve the configured database adapter from the app container."""
    return request.app.state.database


def get_db_connection(
    database: Annotated[SQLiteDatabase, Depends(get_database)],
) -> Iterator[sqlite3.Connection]:
    """Yield a request-scoped SQLite connection and close it afterwards."""
    connection = database.connect()
    try:
        yield connection
    finally:
        connection.close()
