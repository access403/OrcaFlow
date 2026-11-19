import httpx
import pytest
from fastapi.testclient import TestClient

from backend.main import create_app
from backend.providers.freellmapi import FreeLLMAPIError, FreeLLMAPIProvider
from backend.settings import Settings


class FakeResponse:
    def __init__(self, data: dict[str, object] | None = None, status_error: Exception | None = None) -> None:
        self._data = data
        self._status_error = status_error

    def raise_for_status(self) -> None:
        if self._status_error is not None:
            raise self._status_error

    def json(self) -> dict[str, object]:
        assert self._data is not None
        return self._data


def test_provider_loads_configuration_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("FREELLMAPI_BASE_URL", "https://example.test/v1")
    monkeypatch.setenv("FREELLMAPI_API_KEY", "test-key")
    monkeypatch.setenv("FREELLMAPI_MODEL", "test-model")

    provider = FreeLLMAPIProvider()

    assert provider.base_url == "https://example.test/v1"
    assert provider.api_key == "test-key"
    assert provider.model == "test-model"


def test_provider_posts_openai_chat_completion_payload() -> None:
    captured: dict[str, object] = {}

    def fake_post(url: str, **kwargs: object) -> FakeResponse:
        captured["url"] = url
        captured.update(kwargs)
        return FakeResponse(
            {
                "choices": [
                    {"message": {"role": "assistant", "content": "Hello from FreeLLMAPI"}}
                ]
            }
        )

    provider = FreeLLMAPIProvider(
        base_url="https://example.test/v1",
        api_key="test-key",
        model="test-model",
        post=fake_post,
    )

    assert provider.complete("  Hello  ") == "Hello from FreeLLMAPI"
    assert captured["url"] == "https://example.test/v1/chat/completions"
    assert captured["headers"] == {
        "Content-Type": "application/json",
        "Authorization": "Bearer test-key",
    }
    assert captured["json"] == {
        "model": "test-model",
        "messages": [{"role": "user", "content": "Hello"}],
    }


@pytest.mark.parametrize(
    ("response", "message"),
    [
        (FakeResponse({"choices": []}), "invalid chat-completions response"),
        (
            FakeResponse(
                status_error=httpx.HTTPStatusError(
                    "bad status",
                    request=httpx.Request("POST", "https://example.test"),
                    response=httpx.Response(500),
                )
            ),
            "request failed",
        ),
    ],
)
def test_provider_reports_invalid_or_failed_responses(
    response: FakeResponse,
    message: str,
) -> None:
    provider = FreeLLMAPIProvider(
        base_url="https://example.test/v1",
        model="test-model",
        post=lambda *_args, **_kwargs: response,
    )

    with pytest.raises(FreeLLMAPIError, match=message):
        provider.complete("Hello")


def test_provider_test_api_returns_response() -> None:
    provider = FreeLLMAPIProvider(
        base_url="https://example.test/v1",
        api_key="test-key",
        model="test-model",
        post=lambda *_args, **_kwargs: FakeResponse(
            {
                "choices": [
                    {"message": {"role": "assistant", "content": "Provider is ready"}}
                ]
            }
        ),
    )
    client = TestClient(create_app(freellmapi=provider))

    response = client.post("/provider/test", json={"prompt": "Hello"})

    assert response.status_code == 200
    assert response.json() == {"response": "Provider is ready"}


def test_provider_test_api_rejects_blank_prompt() -> None:
    provider = FreeLLMAPIProvider(
        base_url="https://example.test/v1",
        model="test-model",
    )
    client = TestClient(create_app(freellmapi=provider))

    response = client.post("/provider/test", json={"prompt": "  "})

    assert response.status_code == 422


def test_provider_test_api_maps_provider_errors_to_bad_gateway(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("FREELLMAPI_BASE_URL", raising=False)
    monkeypatch.delenv("FREELLMAPI_MODEL", raising=False)
    settings = Settings.from_env()
    client = TestClient(create_app(settings=settings))

    response = client.post("/provider/test", json={"prompt": "Hello"})

    assert response.status_code == 502
