"""Application configuration."""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    app_name: str = "OrcaFlow API"
    database_path: Path = Path("backend/database/orcaflow.sqlite3")
    freellmapi_base_url: str | None = None
    freellmapi_api_key: str | None = None
    freellmapi_model: str | None = None

    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables."""
        return cls(
            app_name=os.getenv("ORCAFLOW_APP_NAME", cls.app_name),
            database_path=Path(
                os.getenv("ORCAFLOW_DATABASE_PATH", str(cls.database_path))
            ),
            freellmapi_base_url=os.getenv("FREELLMAPI_BASE_URL"),
            freellmapi_api_key=os.getenv("FREELLMAPI_API_KEY"),
            freellmapi_model=os.getenv("FREELLMAPI_MODEL"),
        )
