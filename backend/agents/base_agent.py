"""Framework-neutral contract for agent implementations."""

from abc import ABC, abstractmethod
from typing import Any, Mapping


class BaseAgent(ABC):
    """Common interface for agents backed by LangGraph, CrewAI, or both."""

    @abstractmethod
    def invoke(self, inputs: Mapping[str, Any]) -> Any:
        """Run the agent with the supplied inputs."""
