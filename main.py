from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ResearchRequest(BaseModel):
    prompt: str


@app.get("/health")
def health_endpoint():
    return {"message": "healthy", "status_code": 200}


@app.post("/research")
def trigger_research(request):
    try:
        return {"message": f"Research request triggered for prompt {request.prompt}"}
    except Exception:
        return {"message": "Error Processing request, please check payload"}
