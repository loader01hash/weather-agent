# Multi-Agent System API Examples

## Quick Start

Start the system:
```bash
python smart_weather_api.py
```

## API Endpoints

### 1. Submit Query to Multi-Agent System

**Endpoint:** `POST /query`

Submit natural language queries to the multi-agent system for processing.

```bash
# Assignment example query
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "Get the current weather in New York and give me a short summary"}'

# Clothing advice query
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What should I wear in London today?"}'

# Activity planning query
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "Is it good weather for running in Chicago?"}'
```

**Response Format:**
```json
{
  "query": "Get the current weather in New York and give me a short summary",
  "response": "New York is currently 22°C with partly cloudy skies...",
  "agent_workflow": {
    "step_1": "Agent A analyzed natural language request",
    "step_2": "Agent A decomposed request into tasks",
    "step_3": "Agent A delegated tasks to Agent B",
    "step_4": "Agent B executed weather data fetching",
    "step_5": "Agent B generated contextual insights",
    "step_6": "Agent A compiled final response"
  },
  "status": "success"
}
```

### 2. View Agent Workflow Demo

**Endpoint:** `GET /demo`

See how the multi-agent system works and communicates.

```bash
curl -X GET "http://localhost:8000/demo"
```

**Response:** Shows agent roles, communication protocol, and example workflows.

### 3. Check System Health

**Endpoint:** `GET /health`

Verify that both agents and external services are ready.

```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "system_status": "operational",
  "multi_agent_system": {
    "agent_a_coordinator": "initialized and ready",
    "agent_b_executor": "initialized and ready",
    "communication": "active"
  },
  "external_services": {
    "openweather_api": "configured",
    "openrouter_ai": "configured"
  }
}
```

## 🧪 Testing Examples

### Python Requests
```python
import requests

# Submit query to multi-agent system
response = requests.post(
    "http://localhost:8000/query",
    json={"query": "What's the weather in Paris and what should I wear?"}
)

result = response.json()
print(f"Agent Response: {result['response']}")
print(f"Workflow: {result['agent_workflow']}")
```

### JavaScript Fetch
```javascript
// Submit query to multi-agent system
fetch('http://localhost:8000/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: "Is it good weather for outdoor activities in Miami?"
  })
})
.then(response => response.json())
.then(data => {
  console.log('Agent Response:', data.response);
  console.log('Workflow:', data.agent_workflow);
});
```

## Assignment Demonstration

The system perfectly demonstrates the assignment requirements:

1. **Two Agents**: Agent A (Coordinator) and Agent B (Executor)
2. **Communication**: Structured Task/TaskResult objects
3. **Task Delegation**: Agent A breaks queries into tasks for Agent B
4. **Natural Language**: AI-powered query understanding
5. **End-to-End**: Complete workflow from query to response

### Example Workflow
```
User: "Get weather in NYC and summarize"
  ↓
Agent A: Analyzes query → Creates tasks [GET_WEATHER, SUMMARIZE]
  ↓
Agent B: Fetches weather data → Generates summary
  ↓
Agent A: Compiles results → Returns natural response
```

## Interactive Documentation

Visit `http://localhost:8000/docs` for full interactive API documentation with:
- Request/response schemas
- Try-it-out functionality
- Detailed endpoint descriptions
- Example requests and responses