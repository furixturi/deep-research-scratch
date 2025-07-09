from fastapi import FastAPI, Request
from pydantic import BaseModel
from .agent import run_agent

app = FastAPI(title="Deep Research Tool Server")

class AgentRequest(BaseModel):
    prompt: str
    config: dict = {}

@app.post("/run_agent")
async def run_agent_endpoint(data: AgentRequest):
    """
    Endpoint to run the agent with the provided prompt and configuration.
    """
    try:
        response = await run_agent(prompt=data.prompt, config=data.config)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/health")
def health_check():
    """
    Health check endpoint to verify the server is running.
    """
    return {"status": "ok"}