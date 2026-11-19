"""LangGraph workflow for classifying tasks and selecting an agent."""

import re
from typing import Literal, NotRequired, Protocol, TypedDict

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

TaskType = Literal["research", "development", "analysis"]
AgentName = Literal["ResearchOrca", "DeveloperOrca", "AnalystOrca"]


class TaskClassifier(Protocol):
    """Contract for task-classification strategies."""

    def classify(self, task: str) -> TaskType:
        """Return the task category for the supplied task."""


class KeywordTaskClassifier:
    """Classify tasks using configurable, deterministic keyword matching."""

    _KEYWORDS: dict[TaskType, frozenset[str]] = {
        "research": frozenset(
            {"research", "investigate", "explore", "source", "citation", "find", "search", "survey"}
        ),
        "development": frozenset(
            {"implement", "build", "code", "develop", "fix", "refactor", "create", "debug"}
        ),
        "analysis": frozenset(
            {"analyze", "analyse", "evaluate", "compare", "assess", "summarize", "explain", "review"}
        ),
    }
    _TIE_BREAK_ORDER: tuple[TaskType, ...] = ("development", "research", "analysis")

    def classify(self, task: str) -> TaskType:
        words = set(re.findall(r"[a-z]+", task.casefold()))
        scores = {
            task_type: len(words & keywords)
            for task_type, keywords in self._KEYWORDS.items()
        }
        highest_score = max(scores.values())
        if highest_score == 0:
            return "analysis"
        return next(
            task_type
            for task_type in self._TIE_BREAK_ORDER
            if scores[task_type] == highest_score
        )


class ManagerState(TypedDict):
    task: str
    task_type: NotRequired[TaskType]
    selected_agent: NotRequired[AgentName]
    execution_plan: NotRequired[list[str]]


class ManagerResult(BaseModel):
    task_type: TaskType
    selected_agent: AgentName
    execution_plan: list[str]


class ManagerOrca:
    """Classify a task and produce an execution plan using a LangGraph workflow."""

    def __init__(self, classifier: TaskClassifier | None = None) -> None:
        self._classifier = classifier or KeywordTaskClassifier()
        self._graph = self._build_graph()

    def invoke(self, task: str) -> ManagerResult:
        """Return a classification, selected agent, and proposed execution plan."""
        normalized_task = task.strip()
        if not normalized_task:
            raise ValueError("Task must not be empty.")

        result = self._graph.invoke({"task": normalized_task})
        return ManagerResult.model_validate(result)

    def _build_graph(self):
        graph = StateGraph(ManagerState)
        graph.add_node("classify", self._classify_task)
        graph.add_node("research", self._plan_research)
        graph.add_node("development", self._plan_development)
        graph.add_node("analysis", self._plan_analysis)
        graph.add_edge(START, "classify")
        graph.add_conditional_edges(
            "classify",
            self._route_by_task_type,
            {
                "research": "research",
                "development": "development",
                "analysis": "analysis",
            },
        )
        graph.add_edge("research", END)
        graph.add_edge("development", END)
        graph.add_edge("analysis", END)
        return graph.compile()

    def _classify_task(self, state: ManagerState) -> dict[str, TaskType]:
        return {"task_type": self._classifier.classify(state["task"])}

    def _route_by_task_type(self, state: ManagerState) -> TaskType:
        return state["task_type"]

    @staticmethod
    def _plan_research(state: ManagerState) -> dict[str, AgentName | list[str]]:
        return {
            "selected_agent": "ResearchOrca",
            "execution_plan": [
                f"Define research questions for: {state['task']}",
                "Gather and verify relevant evidence",
                "Synthesize findings and note uncertainties",
            ],
        }

    @staticmethod
    def _plan_development(state: ManagerState) -> dict[str, AgentName | list[str]]:
        return {
            "selected_agent": "DeveloperOrca",
            "execution_plan": [
                f"Translate the task into implementation requirements: {state['task']}",
                "Plan focused code changes",
                "Implement the changes and run relevant tests",
            ],
        }

    @staticmethod
    def _plan_analysis(state: ManagerState) -> dict[str, AgentName | list[str]]:
        return {
            "selected_agent": "AnalystOrca",
            "execution_plan": [
                f"Break down the task into questions: {state['task']}",
                "Examine relevant information and evidence",
                "Summarize findings and implications",
            ],
        }
