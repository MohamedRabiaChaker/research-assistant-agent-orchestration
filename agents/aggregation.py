import time

from state import Task, WorkflowRun


class AggregationAgent:
    def execute(self, task: Task, workflow_run: WorkflowRun):
        print(f"Starting aggregation for task {task.id}")
        time.sleep(5)
        print(f"Aggregation for task {task.id} complete")
        pass
