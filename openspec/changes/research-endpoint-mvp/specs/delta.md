# Research Endpoint MVP — Delta Spec

## Purpose

Enable users to trigger multi-agent research workflows through a single HTTP endpoint and receive findings.

## Requirements

### Endpoint Contract
- The system SHALL expose POST `/research` endpoint
- The endpoint MUST accept a JSON request with field `topic` (string)
- The endpoint MUST return a JSON response with field `findings` (array)
- The endpoint MUST return HTTP status 200 on success

### Workflow Execution
- The system SHALL execute ResearchAgent first, then ValidationAgent, then AggregationAgent
- The system SHALL execute agents synchronously (blocking call, return results before HTTP response)
- The system SHALL create one workflow per request
- The system SHALL create one task per agent within that workflow
- Each task MUST transition through states: PENDING → IN_PROGRESS → COMPLETED

### Data Flow
- The system SHALL pass the topic to each agent for execution context
- Each agent's output SHALL become the next agent's input
- The system MUST return the final AggregationAgent output to the user

### Finding Format
- Each finding MUST contain: `title`, `source`, `content`, `confidence`
- `confidence` MUST be a float between 0 and 1

### Concurrency
- The system MUST process only one workflow at a time (no concurrent requests)

## Scenarios

### Scenario: Successful Research Workflow
**GIVEN** a user submits a POST request to `/research` with `{"topic": "climate change"}`
**WHEN** the orchestrator processes the request
**THEN** the endpoint returns HTTP 200 with `{"findings": [...]}`
**AND** each finding in the response contains title, source, content, and confidence fields
