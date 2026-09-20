from fastapi import FastAPI
from pydantic import BaseModel

from engine.orchestrator import Orchestrator

app = FastAPI()
orchestrator = Orchestrator()


class ResearchRequest(BaseModel):
    topic: str


@app.get("/health")
def health_endpoint():
    return {"message": "healthy", "status_code": 200}


@app.post("/research")
def trigger_research(request: ResearchRequest):
    findings = orchestrator.execute(request.topic)
    return {"findings": findings}
