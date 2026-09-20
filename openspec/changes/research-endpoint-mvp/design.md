# Research Endpoint MVP — Design

## Architecture Overview

The orchestrator coordinates a multi-agent workflow. It creates a Workflow object per request, spawns three Tasks (one per agent type), executes them sequentially, and collects findings to return. No database persistence for MVP—all state lives during the request.

## Agent Orchestration Pattern

Sequential execution: create an Orchestrator class with a single public method `execute(topic: str) -> list[Finding]`.

1. Create Workflow with unique ID
2. Create three Task objects (Research, Validation, Aggregation) with dependencies
3. For each task, get the agent from agent_registry
4. Call agent.execute(task, workflow_run), passing task + workflow context
5. Update TaskRun with results (status, output)
6. Pass previous agent's output as input to next agent

No parallelization. If an agent returns empty list, continue anyway (don't halt).

## Data Flow Through Agents

- ResearchAgent input: task.parameters['topic']
- ResearchAgent output: list[Finding]
- ValidationAgent input: previous findings + task context
- ValidationAgent output: list[Finding] (filtered/enriched)
- AggregationAgent input: previous findings + task context
- AggregationAgent output: list[Finding] (final result)

Each agent receives findings from the previous step. Agents are dummy for MVP—they pass data through, maybe transform slightly.

## Status Tracking Implementation

Use TaskRun dataclass for execution records. Set status before and after agent.execute():
- Before: status = IN_PROGRESS
- After: status = COMPLETED (or FAILED on exception)

Track started_at, finished_at for timing. Store output in TaskRun.output.

## Error Handling Strategy

For MVP: No retries. If an agent raises an exception, catch it, mark task as FAILED, store error in TaskRun.errors, return empty findings to user. Log the error.

## API Response Format

POST /research returns:
```json
{
  "findings": [
    {
      "title": "string",
      "source": "string", 
      "content": "string",
      "confidence": 0.95
    }
  ]
}
```

Always return 200 with findings array (may be empty). No error responses in MVP.

## State Management Decisions

- Workflow is mutable during execution (properties set as tasks run)
- TaskRun is mutable (status and output updated as execution progresses)
- Finding objects are immutable (created by agents, not modified)
- No persistence: all state discarded after request completes
