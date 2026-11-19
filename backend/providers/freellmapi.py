"""FreeLLMAPI OpenAI-compatible provider."""

import os
from collections.abc import Callable
from typing import Any

import httpx


class FreeLLMAPIError(RuntimeError):
    """Raised when FreeLLMAPI cannot complete a provider request."""


class FreeLLMAPIProvider:
    """Provider adapter for an OpenAI-compatible FreeLLMAPI endpoint."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        post: Callable[..., Any] | None = None,
    ) -> None:
        self.base_url = (
            base_url if base_url is not None else os.getenv("FREELLMAPI_BASE_URL")
        )
        self.api_key = (
            api_key if api_key is not None else os.getenv("FREELLMAPI_API_KEY")
        )
        self.model = model if model is not None else os.getenv("FREELLMAPI_MODEL")
        self._post = post

    def complete(self, prompt: str) -> str:
        """Send a chat-completions request and return the assistant text."""
        normalized_prompt = prompt.strip()
        if not normalized_prompt:
            raise ValueError("Prompt must not be empty.")
        if not self.base_url:
            raise FreeLLMAPIError(
                "FREELLMAPI_BASE_URL is required."
            )
        if not self.model:
            raise FreeLLMAPIError("FREELLMAPI_MODEL is required.")

        url = self.base_url.rstrip("/")
        if not url.endswith("/chat/completions"):
            url = f"{url}/chat/completions"

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": normalized_prompt}],
        }

        try:
            post = self._post or httpx.post
            response = post(url, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise FreeLLMAPIError(f"FreeLLMAPI request failed: {exc}") from exc

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise FreeLLMAPIError(
                "FreeLLMAPI returned an invalid chat-completions response."
            ) from exc

        if isinstance(content, list):
            content = "".join(
                part.get("text", "")
                for part in content
                if isinstance(part, dict)
            )
        if not isinstance(content, str):
            raise FreeLLMAPIError(
                "FreeLLMAPI returned an invalid chat-completions response."
            )
        return content

