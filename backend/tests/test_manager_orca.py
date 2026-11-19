import pytest
from fastapi.testclient import TestClient

from backend.agents.manager_orca import (
    FreeLLMTaskClassifier,
    ManagerOrca,
    TaskType,
)
from backend.main import create_app
from backend.providers.freellmapi import FreeLLMAPIError, FreeLLMAPIProvider


@pytest.mark.parametrize(
    ("task", "task_type", "selected_agent"),
    [
        ("Research renewable energy storage", "research", "ResearchOrca"),
        ("Implement an API endpoint", "development", "DeveloperOrca"),
        ("Compare these two approaches", "analysis", "AnalystOrca"),
        ("Help me plan my next steps", "analysis", "AnalystOrca"),
    ],
)
def test_manager_classifies_and_routes_task(
    task: str,
    task_type: str,
    selected_agent: str,
) -> None:
    result = ManagerOrca().invoke(task)

    assert result.task_type == task_type
    assert result.selected_agent == selected_agent
    assert result.execution_plan
    assert set(result.model_dump()) == {
        "task_type",
        "selected_agent",
        "execution_plan",
    }


def test_manager_rejects_empty_task() -> None:
    with pytest.raises(ValueError, match="Task must not be empty"):
        ManagerOrca().invoke("  ")


def test_manager_uses_injected_classifier() -> None:
    class FixedClassifier:
        def classify(self, _task: str) -> TaskType:
            return "research"

    result = ManagerOrca(classifier=FixedClassifier()).invoke(
        "Implement a data collector"
    )

    assert result.task_type == "research"
    assert result.selected_agent == "ResearchOrca"


def test_manager_api_returns_expected_output_shape() -> None:
    client = TestClient(create_app(manager=ManagerOrca()))

    response = client.post(
        "/manager/tasks",
        json={"task": "Fix a failing test"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "task_type": "development",
        "selected_agent": "DeveloperOrca",
        "execution_plan": [
            "Translate the task into implementation requirements: Fix a failing test",
            "Plan focused code changes",
            "Implement the changes and run relevant tests",
        ],
    }


def test_manager_api_rejects_blank_task() -> None:
    client = TestClient(create_app())

    response = client.post("/manager/tasks", json={"task": "  "})

    assert response.status_code == 422


def test_free_llm_classifier_routes_llm_category() -> None:
    class FixedProvider:
        def complete(self, _prompt: str) -> str:
            return "development"

    classifier = FreeLLMTaskClassifier(FixedProvider())

    assert classifier.classify("Create a new API") == "development"


def test_free_llm_classifier_falls_back_on_provider_error() -> None:
    class FailingProvider:
        def complete(self, _prompt: str) -> str:
            raise FreeLLMAPIError("provider unavailable")

    classifier = FreeLLMTaskClassifier(FailingProvider())

    assert classifier.classify("Research renewable energy") == "research"
    assert classifier.classify("Implement an API endpoint") == "development"


def test_free_llm_classifier_falls_back_on_invalid_category() -> None:
    class InvalidProvider:
        def complete(self, _prompt: str) -> str:
            return "not a valid category"

    classifier = FreeLLMTaskClassifier(InvalidProvider())

    assert classifier.classify("Compare these approaches") == "analysis"


def test_manager_api_uses_free_llm_provider() -> None:
    provider = FreeLLMAPIProvider(
        base_url="https://example.test/v1",
        api_key="test-key",
        model="test-model",
        post=lambda *_args, **_kwargs: FakeProviderResponse(
            {"choices": [{"message": {"content": "research"}}]}
        ),
    )
    client = TestClient(create_app(freellmapi=provider))

    response = client.post(
        "/manager/tasks",
        json={"task": "Investigate energy storage"},
    )

    assert response.status_code == 200
    assert response.json()["task_type"] == "research"
    assert response.json()["selected_agent"] == "ResearchOrca"


class FakeProviderResponse:
    def raise_for_status(self) -> None:
        pass

    def __init__(self, data: dict[str, object]) -> None:
        self._data = data

    def json(self) -> dict[str, object]:
        return self._data
