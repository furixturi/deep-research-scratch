## Run the tool server from root
```bash
$ uvicorn src.api.main:app --reload
```

### Health Check
```bash
$ curl http://localhost:8000/health
```
This should return
```json
{"status":"ok"}
```

### Run agent
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



