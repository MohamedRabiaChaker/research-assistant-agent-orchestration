# Agent Instructions

## Code Style & Conventions

- Follow PEP 8 for Python code
- Use type hints for all function parameters and return types
- Import agent classes from `agents/` package (e.g., `from agents import ResearchAgent`)
- Task-specific parameters live in `task.parameters` dict (e.g., `task.parameters['topic']`)
- Prefer simple, explicit code over clever abstractions
- Keep agent implementations focused on a single responsibility

**Comments**: Do not add comments. Well-named variables and functions are self-documenting. Only add a comment when the WHY is non-obvious (hidden constraint, subtle invariant, workaround for a specific issue). If removing a comment wouldn't confuse a reader, don't write it. When a comment is necessary, keep it short: maximum 3 sentences. No multi-line comment blocks.

**Docstrings**: Keep them practical, not verbose. One-liner is usually enough. Example:
```python
def execute(self, task: Task, workflow_run: WorkflowRun) -> list[Finding]:
    """Execute research task and return findings."""
```

Not:
```python
def execute(self, task: Task, workflow_run: WorkflowRun) -> list[Finding]:
    """
    Execute a research task by querying external APIs and returning findings.
    
    Args:
        task: The task definition containing topic and parameters
        workflow_run: The workflow execution context for tracking
        
    Returns:
        A list of Finding objects with title, source, content, and confidence
    """
```

Avoid docstrings that just restate what the signature already says (parameter names, return type).

## Git Conventions

**Branch naming**: Use `[function]/slug` format where function is one of: `feature`, `bug`, `demo`, `refactor`

Examples:
- `feature/research-endpoint-mvp`
- `bug/fix-agent-timeout`
- `demo/async-workflow-prototype`
- `refactor/task-state-machine`

**Commit messages**: Keep them short and practical. Maximum 1 sentence. State the what, not the how.

Examples:
- ✅ `Add POST /research endpoint with dummy agents`
- ✅ `Fix agent timeout in validation step`
- ❌ `Update the execute method to add error handling for validation` (too verbose, states the how)
- ❌ `Make changes` (too vague)

One commit per logical unit. If your commit message needs an "and" or "also", split it into two commits.

## Workflow Execution Model

**Sequential execution**: Agents execute in strict order — Research → Validation → Aggregation. No branching, no parallelization in MVP.

**Invocation contract**:
```python
agent = AgentClass()
output = agent.execute(task: Task, workflow_run: WorkflowRun)
```

**Data threading**: Pass task context through the chain:
- Research agent receives topic from task.parameters
- Research output becomes Validation input
- Validation output becomes Aggregation input
- Final output is returned to user

**Timing**: Track start/finish times in TaskRun. Execution is synchronous—HTTP response waits for all agents to complete.

## Error Handling

For MVP: Keep simple. Agents should not throw exceptions; log errors and return empty/partial results.

- If an agent fails: Return empty list or lowest-confidence findings
- Do not retry—fail fast
- Log error to TaskRun.errors for debugging
- Mark task as FAILED in status enum

Escalation and recovery strategies deferred to future iterations.

## State Management

**Immutable task definition**: Task objects define what work to do (type, parameters, dependencies). Do not mutate task state.

**Mutable execution record**: TaskRun tracks actual execution (status, timing, output, errors). Update TaskRun as execution progresses.

**Workflow context**: WorkflowRun provides execution context (started_at, logs, knowledge, report). Access via `workflow_run` parameter in agent.execute().

**Finding accumulation**: Each agent transforms findings but does not discard them. Aggregation agent receives the full list from Validation.

## API Design Principles

**Single entry point**: POST /research is the only user-facing endpoint for research workflows.

**Request simplicity**: Accept minimal input (topic string). Future iterations can add parameters.

**Response consistency**: Always return `{"findings": [...]}` structure. Findings are guaranteed to have title, source, content, confidence.

**HTTP semantics**: Return 200 on success. Error responses (malformed request, server error) follow standard HTTP status codes.

**No hidden state**: Workflows exist for one request only. No workflow persistence or polling model in MVP.
