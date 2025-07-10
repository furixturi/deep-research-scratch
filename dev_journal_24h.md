# MVP 24 Hours Journal

## Hour 1-4 Planning
Research and decide on project scope. See README.md

## Hour 5 Scaffolding
- 🧱 Project structured under src/api/ with clean separation
- ✅ .venv, .env, and requirements.txt configured
- ✅ FastAPI server scaffolded and running
- ✅ /run_agent endpoint implemented
- ✅ run_single_agent() and run_planner_agent() stub in place
- ✅ Async-compatible architecture established
- ✅ Config loading (via YAML) and merging implemented
- ❌ Removed external agent framework abstraction — going minimal and custom


### Run the agent server
Run from project root.
```bash
$ uvicorn src.api.main:app --reload
```

#### Health Check
```bash
$ curl http://localhost:8000/health
```
This should return
```json
{"status":"ok"}
```

#### Run agent
```bash
curl -X POST http://localhost:8000/run_agent \
> -H "Content-Type: application/json" \
> -d '{"prompt": "What is Deep Research?", "config": {"agent_type": "single_agen
t"}}'
```
For now, this should return
```json
{"response":"[Single Agent /stub] You said: What is Deep Research? with config: {'agent_type': 'single_agent'}"}
```

## Hour 6-8.5 Single Agent ReAct Loop, Tool Management Mechanism
- 🧠 Implemented a minimalistic, modular single-agent ReAct reasoning loop
- 🧾 Built a role-based Memory system compatible with chat-style models
- 🧰 Established a centralized tool registry with dynamic prompt integration
- 🧪 Verified end-to-end behavior using a stateless stub model and dummy tool
- 🗂️ Standardized all imports with api. prefix for package-ready structure

### Run the agent server
Changed the relative import to production-ready modular import. Still from the project root but now run the agent server with PYTHONPATH
```bash
$  PYTHONPATH=src uvicorn api.main:app --reload
```

### Test the single agent ReAct loop
```bash
$ curl -X POST http://localhost:8000/run_agent \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "How much revenue did NVIDIA make in 2024?",
    "config": {
      "agent_type": "single_agent"
    }
  }'
```
This should return
```bash
{"response":"[Stopped after 3 steps - no final answer]"}
```
While debug log printed on the server side
```bash
INFO:     127.0.0.1:59413 - "POST /run_agent HTTP/1.1" 200 OK
 --- Step 1 ---
 Thought: Thought: I am a stub thought. Still, I should use a tool to answer.
 Action: Action: search
 Action Input: Action Input: NVIDIA revenue 2024
> Calling tool 'search' with input: NVIDIA revenue 2024
< Tool 'search' returned: Simulated search result for query: NVIDIA revenue 2024

 --- Step 2 ---
 Thought: Thought: I am a stub thought. Still, I should use a tool to answer.
 Action: Action: search
 Action Input: Action Input: NVIDIA revenue 2024
> Calling tool 'search' with input: NVIDIA revenue 2024
< Tool 'search' returned: Simulated search result for query: NVIDIA revenue 2024

 --- Step 3 ---
 Thought: Thought: I am a stub thought. Still, I should use a tool to answer.
 Action: Action: search
 Action Input: Action Input: NVIDIA revenue 2024
> Calling tool 'search' with input: NVIDIA revenue 2024
< Tool 'search' returned: Simulated search result for query: NVIDIA revenue 2024
```