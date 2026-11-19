import pytest
from fastapi.testclient import TestClient

from backend.agents.manager_orca import ManagerOrca
from backend.main import create_app


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

    assert result.model_dump() == {
        "task_type": task_type,
        "selected_agent": selected_agent,
        "execution_plan": result.execution_plan,
    }
    assert result.execution_plan


def test_manager_rejects_empty_task() -> None:
    with pytest.raises(ValueError, match="Task must not be empty"):
        ManagerOrca().invoke("  ")


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
