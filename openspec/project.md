# Project Context

## Tech Stack

- **Language**: Python 3.14+
- **Framework**: FastAPI for HTTP API
- **Agent Orchestration**: LangGraph for workflow coordination
- **LLM/Agent Library**: LangChain for agent implementations
- **Validation/Serialization**: Pydantic for data models
- **Server**: Uvicorn (ASGI)
- **Package Manager**: uv

## Architecture Pattern

**Agent-based orchestration** — Multiple specialized agents collaborate in sequence to solve research tasks.

Core execution model:
- **Workflow**: Top-level container for a research request, tracks overall progress
- **Task**: Unit of work assigned to a specific agent (Research, Validation, Aggregation)
- **TaskRun**: Execution record of a task, tracks status, timing, errors, output
- **Finding**: Result unit returned from agents (title, source, content, confidence)

Execution flow: User → API → Workflow → Tasks (sequential) → Agent outputs → Aggregated response → User

## Key Conventions

- Agent classes inherit from base pattern: `execute(task: Task, workflow_run: WorkflowRun) -> output`
- Task status follows enum: PENDING → IN_PROGRESS → COMPLETED | FAILED
- Findings are immutable dataclasses with four fields: title, source, content, confidence
- No async operations in MVP (all synchronous execution)
- Each request creates exactly one workflow with three tasks (Research, Validation, Aggregation)

## Project Goals

1. Build a working research orchestration system to validate multi-agent coordination patterns
2. Use spec-driven development (OpenSpec) as the primary development tool
3. Iterate vertically: complete one agent's real implementation fully before moving to the next
4. Document the learning journey for technical articles on AI-driven development and spec-driven practices

## Assumptions

- Single concurrent workflow (no parallel request handling)
- Synchronous execution model (API blocks until all agents complete)
- Agents currently return dummy data (will be replaced iteratively)
- No persistence layer needed in MVP (state lives in memory during request)
- Task dependencies are strictly linear (Research → Validation → Aggregation)
