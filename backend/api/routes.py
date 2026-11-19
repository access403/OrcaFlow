"""HTTP API routes."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, field_validator

from backend.agents.manager_orca import ManagerOrca, ManagerResult
from backend.api.dependencies import get_freellmapi, get_manager
from backend.providers.freellmapi import FreeLLMAPIError, FreeLLMAPIProvider

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


class ProviderTestRequest(BaseModel):
    prompt: str

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, prompt: str) -> str:
        normalized_prompt = prompt.strip()
        if not normalized_prompt:
            raise ValueError("Prompt must not be empty.")
        return normalized_prompt


class ProviderTestResponse(BaseModel):
    response: str


@router.post("/provider/test", response_model=ProviderTestResponse)
def test_provider(
    request: ProviderTestRequest,
    provider: FreeLLMAPIProvider = Depends(get_freellmapi),
) -> ProviderTestResponse:
    """Run a connectivity test through the FreeLLMAPI provider."""
    try:
        response = provider.complete(request.prompt)
    except FreeLLMAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return ProviderTestResponse(response=response)
