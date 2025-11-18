# Project File Structure Explanation

## Main Entry Points

### **`smart_weather_api.py`** - **PRIMARY API** (Use This!)
- **Purpose**: Advanced FastAPI server with smart contextual responses
- **Features**: 
  - Multi-agent system with intelligent responses
  - Context-aware query understanding (clothing, activities, health, etc.)
  - Multi-city comparisons
  - Sport-specific advice
  - Travel and event planning
- **Usage**: `python smart_weather_api.py`
- **Endpoints**: `/query`, `/demo`, `/health`

### **`main.py`** - **CLI Interface** (For Testing)
- **Purpose**: Command-line interface for testing agents
- **Features**: Interactive mode, single queries
- **Usage**: `python main.py` or `python main.py "your query"`
- **Good for**: Quick testing without starting web server

## Agent System

### **Core Agents**
- **`agents/openrouter_smart_agent.py`** - Smart Coordinator (CURRENT)
- **`agents/agent_b.py`** - Executor Agent
- **`agents/agent_a.py`** - Original Coordinator (Legacy)

### **Utilities**
- **`utils/weather_api.py`** - Weather data fetching
- **`utils/openrouter_insight_engine.py`** - AI-powered insights
- **`utils/insight_engine.py`** - Basic insights (fallback)
- **`utils/message.py`** - Agent communication structures

## Documentation & Testing

### **Documentation**
- **`README.md`** - Main project documentation
- **`API_EXAMPLES.md`** - API usage examples
- **`QUICKSTART.md`** - Setup guide
- **`PROJECT_SUMMARY.md`** - Technical overview

### **Testing**
- **`test_agentic_system.py`** - Comprehensive API tests
- **`test_system.py`** - Basic system tests

## Recommended Usage

### **For Assignment Demonstration:**
```bash
# Start the smart API (recommended)
python smart_weather_api.py

# Test the system
python test_agentic_system.py
```

### **For Quick CLI Testing:**
```bash
# Interactive mode
python main.py

# Single query
python main.py "what should I wear in bangalore?"
```

### **For API Integration:**
```bash
# Use the smart API endpoints
curl -X POST "http://localhost:8000/query" \
     -d '{"query": "your question here"}'
```

## Evolution of Files

1. **`main.py`** - Original CLI interface - **Keep for testing**
2. **`api.py`** - Basic FastAPI - **Removed (redundant)**
3. **`smart_weather_api.py`** - Advanced API - **Primary interface**

## Which File to Use When

| Use Case | File | Why |
|----------|------|-----|
| **Assignment Demo** | `smart_weather_api.py` | Full multi-agent system with web API |
| **Quick Testing** | `main.py` | Fast CLI testing without web server |
| **API Integration** | `smart_weather_api.py` | RESTful endpoints for applications |
| **Development** | Both | CLI for quick tests, API for full features |

## Key Difference

- **`main.py`**: Simple CLI → Agent A → Agent B → Response
- **`smart_weather_api.py`**: Web API → Smart Agent → Agent B → Contextual Response

Both use the same underlying multi-agent system, just different interfaces!