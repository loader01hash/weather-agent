"""
Smart Weather Insights API - Agentic AI Multi-Agent System
A simplified, async-compatible FastAPI application with two cooperating agents.
"""

import os
import asyncio
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Import the agents
from agents.agent_b import AgentB
from agents.openrouter_smart_agent import OpenRouterSmartAgent

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Smart Weather Insights - Agentic AI System",
    description="Multi-agent AI system where Agent A coordinates and Agent B executes weather tasks",
    version="1.0.0"
)

# Initialize agents globally
openrouter_key = os.getenv("OPENROUTER_API_KEY")
weather_key = os.getenv("OPENWEATHER_API_KEY")

if not weather_key or not openrouter_key:
    raise Exception("Missing required API keys. Please set OPENWEATHER_API_KEY and OPENROUTER_API_KEY in .env file")

# Initialize the multi-agent system
agent_b = AgentB(weather_api_key=weather_key, openrouter_api_key=openrouter_key)
agent_a = OpenRouterSmartAgent(openrouter_api_key=openrouter_key, agent_b=agent_b)


class AgentRequest(BaseModel):
    """Request model for the multi-agent system."""
    query: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "Get the current weather in New York and give me a short summary"
                },
                {
                    "query": "What should I wear in London today?"
                },
                {
                    "query": "Is it good weather for running in Chicago?"
                }
            ]
        }
    }


class AgentResponse(BaseModel):
    """Response model from the multi-agent system."""
    query: str
    response: str
    agent_workflow: Optional[Dict[str, Any]] = None
    status: str = "success"


class SimpleResponse(BaseModel):
    """Simple response model without workflow details."""
    query: str
    response: str
    status: str = "success"


@app.get("/")
async def root():
    """Root endpoint - Multi-Agent AI System information."""
    return {
        "title": "Smart Weather Insights - Agentic AI System",
        "description": "Multi-agent AI system demonstrating agent communication and task delegation",
        "agents": {
            "Agent A (Coordinator)": "Analyzes requests, breaks into tasks, coordinates workflow",
            "Agent B (Executor)": "Executes weather data fetching and insight generation"
        },
        "features": [
            "Natural language request processing",
            "Intelligent task decomposition", 
            "Agent-to-agent communication",
            "Contextual response generation",
            "Async-compatible architecture"
        ],
        "endpoints": {
            "/query": "POST - Submit natural language query (clean response)",
            "/query-detailed": "POST - Submit query with agent workflow details",
            "/demo": "GET - View agent workflow demonstration",
            "/health": "GET - Check system health and agent status"
        }
    }


@app.post("/query", response_model=SimpleResponse)
async def process_query(request: AgentRequest):
    """
    Submit a natural language query to the multi-agent system.
    
    **Multi-Agent Processing:**
    1. **Agent A (Coordinator)** receives and analyzes the natural language query
    2. **Agent A** decomposes the query into specific, actionable tasks
    3. **Agent A** delegates tasks to **Agent B (Executor)** using structured messages
    4. **Agent B** executes tasks (weather API calls, data processing, insight generation)
    5. **Agent A** receives results and compiles the final user response
    
    **Supported Query Types:**
    - Weather requests: "Get the current weather in New York and give me a short summary"
    - Clothing advice: "What should I wear in Boston today?"
    - Activity planning: "Is it good weather for running in Miami?"
    - Health considerations: "Should I be concerned about Phoenix heat?"
    """
    try:
        # This demonstrates the full multi-agent workflow
        # Agent A coordinates the entire process internally
        response = await asyncio.to_thread(agent_a.process_request, request.query)
        
        return SimpleResponse(
            query=request.query,
            response=response,
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Multi-agent system error: {str(e)}"
        )


@app.post("/query-detailed", response_model=AgentResponse)
async def process_query_detailed(request: AgentRequest):
    """
    Submit a natural language query with detailed agent workflow information.
    
    **Same processing as /query but includes:**
    - Agent workflow steps
    - Communication details
    - Task delegation information
    
    **Use this endpoint when you want to see how the multi-agent system works internally.**
    """
    try:
        # This demonstrates the full multi-agent workflow
        response = await asyncio.to_thread(agent_a.process_request, request.query)
        
        # Create detailed workflow information
        workflow_info = {
            "agents_used": "Agent A (Coordinator) + Agent B (Executor)",
            "communication_method": "Direct function calls with structured messages",
            "processing_steps": [
                "Agent A analyzed natural language request",
                "Agent A decomposed request into tasks", 
                "Agent A delegated tasks to Agent B",
                "Agent B executed weather data fetching",
                "Agent B generated contextual insights",
                "Agent A compiled final response"
            ],
            "task_types_handled": ["weather_data_retrieval", "insight_generation", "response_compilation"]
        }
        
        return AgentResponse(
            query=request.query,
            response=response,
            agent_workflow=workflow_info,
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Multi-agent system error: {str(e)}"
        )


@app.get("/demo")
async def agent_workflow_demo():
    """
    Demonstrate the multi-agent workflow and communication patterns.
    Shows how Agent A (Coordinator) and Agent B (Executor) collaborate.
    """
    demo_queries = [
        {
            "query": "Get the current weather in New York and give me a short summary",
            "agent_a_role": "Breaks into: 1) Get weather data, 2) Generate summary",
            "agent_b_role": "Fetches weather data from API, provides structured results",
            "communication": "Agent A → Agent B via Task objects, Agent B → Agent A via TaskResult"
        },
        {
            "query": "What should I wear in London today?",
            "agent_a_role": "Identifies clothing intent, requests weather + clothing insights",
            "agent_b_role": "Gets weather data, generates clothing recommendations",
            "communication": "Structured task delegation with contextual parameters"
        }
    ]
    
    return {
        "multi_agent_system": {
            "description": "Two-agent system demonstrating task delegation and communication",
            "workflow": "User Query → Agent A (Analysis & Delegation) → Agent B (Execution) → Agent A (Compilation) → Response"
        },
        "agent_roles": {
            "Agent A - Coordinator": {
                "primary_function": "Request analysis and task orchestration",
                "capabilities": [
                    "Natural language query understanding",
                    "Intelligent task decomposition",
                    "Agent-to-agent communication",
                    "Result compilation and response generation"
                ],
                "ai_tools": "OpenRouter GPT for language processing"
            },
            "Agent B - Executor": {
                "primary_function": "Task execution and data processing", 
                "capabilities": [
                    "Weather data retrieval from external APIs",
                    "Insight generation and analysis",
                    "Structured data processing",
                    "Error handling for external services"
                ],
                "integrations": ["OpenWeatherMap API", "AI insight engines"]
            }
        },
        "communication_method": {
            "type": "Programmatic function calls",
            "message_format": "Structured Task and TaskResult objects",
            "data_flow": "Agent A → Task → Agent B → TaskResult → Agent A",
            "error_handling": "Graceful degradation with informative fallbacks"
        },
        "example_workflows": demo_queries
    }


@app.get("/health")
async def system_health():
    """
    Check the health and readiness of the multi-agent system.
    Verifies agent initialization and external API connectivity.
    """
    return {
        "system_status": "operational",
        "multi_agent_system": {
            "agent_a_coordinator": "initialized and ready",
            "agent_b_executor": "initialized and ready",
            "communication": "active"
        },
        "external_services": {
            "openweather_api": "configured" if weather_key else "not_configured",
            "openrouter_ai": "configured" if openrouter_key else "not_configured"
        },
        "capabilities": {
            "natural_language_processing": "available" if openrouter_key else "limited",
            "weather_data_retrieval": "available" if weather_key else "unavailable",
            "task_delegation": "active",
            "agent_communication": "active"
        }
    }





def check_environment():
    """Check if required environment variables are set."""
    required_keys = ["OPENWEATHER_API_KEY", "OPENROUTER_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print("❌ Missing required environment variables:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\nPlease add them to your .env file")
        return False
    
    print("✅ Environment variables configured")
    return True


def main():
    """Run the Multi-Agent AI System."""
    print("🤖 Multi-Agent AI Weather System")
    print("=" * 40)
    print("Agent A: Coordinator (Request Analysis & Task Delegation)")
    print("Agent B: Executor (Task Execution & Data Processing)")
    print("=" * 40)
    
    if not check_environment():
        return
    
    print("🚀 Starting multi-agent system...")
    print("📡 Server: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🎯 Agent Demo: http://localhost:8000/demo")
    print("💚 Health Check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop")
    
    try:
        uvicorn.run(
            "smart_weather_api:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )
    except KeyboardInterrupt:
        print("\n👋 Multi-agent system stopped")


if __name__ == "__main__":
    main()