# Smart Weather Insights API

A FastAPI-based contextual weather insights system that provides intelligent, query-specific responses using AI-powered multi-agent architecture.

## Key Features

- **Contextual Understanding**: Understands what you're actually asking (clothing, activities, health, etc.)
- **Smart Response Length**: Short answers for simple queries, detailed insights for specific questions
- **Multi-Agent Architecture**: Coordinator and Executor agents working together
- **AI-Powered Analysis**: Uses OpenRouter's GPT models for intelligent recommendations
- **Real-time Weather Data**: Integrated with OpenWeatherMap API

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
Create a `.env` file with your API keys:
```env
OPENWEATHER_API_KEY=your_openweather_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

3. **Start the API server:**
```bash
python run_smart_api.py
```

4. **Test the API:**
```bash
python quick_test.py
```

## 📖 API Documentation

Once the server is running, visit:
- **Interactive docs:** http://localhost:8000/docs
- **API info:** http://localhost:8000/

## 🔗 Current API Endpoints

### `POST /contextual`
Get contextual weather insights based on your specific query.

**Simple Query (Short Response):**
```json
{
  "query": "What is the temperature in Bangalore?"
}
```

**Response:**
```json
{
  "query": "What is the temperature in Bangalore?",
  "response": "It's 24.6°C in Bangalore with haze.",
  "status": "success"
}
```

**Detailed Query (Contextual Response):**
```json
{
  "query": "What should I wear in New York today?"
}
```

**Response:**
```json
{
  "query": "What should I wear in New York today?",
  "response": "Hey! With the temperature around 15°C and partly cloudy skies, this is perfect sweater weather! I'd recommend a light sweater or cardigan with jeans. The 65% humidity means it might feel slightly warmer than the actual temperature, so avoid heavy layers...",
  "status": "success"
}
```

### `GET /examples`
Get example queries by category (clothing, activities, health, priority).

### `GET /test`
Test system with sample queries showing short vs detailed responses.

### `POST /batch`
Process multiple queries at once.

### `GET /health`
Health check endpoint.

## Query Types & Examples

### Simple Queries → Short Responses (25-40 characters)
- **"What is the temperature in Mumbai?"** → `"Mumbai is 30.99°C with smoke."`
- **"Weather in London?"** → `"London is 2.3°C with scattered clouds."`
- **"Temperature in Delhi?"** → `"Delhi is 25.1°C with haze."`

### Specific Queries → Detailed Contextual Responses (800+ characters)

#### 👕 Clothing Questions
- "What should I wear in Boston today?"
- "Do I need a jacket in Seattle?"
- "Should I dress warmly for Chicago weather?"

#### 🏃‍♂️ Activity Questions
- "Is it good weather for running in Central Park?"
- "Should I go hiking in Denver today?"
- "Can I have a picnic in San Francisco?"

#### 🌡️ Health & Safety Questions
- "Is it safe to drive in Miami weather?"
- "Should I be concerned about the heat in Phoenix?"
- "Is the humidity dangerous in Houston?"

#### Priority Questions
- "What's the most important thing about Seattle weather?"
- "What should be my main concern with Miami weather?"
- "What's the key thing to know about Tokyo weather?"

## 🤖 AI Model & Architecture

- **Model:** GPT-OSS-20B (Free tier)
- **Provider:** OpenRouter
- **Architecture:** Multi-agent system with smart contextual understanding
- **Response Intelligence:** Automatically detects query type and adjusts response length

## 🔑 Required API Keys

1. **OpenWeatherMap API:** https://openweathermap.org/api (Free tier available)
2. **OpenRouter API:** https://openrouter.ai/ (Free tier available)

## Testing

### Quick Test
```bash
python quick_test.py
```

### Manual Testing with curl

**Simple Query:**
```bash
curl -X POST "http://localhost:8000/contextual" \
     -H "Content-Type: application/json" \
     -d '{"query": "Temperature in Paris?"}'
```

**Detailed Query:**
```bash
curl -X POST "http://localhost:8000/contextual" \
     -H "Content-Type: application/json" \
     -d '{"query": "What should I wear in Paris today?"}'
```

**Batch Queries:**
```bash
curl -X POST "http://localhost:8000/batch" \
     -H "Content-Type: application/json" \
     -d '["Temperature in Mumbai?", "What should I wear in London?"]'
```

## Clean Project Structure

```
├── agents/
│   ├── agent_a.py                    # Original coordinator agent
│   ├── agent_b.py                    # Executor agent
│   └── openrouter_smart_agent.py     # Smart contextual coordinator
├── utils/
│   ├── insight_engine.py             # Basic insight generation
│   ├── openrouter_insight_engine.py  # AI-powered insights
│   ├── weather_api.py                # Weather data fetching
│   ├── message.py                    # Message structures
│   └── insight_formatter.py          # Response formatting
├── openrouter_smart_api.py           # Main Smart API (CURRENT)
├── api.py                           # Original API
├── simple_api.py                    # Simplified API version
├── main.py                          # Original CLI interface
├── test_system.py                   # System test script
├── run_smart_api.py                 # Simple run script
├── quick_test.py                    # Quick API test
└── requirements.txt                 # Updated dependencies
```

## Dependencies

- FastAPI - Web framework
- Uvicorn - ASGI server
- Requests - HTTP client
- Python-dotenv - Environment variables
- OpenAI - AI model integration (via OpenRouter)

## What Makes This Special

1. **Context Awareness**: Understands what you're actually asking
2. **Smart Length Control**: Short for simple, detailed for complex queries
3. **Natural Language**: Conversational, not robotic responses
4. **Actionable Advice**: Practical recommendations you can use
5. **Reliable Fallbacks**: Always provides useful information