"""SQLite connection factory."""

import sqlite3
from pathlib import Path


class SQLiteDatabase:
    """Creates SQLite connections for dependency injection."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def connect(self) -> sqlite3.Connection:
        """Open a connection to the configured SQLite database."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(self.path)
