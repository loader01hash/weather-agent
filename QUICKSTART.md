# Smart Weather Insights - Quick Start Guide

Get the contextual weather insights system running in 5 minutes!

## What's New

This system now provides **contextual, query-specific responses**:
- **Simple queries** → Short, crisp answers
- **Specific queries** → Detailed, actionable insights

## Prerequisites

- Python 3.8 or higher
- OpenRouter API key ([Get one free here](https://openrouter.ai/))
- OpenWeatherMap API key ([Get one free here](https://openweathermap.org/api))

## Step 1: Setup Environment

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create environment file:**
   Create a `.env` file with your API keys:
   ```env
   OPENWEATHER_API_KEY=your-weather-api-key-here
   OPENROUTER_API_KEY=your-openrouter-api-key-here
   ```

## Step 2: Choose Your Interface

### Option A: Web API (Recommended)
```bash
python smart_weather_api.py     # Start web server
```
The API will be available at `http://localhost:8000`

**Test the API:**
```bash
python test_agentic_system.py   # Comprehensive tests
```

### Option B: Command Line (Quick Testing)
```bash
python main.py                  # Interactive mode
python main.py "your query"     # Single query
```

## Step 3: Try Different Query Types

### Simple Queries (Get Short Responses)
```bash
curl -X POST "http://localhost:8000/contextual" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the temperature in Bangalore?"}'
```
**Response:** `"It's 24.6°C in Bangalore with haze."`

### Specific Queries (Get Detailed Insights)
```bash
curl -X POST "http://localhost:8000/contextual" \
     -H "Content-Type: application/json" \
     -d '{"query": "What should I wear in New York today?"}'
```
**Response:** Detailed clothing recommendations with explanations

## Step 4: Explore Query Categories

### Clothing Questions
- "What should I wear in Boston today?"
- "Do I need a jacket in Seattle?"
- "Should I dress warmly for Chicago weather?"

### Activity Questions
- "Is it good weather for running in Chicago?"
- "Should I go hiking in Denver today?"
- "Can I have a picnic in San Francisco?"

### Health & Safety Questions
- "Should I be concerned about Phoenix heat?"
- "Is it safe to drive in Miami weather?"
- "Is the humidity dangerous in Houston?"

### Priority Questions
- "What's the most important thing about Seattle weather?"
- "What should be my main concern with Miami weather?"

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/contextual` | POST | Get contextual weather insights |
| `/examples` | GET | See example queries by category |
| `/test` | GET | Test system with sample queries |
| `/batch` | POST | Process multiple queries at once |

## Troubleshooting

### Common Issues

**❌ "Missing OPENROUTER_API_KEY"**
- Make sure `.env` file exists in project root
- Get free API key from [openrouter.ai](https://openrouter.ai/)

**❌ "Missing OPENWEATHER_API_KEY"**
- Get free API key from [openweathermap.org](https://openweathermap.org/api)
- Wait 10-15 minutes for activation after signup

**❌ "ModuleNotFoundError"**
- Run: `pip install -r requirements.txt`
- Make sure you're in the project directory

**❌ "City not found"**
- Try different city name spelling
- Use common city names or include country

### Getting API Keys

**OpenRouter API Key (Free):**
1. Go to [openrouter.ai](https://openrouter.ai/)
2. Sign up for free account
3. Go to Keys section
4. Create new API key
5. Copy the key (starts with `sk-or-`)

**OpenWeatherMap API Key (Free):**
1. Go to [openweathermap.org](https://openweathermap.org/api)
2. Sign up for free account
3. Go to API Keys section
4. Copy your default API key
5. Wait 10-15 minutes for activation

## Current Project Structure

```
smart-weather-insights/
├── run_smart_api.py              # Simple run script
├── openrouter_smart_api.py       # Main Smart API
├── quick_test.py                 # Quick test script
├── agents/
│   ├── agent_a.py               # Original coordinator
│   ├── agent_b.py               # Executor agent
│   └── openrouter_smart_agent.py # Smart contextual coordinator
├── utils/
│   ├── weather_api.py           # Weather data fetching
│   ├── insight_engine.py        # Basic insights
│   ├── openrouter_insight_engine.py # AI-powered insights
│   └── message.py               # Message structures
├── requirements.txt             # Dependencies
├── .env                        # Your API keys
└── API_README.md               # API documentation
```

## How It Works

1. **Query Analysis**: System detects if query is simple or specific
2. **Smart Routing**: 
   - Simple queries → Short, direct responses
   - Specific queries → Detailed, contextual insights
3. **AI Processing**: Uses OpenRouter's GPT models for intelligent analysis
4. **Weather Integration**: Real-time data from OpenWeatherMap
5. **Contextual Response**: Natural, actionable advice

## Example Responses

### Simple Query
**Input:** `"Temperature in Mumbai?"`  
**Output:** `"Mumbai is 30.99°C with smoke."`

### Detailed Query
**Input:** `"What should I wear in Mumbai today?"`  
**Output:** Detailed clothing recommendations considering temperature, humidity, air quality, and comfort factors.

## Next Steps

- Visit `http://localhost:8000/docs` for interactive API documentation
- Check `API_README.md` for complete API reference
- Try the `/examples` endpoint to see all query categories
- Use `/test` endpoint to see system capabilities

## Migration from Original System

The smart system is backward compatible:
```python
# Works with both original and smart agents
response = agent.process_request("What's the weather in NYC?")
```

Happy coding! 🚀🌤️