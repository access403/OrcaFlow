"""HTTP endpoints for manager task routing."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, field_validator

from backend.agents.manager_orca import ManagerOrca, ManagerResult
from backend.api.dependencies import get_manager

router = APIRouter()


class ManagerTaskRequest(BaseModel):
    task: str

    @field_validator("task")
    @classmethod
    def validate_task(cls, task: str) -> str:
        normalized_task = task.strip()
        if not normalized_task:
            raise ValueError("Task must not be empty.")
        return normalized_task


@router.post("/manager/tasks", response_model=ManagerResult)
def manage_task(
    request: ManagerTaskRequest,
    manager: ManagerOrca = Depends(get_manager),
) -> ManagerResult:
    """Classify a submitted task and select an agent."""
    return manager.invoke(request.task)
