from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from agents import AggregationAgent, ResearchAgent, ValidationAgent


class TaskType(Enum):
    RESEARECH = "research"
    VALIDATION = "validation"
    AGGREGATION = "aggregation"


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


agent_registry = {
    TaskType.AGGREGATION: AggregationAgent,
    TaskType.RESEARECH: ResearchAgent,
    TaskType.VALIDATION: ValidationAgent,
}


@dataclass
class Workflow:
    id: str
    tasks: list[Task]
    started_at: datetime
    finished_at: datetime
    total_tokens: int
    current_step: str


@dataclass
class ExecutionError:
    timestamp: datetime
    message: str
    traceback: str
    recoverable: str


@dataclass
class Task:
    id: str
    type: TaskType
    depends_on: list[str]
    runs: list[TaskRun]
    workflow: str


@dataclass
class Finding:
    title: str
    source: str
    content: str
    confidence: float


@dataclass
class TaskRun:
    taskid: str
    task_run_id: str
    status: TaskStatus
    started_at: datetime
    finished_at: datetime
    retires: int
    errors: list[dict]
    output: list[Finding] | None
    runtime_prarmeters: dict


@dataclass
class State:
    user_input: str
    tasks: list[Task]
    facts: list[Finding]
    report: str
