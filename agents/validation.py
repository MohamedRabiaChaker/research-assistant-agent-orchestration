import time

from state import Task, WorkflowRun


class ValidationAgent:
    def execute(self, task: Task, workflow_run: WorkflowRun):
        print(f"Starting validation for task {task.id}")
        time.sleep(5)
        print(f"Validation for task {task.id} complete")
        pass
