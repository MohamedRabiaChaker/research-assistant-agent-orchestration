from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import TypedDict


class ResearchAgent:
    def __init__(self):
        pass


class ValidationAgent:
    def __init__(self):
        pass


class AggregationAgent:
    def __init__(self):
        pass


class TaskType(Enum):
    RESEARECH = ResearchAgent
    VALIDATION = ValidationAgent
    AGGREGATION = AggregationAgent


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Metadata:
    started_at: datetime
    token_cost: int
    retries: int


class TaskState(TypedDict):
    id: str
    type: TaskType
    status: TaskStatus
    depends_on: list[str]
    metadata: Metadata


class OrchestrationPhase(Enum):
    PLAN = "pending"
    EXECUTE = "in_progress"
    AGGREGATE = "completed"


@dataclass
class Finding:
    title: str
    source: str
    content: str
    confidence: float


@dataclass
class State:
    user_input: str
    orchestratrion_phase: OrchestrationPhase
    tasks: list[TaskState]
    facts: list[Finding]
    report: str
