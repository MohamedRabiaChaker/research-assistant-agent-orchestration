from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TaskType(Enum):
    RESEARECH = "research"
    VALIDATION = "validation"
    AGGREGATION = "aggregation"


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Finding:
    title: str
    source: str
    content: str
    confidence: float


@dataclass
class ExecutionError:
    timestamp: datetime
    message: str
    traceback: str
    recoverable: str


@dataclass
class Workflow:
    id: str
    tasks: list[Task]
    user_input: str
    workflow_runs: list[WorkflowRun]


@dataclass
class WorkflowRun:
    started_at: datetime
    finished_at: datetime
    total_tokens: int
    current_step: str
    logs: list[str]
    report: dict
    knowledge: list[dict]
    tasks: list[Task]


@dataclass
class Task:
    id: str
    type: TaskType
    depends_on: list[str]
    runs: list[TaskRun]
    workflow: str
    parameters: dict = None


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
