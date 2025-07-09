# Deep Research from Scratch (MVP)

A minimal, production-minded implementation of a tool-using research agent powered by LLMs.  
This assistant reasons step-by-step using tools like web search and code execution, and keeps a structured memory of its actions.

---

## 🎯 Goal

Build a deep research assistant within 24 hours, capable of answering complex questions by reasoning through tools and memory — like a simplified, open version of what Hugging Face or OpenAI agents might do internally.

---

## 🧱 Architecture Overview

We implement three essential components:

### 1. Agentic Reasoning Core

The thinking and coordination brain — modular and model-flexible, with support for single-agent or planner-based logic.

- **Model abstraction layer**: lets the user select models from OpenAI, Claude, etc.
- **Working memory**: stores a structured trace of thoughts, actions, and observations
- **Agentic system** (configurable):
  - **Option 1: Single-agent** with ReAct-style loop
  - **Option 2: Planner + role-based sub-agents** (e.g., searcher, coder)

### 2. Tool Use Layer

The system's eyes and hands — executes decisions made by the reasoning core.

- **Web search tool**: returns structured results with citation and snippet
- **Code execution tool**: runs secure Python code in subprocess
- *(TBA)* PDF parser, file tools, RAG backend, etc.

### 3. Memory, Trace, and Interface Layer

The long-term awareness and observability system.

- **Short-term memory**: maintained in memory, persisted async
- **Long-term memory**: stores knowledge summaries
- **Trace logger**: full history of thoughts, actions, outcomes
- **UI/API**: CLI, or HTTP API for Open WebUI integration

![diagram](media/component%20diagram.png)

---

## 🗂️ Project Structure

<pre lang="markdown">
deep-research-scratch/
├── media/                      # Architecture diagrams, screenshots
├── README.md
├── requirements.txt
└── src/
    ├── api/                    # Backend logic
    │   ├── agent_server.py     # FastAPI app with /run_agent
    │   ├── config.yaml         # Runtime defaults (model, agent type, etc.)
    │   ├── config_loader.py
    │   ├── agent/              # Custom agent logic
    │   │   ├── single_agent.py
    │   │   ├── memory.py
    │   │   ├── trace.py
    │   │   └── multi_agents/
    │   │       ├── planner_agent.py
    │   │       ├── search_agent.py
    │   │       ├── summarizer_agent.py
    │   │       └── writer_agent.py
    │   ├── models/             # Model routing layer
    │   │   └── model_router.py
    │   ├── tools/              # Tool interfaces (search, code, etc.)
    │   │   ├── search.py
    │   │   └── code_executor.py
    │   └── log/                # Logs and memory traces
    └── ui/
        └── open-webui/         # Optional: integration with Open WebUI
</pre>
