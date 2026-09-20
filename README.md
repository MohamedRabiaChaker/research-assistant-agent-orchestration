# Research Assistant Agent Orchestration

A multi-agent orchestration system for coordinating research workflows. Users submit a research topic and the orchestrator orchestrates multiple specialized agents (Research, Validation, Aggregation) to produce findings.

## Project Goal

Build a learning platform for understanding spec-driven development (OpenSpec) through iterative development. Development is driven by specifications documented in `openspec/`.

## Getting Started

### Prerequisites
- Python 3.14+
- `uv` (package manager)

### Installation
```bash
uv sync
```

### Running
```bash
fastapi dev main.py
```

The API will be available at `http://localhost:8000`.

## API

### POST /research

Request:
```json
{
  "topic": "climate change"
}
```

Response:
```json
{
  "findings": [
    {
      "title": "Finding Title",
      "source": "source name",
      "content": "Finding content",
      "confidence": 0.95
    }
  ]
}
```

## Development

Development is guided by specifications in `openspec/`. See `openspec/README.md` or the `openspec/` directory structure for current designs and proposals.

## Project Status

MVP: Research endpoint with dummy agents. Iterating on individual agent implementations.
