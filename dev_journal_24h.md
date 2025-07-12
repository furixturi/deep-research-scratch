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

## Hour 8.5-10.5 Model Config, Model Provider Integration, Model Router
- Redesigned model config and added AOAI and OAI model configuration
- Built AOAI and OAI model integration
- Built model router and test

## Hour 10.5-13 OpenAI Native Tool Call style
- Debug single agent ReAct end to end flow
- Refactor tools mechanism and registry
- Align tools with OpenAI native tools format
- Test and debug single agent ReAct flow with tool integration

### Test end-to-end ReAct flow with tool integration
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

Agent server debug logs
```bash
200 OK

============================================================
AGENT STARTING - AVAILABLE TOOLS:
  • search: Search the web for information
  • code: Execute Python code
============================================================

TOOL SCHEMAS:
[
  {
    "type": "function",
    "function": {
      "name": "search",
      "description": "Search the web for information",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query to look for"
          }
        },
        "required": [
          "query"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "code",
      "description": "Execute Python code",
      "parameters": {
        "type": "object",
        "properties": {
          "code": {
            "type": "string",
            "description": "The Python code to execute"
          }
        },
        "required": [
          "code"
        ]
      }
    }
  }
]

============================================================

USER QUESTION: How much revenue did NVIDIA make in 2024?
============================================================

=== STEP 1 ===

- Model Router DEBUG: Passing messages to AOAI model: {'role': 'user', 'content': 'How much revenue did NVIDIA make in 2024?'}

- Model Router DEBUG: Passing 2 tools to AOAI model
- Model Router DEBUG: Tools: ['search', 'code']

*** Raw response ***
 ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_zE8kaafT2EvYoT4OmwCWLpNB', function=Function(arguments='{"query":"NVIDIA revenue for 2024"}', name='search'), type='function')])

### Response has Tool Calls ###
Tool calls: 1
> Tool name: search
> Tool arg: {"query":"NVIDIA revenue for 2024"}
> Tool call ID: call_zE8kaafT2EvYoT4OmwCWLpNB
< Tool result: Simulated search result for query: NVIDIA revenue for 2024

=== STEP 2 ===

- Model Router DEBUG: Passing messages to AOAI model: {'role': 'tool', 'tool_call_id': 'call_zE8kaafT2EvYoT4OmwCWLpNB', 'content': 'Simulated search result for query: NVIDIA revenue for 2024'}

- Model Router DEBUG: Passing 2 tools to AOAI model
- Model Router DEBUG: Tools: ['search', 'code']

*** Raw response ***
 ChatCompletionMessage(content='Thought: The search query did not yield updated results for NVIDIA\'s 2024 revenue. As 2024 is ongoing, there may be quarterly revenue reports instead of the full year\'s data available. I will refine my search to look for recent quarterly earnings updates for NVIDIA in 2024.\n\nAction: Search\nAction Input: "NVIDIA Q1 Q2 revenue 2024 earnings results"', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_kuQ1gJ1sxhr4fIm00oU0W2Yp', function=Function(arguments='{"query":"NVIDIA Q1 Q2 revenue 2024 earnings results"}', name='search'), type='function')])

### Response has Tool Calls ###
Tool calls: 1

### Response also has TEXT ###
- Thought: The search query did not yield updated results for NVIDIA's 2024 revenue. As 2024 is ongoing, there may be quarterly revenue reports instead of the full year's data available. I will refine my search to look for recent quarterly earnings updates for NVIDIA in 2024.
- Action: Search
- Action Input: "NVIDIA Q1 Q2 revenue 2024 earnings results"
> Tool name: search
> Tool arg: {"query":"NVIDIA Q1 Q2 revenue 2024 earnings results"}
> Tool call ID: call_kuQ1gJ1sxhr4fIm00oU0W2Yp
< Tool result: Simulated search result for query: NVIDIA Q1 Q2 revenue 2024 earnings results

=== STEP 3 ===

- Model Router DEBUG: Passing messages to AOAI model: {'role': 'tool', 'tool_call_id': 'call_kuQ1gJ1sxhr4fIm00oU0W2Yp', 'content': 'Simulated search result for query: NVIDIA Q1 Q2 revenue 2024 earnings results'}

- Model Router DEBUG: Passing 2 tools to AOAI model
- Model Router DEBUG: Tools: ['search', 'code']

*** Raw response ***
 Thought: Based on the simulated search results, the exact revenue from NVIDIA for 2024 is not provided directly. Quarterly data might need to be aggregated when available. Alternatively, no official data for fiscal year 2024 may yet be complete.

Final Answer: NVIDIA's total revenue for 2024 is not finalized as the year is ongoing. You can check quarterly financial reports (e.g., Q1, Q2) released by NVIDIA to estimate their revenue for 2024. For accurate and updated information, visit NVIDIA's official investor relations website or view their SEC filings.

### Response is TEXT only ###
Thought: Based on the simulated search results, the exact revenue from NVIDIA for 2024 is not provided directly. Quarterly data might need to be aggregated when available. Alternatively, no official data for fiscal year 2024 may yet be complete.

Final Answer: NVIDIA's total revenue for 2024 is not finalized as the year is ongoing. You can check quarterly financial reports (e.g., Q1, Q2) released by NVIDIA to estimate their revenue for 2024. For accurate and updated information, visit NVIDIA's official investor relations website or view their SEC filings.
```

Response to curl command
```bash
{"response":"NVIDIA's total revenue for 2024 is not finalized as the year is ongoing. You can check quarterly financial reports (e.g., Q1, Q2) released by NVIDIA to estimate their revenue for 2024. For accurate and updated information, visit NVIDIA's official investor relations website or view their SEC filings."}
```