from fastapi import FastAPI, Request
from pydantic import BaseModel

from api.config_loader import load_default_config
from api.agent import run_agent

app = FastAPI(title="Deep Research Agent Server")
default_config = load_default_config()

class AgentRequest(BaseModel):
    prompt: str
    config: dict = {}

@app.post("/run_agent")
async def run_agent_endpoint(data: AgentRequest):
    """
    Endpoint to run the agent with the provided prompt and configuration.
    """
    merged_config = {**default_config, **data.config}

    try:
        response = await run_agent(prompt=data.prompt, config=merged_config)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/health")
def health_check():
    """
    Health check endpoint to verify the server is running.
    """
    return {"status": "ok"}