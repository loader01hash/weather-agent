"""Simple FastAPI endpoint for weather insights using GPT-OSS-20B."""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from agents.agent_b import AgentB
from utils.message import Task, TaskType

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Weather Insights API",
    description="Get intelligent weather insights powered by GPT-OSS-20B",
    version="1.0.0"
)

# Initialize agent
openrouter_key = os.getenv("OPENROUTER_API_KEY")
weather_key = os.getenv("OPENWEATHER_API_KEY")

if not openrouter_key or not weather_key:
    raise Exception("Missing required API keys. Please set OPENROUTER_API_KEY and OPENWEATHER_API_KEY in .env file")

agent_b = AgentB(weather_api_key=weather_key, openrouter_api_key=openrouter_key)


class WeatherRequest(BaseModel):
    city: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "city": "New York"
            }
        }


class WeatherResponse(BaseModel):
    city: str
    weather_data: dict
    insights: dict
    status: str = "success"


def extract_city_from_query(query: str) -> str:
    """Simple city extraction from query."""
    # Common city names to look for
    cities = [
        "new york", "london", "paris", "tokyo", "miami", "chicago", 
        "seattle", "phoenix", "berlin", "sydney", "toronto", "boston",
        "los angeles", "san francisco", "denver", "atlanta", "houston"
    ]
    
    query_lower = query.lower()
    for city in cities:
        if city in query_lower:
            return city.title()
    
    # Look for "in [city]" pattern
    words = query.split()
    for i, word in enumerate(words):
        if word.lower() == "in" and i + 1 < len(words):
            return words[i + 1].replace(",", "").replace(".", "").replace("?", "")
    
    return "New York"  # Default


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Weather Insights API powered by GPT-OSS-20B",
        "model": "openai/gpt-oss-20b:free",
        "endpoints": {
            "/weather/{city}": "GET - Get weather insights for a city",
            "/weather": "POST - Get weather insights with query",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "model": "openai/gpt-oss-20b:free"}


@app.get("/weather/{city}")
async def get_weather_by_city(city: str):
    """Get weather insights for a specific city."""
    try:
        # Get weather data
        weather_task = Task(
            task_type=TaskType.GET_WEATHER,
            parameters={"city": city, "units": "metric"},
            description=f"Get weather for {city}"
        )
        
        weather_result = agent_b.execute_task(weather_task)
        
        if not weather_result.success:
            raise HTTPException(status_code=404, detail=f"Could not get weather for {city}")
        
        # Generate insights
        insights_task = Task(
            task_type=TaskType.GENERATE_WEATHER_INSIGHTS,
            parameters={"weather_data": weather_result.data},
            description="Generate comprehensive weather insights"
        )
        
        insights_result = agent_b.execute_task(insights_task)
        
        return WeatherResponse(
            city=city,
            weather_data=weather_result.data,
            insights=insights_result.data if insights_result.success else {},
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing weather request: {str(e)}"
        )


@app.post("/weather")
async def get_weather_insights(request: WeatherRequest):
    """Get weather insights for a city."""
    return await get_weather_by_city(request.city)


@app.post("/weather/query")
async def get_weather_from_query(request: dict):
    """
    Get weather insights from a natural language query.
    
    Example: {"query": "What's the weather like in Paris?"}
    """
    try:
        query = request.get("query", "")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        # Extract city from query
        city = extract_city_from_query(query)
        
        # Get weather insights
        return await get_weather_by_city(city)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@app.get("/examples")
async def get_examples():
    """Get example requests."""
    return {
        "city_examples": [
            "New York", "London", "Paris", "Tokyo", "Miami", "Chicago"
        ],
        "query_examples": [
            "What's the weather like in New York?",
            "How's the weather in London today?",
            "Tell me about Paris weather",
            "Weather in Tokyo please"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)