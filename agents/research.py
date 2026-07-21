import random
import time

from state import Finding


class ResearchAgent:
    def execute(self, task, workflow_run):

        print(f"Researching {task.parameters['topic']}")

        time.sleep(random.randint(1, 3))

        return [
            Finding(
                title=task.parameters["topic"],
                source="Dummy",
                content="Lorem ipsum",
                confidence=1.0,
            )
        ]
