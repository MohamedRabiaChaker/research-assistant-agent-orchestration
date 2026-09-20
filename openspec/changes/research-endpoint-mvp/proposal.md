# Research Endpoint MVP

## Why

Establish a working end-to-end orchestration flow to validate the research workflow pattern. This baseline allows us to iterate on individual agents and add capabilities vertically without redesigning the orchestrator itself.

## What

Create a `/research` POST endpoint that:
- Accepts a research topic from the user
- Orchestrates dummy agents (ResearchAgent → ValidationAgent → AggregationAgent) in sequence
- Returns aggregated findings to the user
- Executes synchronously

## Impact

- Users can trigger research workflows through a simple API
- Establishes orchestration pattern for multi-agent coordination
- Enables vertical iteration: next chunks add real agent logic, not orchestrator redesign
- Foundation for workflow state tracking and execution

## Out of Scope (Next Iterations)

- Real agent implementations (Research queries, Validation logic, Aggregation synthesis)
- Async/polling model or workflow history
- Error recovery and retries
- Concurrent workflow management
