import uuid
from datetime import datetime

from agents import AggregationAgent, ResearchAgent, ValidationAgent
from state import Finding, Task, TaskRun, TaskStatus, TaskType, Workflow, WorkflowRun


class Orchestrator:
    def __init__(self, registry=None):
        if registry is None:
            registry = {
                TaskType.AGGREGATION: AggregationAgent,
                TaskType.RESEARECH: ResearchAgent,
                TaskType.VALIDATION: ValidationAgent,
            }
        self.agent_registry = registry

    def execute(self, topic: str) -> list[Finding]:
        workflow_id = str(uuid.uuid4())
        workflow = Workflow(
            id=workflow_id,
            tasks=[],
            user_input=topic,
            workflow_runs=[]
        )

        workflow_run = WorkflowRun(
            started_at=datetime.now(),
            finished_at=None,
            total_tokens=0,
            current_step="research",
            logs=[],
            report={},
            knowledge=[],
            tasks=[]
        )

        task_types = [TaskType.RESEARECH, TaskType.VALIDATION, TaskType.AGGREGATION]
        findings = []

        for idx, task_type in enumerate(task_types):
            task = self._create_task(task_type, idx, workflow_id, topic)
            workflow.tasks.append(task)
            workflow_run.tasks.append(task)

            task_run = self._execute_task(task, workflow_run)
            findings = task_run.output or []

        workflow_run.finished_at = datetime.now()
        workflow.workflow_runs.append(workflow_run)

        return findings

    def _create_task(self, task_type: TaskType, index: int, workflow_id: str, topic: str) -> Task:
        task_id = f"{workflow_id}-{task_type.value}-{index}"
        dependencies = [] if index == 0 else [f"{workflow_id}-{TaskType.RESEARECH.value}-{index-1}"]

        return Task(
            id=task_id,
            type=task_type,
            depends_on=dependencies,
            runs=[],
            workflow=workflow_id,
            parameters={"topic": topic}
        )

    def _execute_task(self, task: Task, workflow_run: WorkflowRun) -> TaskRun:
        task_run = TaskRun(
            taskid=task.id,
            task_run_id=str(uuid.uuid4()),
            status=TaskStatus.IN_PROGRESS,
            started_at=datetime.now(),
            finished_at=None,
            retires=0,
            errors=[],
            output=None,
            runtime_prarmeters=task.parameters
        )

        try:
            agent_class = self.agent_registry[task.type]
            agent = agent_class()
            output = agent.execute(task, workflow_run)
            task_run.output = output
            task_run.status = TaskStatus.COMPLETED
        except Exception as e:
            task_run.status = TaskStatus.FAILED
            task_run.errors.append({"message": str(e), "type": type(e).__name__})

        task_run.finished_at = datetime.now()
        task.runs.append(task_run)

        return task_run
