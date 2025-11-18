"""Agent A - Coordinator Agent that breaks down requests and delegates tasks."""

import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from utils.message import Task, TaskType, TaskResult
from agents.agent_b import AgentB
from utils.insight_formatter import InsightFormatter


class AgentA:
    """
    Coordinator Agent that understands user requests,
    breaks them into tasks, and delegates to Agent B.
    """
    
    def __init__(self, openai_api_key: str, agent_b: AgentB):
        """Initialize Agent A with OpenAI API and reference to Agent B."""
        self.name = "Agent A (Coordinator)"
        self.client = OpenAI(api_key=openai_api_key)
        self.agent_b = agent_b
        self.insight_formatter = InsightFormatter()
        print(f"[{self.name}] Initialized and ready to coordinate tasks")
    
    def process_request(self, user_request: str) -> str:
        """
        Process a user request end-to-end.
        
        Args:
            user_request: Natural language request from user
            
        Returns:
            Final response string
        """
        print(f"\n[{self.name}] Received request: '{user_request}'")
        
        # Step 1: Understand and break down the request
        tasks = self._decompose_request(user_request)
        
        if not tasks:
            return "I couldn't understand your request. Please try rephrasing it."
        
        print(f"[{self.name}] Identified {len(tasks)} task(s) to execute")
        
        # Step 2: Execute tasks via Agent B with intelligent sequencing
        results = []
        weather_data = None
        
        for i, task in enumerate(tasks, 1):
            print(f"[{self.name}] Delegating task {i}/{len(tasks)} to Agent B")
            
            # If this is an insight task, use weather data from previous GET_WEATHER task
            if (task.task_type in [TaskType.GENERATE_WEATHER_INSIGHTS, TaskType.ANALYZE_COMFORT_CONDITIONS, 
                                 TaskType.SUGGEST_ACTIVITIES, TaskType.ASSESS_HEALTH_FACTORS] and 
                weather_data is not None):
                # Replace placeholder with actual weather data
                task.parameters["weather_data"] = weather_data
            
            result = self.agent_b.execute_task(task)
            results.append(result)
            
            # Store weather data for subsequent insight tasks
            if task.task_type == TaskType.GET_WEATHER and result.success:
                weather_data = result.data
        
        # Step 3: Compile and format final response
        final_response = self._compile_response(user_request, tasks, results)
        
        print(f"[{self.name}] Request completed\n")
        return final_response
    
    def _decompose_request(self, user_request: str) -> List[Task]:
        """
        Use AI to understand request and break it into tasks.
        
        Args:
            user_request: User's natural language request
            
        Returns:
            List of Task objects
        """
        system_prompt = """You are a task decomposition assistant. Analyze user requests and break them into specific tasks.

Available task types:
1. GET_WEATHER - Get weather data for a city
   Parameters: {"city": "city_name", "units": "metric" or "imperial"}

2. CALCULATE - Perform calculations
   Parameters: {"operation": "sum/average/max/min", "values": [numbers]}

3. GENERATE_WEATHER_INSIGHTS - Generate comprehensive weather insights
   Parameters: {"weather_data": weather_data_object}

4. ANALYZE_COMFORT_CONDITIONS - Analyze comfort based on weather
   Parameters: {"weather_data": weather_data_object}

5. SUGGEST_ACTIVITIES - Suggest activities based on weather
   Parameters: {"weather_data": weather_data_object}

6. ASSESS_HEALTH_FACTORS - Assess health considerations
   Parameters: {"weather_data": weather_data_object}

For weather-related requests, ALWAYS include GET_WEATHER first, then add insight tasks based on the user's needs:
- If user asks for "insights", "recommendations", or "advice" -> add GENERATE_WEATHER_INSIGHTS
- If user asks about "comfort", "feel", or "temperature comfort" -> add ANALYZE_COMFORT_CONDITIONS  
- If user asks about "activities", "what to do", or "suggestions" -> add SUGGEST_ACTIVITIES
- If user asks about "health", "safety", "clothing", or "what to wear" -> add ASSESS_HEALTH_FACTORS
- If user asks general weather questions, add GENERATE_WEATHER_INSIGHTS for enhanced response

Respond with a JSON array of tasks. Example:
[
  {
    "task_type": "GET_WEATHER",
    "parameters": {"city": "New York", "units": "imperial"},
    "description": "Get weather for New York"
  },
  {
    "task_type": "GENERATE_WEATHER_INSIGHTS",
    "parameters": {"weather_data": "WEATHER_DATA_PLACEHOLDER"},
    "description": "Generate comprehensive weather insights"
  }
]

Use "WEATHER_DATA_PLACEHOLDER" for insight task parameters - this will be replaced with actual weather data.

If the request is unclear or not supported, return an empty array []."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_request}
                ],
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            tasks_data = json.loads(content)
            
            # Convert to Task objects
            tasks = []
            for task_data in tasks_data:
                task_type = TaskType[task_data["task_type"]]
                tasks.append(Task(
                    task_type=task_type,
                    parameters=task_data["parameters"],
                    description=task_data.get("description", "")
                ))
            
            return tasks
            
        except json.JSONDecodeError as e:
            print(f"[{self.name}] Failed to parse AI response: {e}")
            return []
        except Exception as e:
            print(f"[{self.name}] Error decomposing request: {e}")
            return []
    
    def _compile_response(
        self,
        user_request: str,
        tasks: List[Task],
        results: List[TaskResult]
    ) -> str:
        """
        Compile task results into a final user-friendly response.
        
        Args:
            user_request: Original user request
            tasks: List of executed tasks
            results: List of task results
            
        Returns:
            Final formatted response
        """
        # Check for errors
        errors = [r.error for r in results if not r.success]
        if errors:
            return f"I encountered some issues:\n" + "\n".join(f"- {e}" for e in errors)
        
        # Prepare context for AI with enhanced insight formatting
        context = []
        weather_data = None
        insights_data = None
        
        for task, result in zip(tasks, results):
            if result.success:
                if task.task_type == TaskType.GET_WEATHER:
                    weather_data = result.data
                    context.append({
                        "task": "weather_data",
                        "result": result.data
                    })
                elif task.task_type == TaskType.GENERATE_WEATHER_INSIGHTS:
                    insights_data = result.data
                    # Format insights for better AI processing
                    formatted_insights = self.insight_formatter.format_comprehensive_insights(result.data)
                    context.append({
                        "task": "weather_insights",
                        "result": formatted_insights
                    })
                else:
                    context.append({
                        "task": task.description or task.task_type.value,
                        "result": result.data
                    })
        
        # Use AI to generate natural response with insights
        system_prompt = """You are a helpful weather assistant that creates natural, conversational responses with intelligent insights.

Given a user's request and the data gathered (which may include weather data and insights), create a clear and friendly response that:

1. Starts with the basic weather information
2. Incorporates insights naturally into the conversation
3. Prioritizes the most important insights based on weather conditions
4. Uses clear, non-technical language
5. Provides actionable recommendations
6. Organizes information logically (weather → insights → recommendations)

For insight data, look for these categories and present them appropriately:
- Comfort: How the weather feels and comfort levels
- Activities: What activities are recommended or should be avoided
- Health: Health considerations and safety advice
- Clothing: What to wear recommendations
- Patterns: Notable weather conditions or patterns

Make the response conversational and helpful, not just a list of facts."""

        context_str = json.dumps(context, indent=2)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User asked: {user_request}\n\nData gathered:\n{context_str}\n\nProvide a natural response:"}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"[{self.name}] Error generating response: {e}")
            # Fallback to simple formatting
            return self._simple_format_response(results)
    
    def _simple_format_response(self, results: List[TaskResult]) -> str:
        """Enhanced fallback response formatting with insights."""
        response_parts = []
        weather_info = None
        insights_info = []
        
        for result in results:
            if result.success and isinstance(result.data, dict):
                # Weather data
                if "temperature" in result.data:
                    data = result.data
                    temp_unit = "°C" if data.get("units") == "metric" else "°F"
                    weather_info = (
                        f"Weather in {data['city']}: {data['temperature']}{temp_unit}, "
                        f"{data['description']}. Humidity: {data['humidity']}%"
                    )
                # Insight data
                elif "comfort" in result.data or "activities" in result.data:
                    insights_info.append(self._format_insights_simple(result.data))
                elif "category" in result.data:  # Single insight result
                    insights_info.append(self._format_single_insight(result.data))
            elif result.success:
                response_parts.append(f"Result: {result.data}")
        
        # Combine weather and insights
        if weather_info:
            response_parts.append(weather_info)
        
        if insights_info:
            response_parts.extend(insights_info)
        
        return "\n\n".join(response_parts) if response_parts else "Task completed successfully."
    
    def _format_insights_simple(self, insights_data: Dict[str, Any]) -> str:
        """Format comprehensive insights data simply."""
        formatted_parts = []
        
        # Priority order for displaying insights
        priority_order = ["comfort", "health", "activities", "clothing", "patterns"]
        
        for category in priority_order:
            if category in insights_data:
                insight = insights_data[category]
                if insight.get("recommendations"):
                    category_name = category.capitalize()
                    recommendations = insight["recommendations"][:3]  # Limit to top 3
                    formatted_parts.append(f"{category_name}: {'; '.join(recommendations)}")
        
        return "\n".join(formatted_parts)
    
    def _format_single_insight(self, insight_data: Dict[str, Any]) -> str:
        """Format single insight result."""
        category = insight_data.get("category", "").capitalize()
        recommendations = insight_data.get("recommendations", [])
        
        if recommendations:
            return f"{category}: {'; '.join(recommendations[:3])}"
        return ""