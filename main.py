"""CLI Interface for the Multi-Agent AI System - Command Line Testing."""

import os
import sys
from dotenv import load_dotenv
from agents.agent_a import AgentA
from agents.agent_b import AgentB


def load_environment():
    """Load environment variables and validate."""
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    weather_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not openai_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your API keys (see .env.example)")
        sys.exit(1)
    
    if not weather_key:
        print("Error: OPENWEATHER_API_KEY not found in environment variables")
        print("Please create a .env file with your API keys (see .env.example)")
        sys.exit(1)
    
    return openai_key, weather_key


def print_banner():
    """Print welcome banner."""
    print("=" * 60)
    print("  Weather Insights System")
    print("  Intelligent weather analysis powered by AI")
    print("=" * 60)


def run_demo_queries(agent_a: AgentA):
    """Run demonstration queries showcasing weather insights."""
    demo_queries = [
        "Get the current weather in New York and give me insights and recommendations",
        "What's the weather like in London? Should I go outside today?",
        "Tell me about the weather in Tokyo and what I should wear",
        "What activities would you recommend based on the weather in Paris?"
    ]
    
    print("\n🎯 Running Demo Queries:\n")
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{'─' * 60}")
        print(f"Demo Query {i}: {query}")
        print('─' * 60)
        
        response = agent_a.process_request(query)
        
        print(f"\n📋 Response:")
        print(response)
        print()


def interactive_mode(agent_a: AgentA):
    """Run in interactive mode."""
    print("\n💬 Interactive Mode")
    print("Enter your requests (or 'quit' to exit):\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            response = agent_a.process_request(user_input)
            print(f"\n🤖 Assistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


def main():
    """Main function."""
    print_banner()
    
    # Load API keys
    print("\n🔧 Initializing system...")
    openai_key, weather_key = load_environment()
    
    # Check for OpenRouter key (preferred)
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    
    # Initialize agents
    if openrouter_key:
        agent_b = AgentB(weather_api_key=weather_key, openrouter_api_key=openrouter_key)
        agent_a = AgentA(openai_api_key="dummy", agent_b=agent_b)
        print("🧠 Using LLM for intelligent insights")
    else:
        # Fallback to rule-based insights
        agent_b = AgentB(weather_api_key=weather_key)
        agent_a = AgentA(openai_api_key=openai_key or "dummy", agent_b=agent_b)
        print("⚙️ Using rule-based insights (add OPENROUTER_API_KEY for AI insights)")
    
    print("\n✅ System ready!\n")
    
    # Check if query provided as command line argument
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"Processing query: {query}\n")
        response = agent_a.process_request(query)
        print(f"\n📋 Response:\n{response}\n")
    else:
        # Run demo queries first
        run_demo = input("Run demo queries? (y/n): ").strip().lower()
        if run_demo == 'y':
            run_demo_queries(agent_a)
        
        # Then enter interactive mode
        interactive_mode(agent_a)


if __name__ == "__main__":
    main()