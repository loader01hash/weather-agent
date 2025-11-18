# Agentic AI Multi-Agent Weather System

A multi-agent AI system demonstrating agent communication, task delegation, and intelligent weather insights. Built for the **Agentic AI Mini-Project Assignment**.

## Assignment Overview

This system implements the required **two-agent architecture** where:

- **Agent A (Coordinator)**: Takes natural language requests, breaks them into tasks, delegates to Agent B
- **Agent B (Executor)**: Performs specific tasks (weather data fetching, insight generation) and returns results
- **Communication**: Agents communicate via structured programmatic calls
- **AI Integration**: Uses OpenRouter GPT for natural language processing

## Assignment Requirements Met

- **Two Agent System**: Agent A (Coordinator) + Agent B (Executor)  
- **Agent Communication**: Programmatic function calls with structured messages  
- **Task Delegation**: Agent A breaks requests into smaller tasks for Agent B  
- **Natural Language Processing**: OpenRouter GPT for request understanding  
- **End-to-End Workflow**: Complete user request → agent processing → final response  
- **Modular Code**: Clean separation of agent roles and responsibilities  
- **Easy to Run**: Single command startup with clear instructions  

## Bonus Features Implemented

- **Multiple Task Support**: Handles various weather-related tasks  
- **Error Handling**: Graceful degradation with fallback responses  
- **Async Compatibility**: FastAPI with async endpoints  
- **Enhanced Communication**: Type-safe message structures  

## Prerequisites

- Python 3.8 or higher
- OpenRouter API key (free at [openrouter.ai](https://openrouter.ai/))
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create `.env` file:**
```env
OPENWEATHER_API_KEY=your_weather_key
OPENROUTER_API_KEY=your_openrouter_key
```

3. **Start the multi-agent system:**
```bash
python smart_weather_api.py
```

4. **Test the system:**
```bash
python test_agentic_system.py
```

## Assignment Example Workflow

### Example: "Get the current weather in New York and give me a short summary"

**Agent A (Coordinator) Process:**
1. Receives natural language request
2. Analyzes intent using AI (OpenRouter GPT)
3. Breaks into tasks: `[GET_WEATHER, GENERATE_SUMMARY]`
4. Delegates tasks to Agent B via structured messages
5. Compiles final response from Agent B results

**Agent B (Executor) Process:**
1. Receives `GET_WEATHER` task from Agent A
2. Fetches weather data from OpenWeatherMap API
3. Receives `GENERATE_SUMMARY` task from Agent A  
4. Generates intelligent summary using AI insights
5. Returns structured results to Agent A

**Communication Flow:**
```
User Request → Agent A → Task Objects → Agent B → TaskResult Objects → Agent A → Final Response
```

### Additional Examples

**Input:** `"What should I wear in London today?"`  
**Agent Workflow:** Agent A identifies clothing intent → Agent B fetches weather + generates clothing insights → Agent A compiles personalized recommendations

**Input:** `"Is it good weather for running in Chicago?"`  
**Agent Workflow:** Agent A identifies activity intent → Agent B analyzes weather for running conditions → Agent A provides activity-specific advice

## Multi-Agent Architecture

### Agent A - Coordinator (OpenRouterSmartAgent)
**Role**: Request analysis, task decomposition, and workflow coordination
- **Natural Language Understanding**: Analyzes user requests using OpenRouter GPT
- **Task Decomposition**: Breaks complex requests into smaller, actionable tasks
- **Agent Communication**: Sends structured Task objects to Agent B
- **Response Compilation**: Combines Agent B results into final user response
- **Error Handling**: Manages failures and provides fallback responses

### Agent B - Executor (AgentB)
**Role**: Task execution and data processing
- **Weather Data Retrieval**: Fetches real-time data from OpenWeatherMap API
- **Insight Generation**: Creates intelligent weather insights using AI
- **Task Processing**: Handles multiple task types (weather, insights, analysis)
- **Structured Results**: Returns TaskResult objects to Agent A
- **Multi-Engine Support**: Basic + AI-powered processing capabilities

### Communication Protocol
```
Agent A ←→ Agent B Communication Flow:

1. Agent A creates Task object with parameters
2. Agent A calls Agent B.execute_task(task)
3. Agent B processes task and external APIs
4. Agent B returns TaskResult object
5. Agent A compiles results into final response
```

**Message Structures:**
- `Task`: Contains task_type, parameters, description
- `TaskResult`: Contains success status, data, error information
- `TaskType`: Enum defining available task types (GET_WEATHER, GENERATE_INSIGHTS, etc.)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/query` | POST | Submit natural language query to multi-agent system |
| `/demo` | GET | View agent workflow demonstration |
| `/health` | GET | Check system health and agent status |

## 🎯 Query Categories & Examples

### 👕 Clothing Questions (Detailed Responses)
- **"What should I wear in Boston today?"** → Specific clothing recommendations with layering advice
- **"Do I need a jacket in Seattle?"** → Direct answer with reasoning and alternatives
- **"Should I dress warmly for Chicago weather?"** → Temperature-appropriate clothing guidance

### 🏃‍♂️ Activity Questions (Detailed Responses)
- **"Is it good weather for running in Chicago?"** → Running-specific conditions and timing
- **"Should I go hiking in Denver today?"** → Hiking safety and equipment recommendations
- **"Can I have a picnic in San Francisco?"** → Outdoor activity suitability assessment

### 🌡️ Health & Safety Questions (Detailed Responses)
- **"Should I be concerned about Phoenix heat?"** → Health risks and safety measures
- **"Is it safe to drive in Miami weather?"** → Driving conditions and precautions
- **"Is the humidity dangerous in Houston?"** → Health implications and recommendations

### 🎯 Priority Questions (Detailed Responses)
- **"What's the most important thing about Seattle weather?"** → Key priority information
- **"What should be my main concern with Miami weather?"** → Primary considerations
- **"What's the key thing to know about Tokyo weather?"** → Essential information

### 🌤️ Simple Questions (Short Responses)
- **"What is the temperature in Mumbai?"** → `"Mumbai is 30.99°C with smoke."`
- **"Weather in London?"** → `"London is 2.3°C with scattered clouds."`
- **"Temperature in Delhi?"** → `"Delhi is 25.1°C with haze."`

## 🧪 Testing Examples

### API Testing
```bash
# Simple query
curl -X POST "http://localhost:8000/contextual" \
     -H "Content-Type: application/json" \
     -d '{"query": "Temperature in Paris?"}'

# Detailed query
curl -X POST "http://localhost:8000/contextual" \
     -H "Content-Type: application/json" \
     -d '{"query": "What should I wear in Paris today?"}'

# Batch queries
curl -X POST "http://localhost:8000/batch" \
     -H "Content-Type: application/json" \
     -d '["Temperature in Mumbai?", "What should I wear in London?"]'
```

## Simplified Project Structure

```
agentic-ai-weather-system/
├── smart_weather_api.py              # 🚀 MAIN API - Multi-agent system (START HERE)
├── main.py                          # 🖥️ CLI interface for testing
├── test_agentic_system.py            # 🧪 Assignment compliance tests
├── agents/
│   ├── openrouter_smart_agent.py    # 🧠 Smart coordinator (CURRENT)
│   ├── agent_b.py                   # ⚡ Executor agent
│   └── agent_a.py                   # 📋 Original coordinator (legacy)
├── utils/
│   ├── weather_api.py               # Weather API integration
│   ├── openrouter_insight_engine.py # AI-powered insights
│   ├── insight_engine.py            # Basic insights (fallback)
│   ├── message.py                   # Agent communication
│   └── insight_formatter.py         # Response formatting
├── simple_api.py                    # Simplified API version
├── test_system.py                   # Basic system tests
├── requirements.txt                 # Python dependencies
├── .env                            # API keys configuration
├── FILE_STRUCTURE.md               # 📖 File explanation guide
├── README.md                       # This file
├── QUICKSTART.md                   # Setup guide
└── PROJECT_SUMMARY.md              # Technical overview
```

## 🎯 **Two Simple Ways to Use:**

### **1. Web API (Recommended for Assignment)**
```bash
python smart_weather_api.py    # Start web server
python test_agentic_system.py  # Test the system
```

### **2. Command Line (Quick Testing)**
```bash
python main.py                 # Interactive mode
python main.py "your query"    # Single query
```

## Technology Stack

- **FastAPI**: Modern web framework with automatic documentation
- **OpenRouter**: AI model access (GPT-OSS-20B free tier)
- **OpenWeatherMap**: Real-time weather data (free tier)
- **Python 3.8+**: Core language with type hints
- **Uvicorn**: ASGI server for FastAPI
- **Requests**: HTTP client for API calls

## 🎯 Key Design Decisions

1. **Smart Response Length**: Automatically matches response detail to query complexity
2. **Context-Aware Intelligence**: Understands user intent beyond keywords
3. **Reliable AI Integration**: OpenRouter with robust fallback systems
4. **FastAPI Architecture**: Modern web API with automatic documentation
5. **Multi-Agent Coordination**: Enhanced agents with specialized capabilities
6. **Natural Language Focus**: Conversational responses, not data dumps

## How to Run

1. **Start the multi-agent system:**
```bash
python smart_weather_api.py
```

2. **Test assignment compliance:**
```bash
python test_agentic_system.py
```

3. **View system documentation:**
- **API Docs**: `http://localhost:8000/docs`
- **Agent Demo**: `http://localhost:8000/demo`
- **System Health**: `http://localhost:8000/health`

## Sample Inputs and Outputs

### Assignment Example
**Input:** `"Get the current weather in New York and give me a short summary"`

**Agent A Process:**
- Analyzes request using OpenRouter GPT
- Breaks into tasks: `[GET_WEATHER, GENERATE_SUMMARY]`
- Delegates to Agent B

**Agent B Process:**
- Fetches weather data from OpenWeatherMap API
- Generates intelligent summary
- Returns structured results

**Output:** `"New York is currently 22°C with partly cloudy skies. It's a pleasant day with comfortable temperatures - perfect for outdoor activities. Light clothing recommended with a possible light jacket for evening."`

### Additional Examples
- **Input:** `"What should I wear in London today?"`
- **Input:** `"Is it good weather for running in Chicago?"`
- **Input:** `"Should I be concerned about Phoenix heat?"`

## Design and Agent Roles

### Agent A (Coordinator) - OpenRouterSmartAgent
**Responsibilities:**
- Natural language request analysis
- Intelligent task decomposition
- Agent-to-agent communication coordination
- Final response compilation and formatting

**AI Integration:** Uses OpenRouter GPT for understanding user intent and generating natural responses

### Agent B (Executor) - AgentB  
**Responsibilities:**
- Weather data retrieval from external APIs
- Task execution (weather fetching, insight generation)
- Structured data processing and formatting
- Error handling for external service failures

**Integrations:** OpenWeatherMap API, AI-powered insight engines

### Communication Method
**Programmatic Function Calls** with structured message objects:
- `Task` objects: Contain task type, parameters, and descriptions
- `TaskResult` objects: Return success status, data, and error information
- Type-safe enums for task types and message types

## Assignment Evaluation Criteria Met

✅ **Clear Agent Separation**: Distinct roles with Agent A coordinating and Agent B executing  
✅ **End-to-End Demo**: Complete workflow from user input to final response  
✅ **AI Integration**: OpenRouter GPT for natural language processing  
✅ **Clean Code**: Modular design with clear interfaces and documentation  
✅ **Easy to Run**: Single command startup with environment validation  
✅ **Thoughtful Design**: Multi-agent architecture with intelligent communication  

This system demonstrates practical agentic AI principles with real-world applicability, showcasing how multiple AI agents can collaborate to solve complex tasks through structured communication and task delegation. 🤖