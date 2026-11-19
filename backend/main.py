"""FastAPI application entry point."""

from fastapi import FastAPI

from backend.agents.manager_orca import ManagerOrca
from backend.api.routes import router as api_router
from backend.database.database import SQLiteDatabase
from backend.settings import Settings


def create_app(
    settings: Settings | None = None,
    database: SQLiteDatabase | None = None,
    manager: ManagerOrca | None = None,
) -> FastAPI:
    """Build the application with replaceable runtime dependencies."""
    app_settings = settings or Settings.from_env()
    app = FastAPI(title=app_settings.app_name)
    app.state.settings = app_settings
    app.state.database = database or SQLiteDatabase(app_settings.database_path)
    app.state.manager = manager or ManagerOrca()
    app.include_router(api_router)
    return app


app = create_app()
