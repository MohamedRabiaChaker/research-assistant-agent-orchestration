# Research Endpoint MVP — Implementation Tasks

## Phase 1: Core Orchestrator

1. Create `engine/orchestrator.py` with Orchestrator class
2. Implement `__init__` to store agent_registry (passed in or imported)
3. Implement `execute(topic: str) -> list[Finding]` method
4. Inside execute: generate unique workflow ID, instantiate Workflow object
5. Test: Verify Orchestrator can be instantiated

## Phase 2: Workflow & Task Creation

6. Inside execute: create three Task objects (one per agent type: Research, Validation, Aggregation)
7. Set task.parameters = {"topic": topic}
8. Create one WorkflowRun object to track overall execution
9. Initialize each task's TaskRun with status=PENDING
10. Test: Verify workflow and tasks are created correctly

## Phase 3: Agent Execution

11. Loop through tasks in order (Research, Validation, Aggregation)
12. For each task: get agent class from agent_registry
13. Instantiate agent, call agent.execute(task, workflow_run)
14. Update task's TaskRun: status=IN_PROGRESS before, status=COMPLETED after
15. Store agent output in TaskRun.output
16. Pass previous task's output as input to next task (modify task.parameters or findings list)
17. Test: Verify agents execute in sequence, data threads through

## Phase 4: Endpoint Integration

18. Update main.py POST /research endpoint
19. Extract topic from request: `request.prompt` (or similar from ResearchRequest model)
20. Instantiate Orchestrator, call orchestrator.execute(topic)
21. Return findings in response format: `{"findings": orchestrator_output}`
22. Test: Verify endpoint accepts POST, returns findings

## Phase 5: Verification

23. Manual test: curl POST /research with {"topic": "test"}
24. Verify response is 200 with findings array
25. Verify all three agents executed (check logs/prints)
26. Verify findings have all required fields: title, source, content, confidence
