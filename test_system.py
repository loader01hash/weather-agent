"""Simple test script to verify the system works."""

import os
from dotenv import load_dotenv
from agents.agent_a import AgentA
from agents.agent_b import AgentB


def test_system():
    """Test the multi-agent system with sample queries."""
    print("🧪 Testing Multi-Agent AI System\n")
    
    # Load environment
    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")
    weather_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not openai_key or not weather_key:
        print("❌ Error: API keys not found. Please set up .env file")
        return False
    
    # Initialize agents
    print("Initializing agents...")
    agent_b = AgentB(weather_api_key=weather_key)
    agent_a = AgentA(openai_api_key=openai_key, agent_b=agent_b)
    
    # Test queries
    test_queries = [
        "Get the current weather in Paris",
        "What's the temperature in Berlin and is it cloudy?",
        "Tell me about the weather in Sydney"
    ]
    
    print("\n" + "=" * 60)
    print("Running Test Queries")
    print("=" * 60 + "\n")
    
    passed = 0
    failed = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}/{len(test_queries)}: {query}")
        print("-" * 60)
        
        try:
            response = agent_a.process_request(query)
            
            if response and len(response) > 10:
                print(f"✅ PASSED")
                print(f"Response: {response[:100]}...")
                passed += 1
            else:
                print(f"❌ FAILED: Response too short or empty")
                failed += 1
                
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Test Summary: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = test_system()
    exit(0 if success else 1)