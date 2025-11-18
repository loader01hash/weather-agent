"""Agent B - Executor Agent that performs specific tasks."""

from typing import Dict, Any
from utils.message import Task, TaskResult, TaskType
from utils.weather_api import WeatherAPI
from utils.insight_engine import InsightEngine
from utils.openrouter_insight_engine import OpenRouterInsightEngine


class AgentB:
    """
    Executor Agent that performs specific tasks.
    Handles weather data retrieval, calculations, and data processing.
    """
    
    def __init__(self, weather_api_key: str, openrouter_api_key=None):
        """Initialize Agent B with weather API and OpenRouter."""
        self.name = "Agent B (Executor)"
        self.weather_api = WeatherAPI(weather_api_key)
        
        # Initialize fallback engine
        self.fallback_engine = InsightEngine()
        
        # Initialize OpenRouter
        if openrouter_api_key:
            self.insight_engine = OpenRouterInsightEngine(
                api_key=openrouter_api_key,
                fallback_engine=self.fallback_engine
            )
        else:
            # Use fallback engine if no OpenRouter key
            self.insight_engine = self.fallback_engine
        
        print(f"[{self.name}] Initialized and ready to execute tasks")
    
    def execute_task(self, task: Task) -> TaskResult:
        """
        Execute a task and return the result.
        
        Args:
            task: Task object containing type and parameters
            
        Returns:
            TaskResult with success status and data
        """
        print(f"[{self.name}] Executing task: {task.task_type.value}")
        
        try:
            if task.task_type == TaskType.GET_WEATHER:
                return self._get_weather(task.parameters)
            elif task.task_type == TaskType.CALCULATE:
                return self._calculate(task.parameters)
            elif task.task_type == TaskType.GENERATE_WEATHER_INSIGHTS:
                return self._generate_weather_insights(task.parameters)
            elif task.task_type == TaskType.ANALYZE_COMFORT_CONDITIONS:
                return self._analyze_comfort_conditions(task.parameters)
            elif task.task_type == TaskType.SUGGEST_ACTIVITIES:
                return self._suggest_activities(task.parameters)
            elif task.task_type == TaskType.ASSESS_HEALTH_FACTORS:
                return self._assess_health_factors(task.parameters)
            else:
                return TaskResult(
                    success=False,
                    data=None,
                    error=f"Unknown task type: {task.task_type}"
                )
        except Exception as e:
            print(f"[{self.name}] Error executing task: {str(e)}")
            return TaskResult(
                success=False,
                data=None,
                error=f"Task execution failed: {str(e)}"
            )
    
    def _get_weather(self, parameters: Dict[str, Any]) -> TaskResult:
        """
        Fetch weather data for a city.
        
        Args:
            parameters: Must contain 'city' key
            
        Returns:
            TaskResult with weather data
        """
        city = parameters.get("city")
        if not city:
            return TaskResult(
                success=False,
                data=None,
                error="City parameter is required"
            )
        
        units = parameters.get("units", "metric")
        
        try:
            weather_data = self.weather_api.get_weather(city, units)
            print(f"[{self.name}] Successfully fetched weather for {city}")
            return TaskResult(
                success=True,
                data=weather_data
            )
        except Exception as e:
            return TaskResult(
                success=False,
                data=None,
                error=f"Failed to get weather: {str(e)}"
            )
    
    def _calculate(self, parameters: Dict[str, Any]) -> TaskResult:
        """
        Perform calculations.
        
        Args:
            parameters: Must contain 'operation' and 'values'
            
        Returns:
            TaskResult with calculation result
        """
        operation = parameters.get("operation")
        values = parameters.get("values", [])
        
        if not operation or not values:
            return TaskResult(
                success=False,
                data=None,
                error="Operation and values are required"
            )
        
        try:
            if operation == "sum":
                result = sum(values)
            elif operation == "average":
                result = sum(values) / len(values)
            elif operation == "max":
                result = max(values)
            elif operation == "min":
                result = min(values)
            else:
                return TaskResult(
                    success=False,
                    data=None,
                    error=f"Unknown operation: {operation}"
                )
            
            return TaskResult(
                success=True,
                data=result
            )
        except Exception as e:
            return TaskResult(
                success=False,
                data=None,
                error=f"Calculation failed: {str(e)}"
            )
    
    def _generate_weather_insights(self, parameters: Dict[str, Any]) -> TaskResult:
        """
        Generate comprehensive weather insights combining multiple analysis types.
        
        Args:
            parameters: Must contain 'weather_data' key
            
        Returns:
            TaskResult with comprehensive insights
        """
        weather_data = parameters.get("weather_data")
        if not weather_data:
            return TaskResult(
                success=False,
                data=None,
                error="Weather data parameter is required for insight generation"
            )
        
        try:
            # Generate all types of insights
            comfort_insights = self.insight_engine.generate_comfort_insights(weather_data)
            activity_insights = self.insight_engine.suggest_activities(weather_data)
            health_insights = self.insight_engine.analyze_health_factors(weather_data)
            clothing_insights = self.insight_engine.assess_clothing_recommendations(weather_data)
            pattern_insights = self.insight_engine.identify_weather_patterns(weather_data)
            
            # Combine all insights
            all_insights = {
                "comfort": comfort_insights.to_dict(),
                "activities": activity_insights.to_dict(),
                "health": health_insights.to_dict(),
                "clothing": clothing_insights.to_dict(),
                "patterns": pattern_insights.to_dict()
            }
            
            print(f"[{self.name}] Successfully generated comprehensive weather insights")
            return TaskResult(
                success=True,
                data=all_insights
            )
        except Exception as e:
            return TaskResult(
                success=False,
                data=None,
                error=f"Failed to generate insights: {str(e)}"
            )
    
    def _analyze_comfort_conditions(self, parameters: Dict[str, Any]) -> TaskResult:
        """
        Analyze comfort conditions based on weather data.
        
        Args:
            parameters: Must contain 'weather_data' key
            
        Returns:
            TaskResult with comfort analysis
        """
        weather_data = parameters.get("weather_data")
        if not weather_data:
            return TaskResult(
                success=False,
                data=None,
                error="Weather data parameter is required for comfort analysis"
            )
        
        try:
            comfort_insights = self.insight_engine.generate_comfort_insights(weather_data)
            print(f"[{self.name}] Successfully analyzed comfort conditions")
            return TaskResult(
                success=True,
                data=comfort_insights.to_dict()
            )
        except Exception as e:
            return TaskResult(
                success=False,
                data=None,
                error=f"Failed to analyze comfort conditions: {str(e)}"
            )
    
    def _suggest_activities(self, parameters: Dict[str, Any]) -> TaskResult:
        """
        Suggest activities based on weather conditions.
        
        Args:
            parameters: Must contain 'weather_data' key
            
        Returns:
            TaskResult with activity suggestions
        """
        weather_data = parameters.get("weather_data")
        if not weather_data:
            return TaskResult(
                success=False,
                data=None,
                error="Weather data parameter is required for activity suggestions"
            )
        
        try:
            activity_insights = self.insight_engine.suggest_activities(weather_data)
            print(f"[{self.name}] Successfully generated activity suggestions")
            return TaskResult(
                success=True,
                data=activity_insights.to_dict()
            )
        except Exception as e:
            return TaskResult(
                success=False,
                data=None,
                error=f"Failed to suggest activities: {str(e)}"
            )
    
    def _assess_health_factors(self, parameters: Dict[str, Any]) -> TaskResult:
        """
        Assess health factors based on weather conditions.
        
        Args:
            parameters: Must contain 'weather_data' key
            
        Returns:
            TaskResult with health assessment
        """
        weather_data = parameters.get("weather_data")
        if not weather_data:
            return TaskResult(
                success=False,
                data=None,
                error="Weather data parameter is required for health assessment"
            )
        
        try:
            health_insights = self.insight_engine.analyze_health_factors(weather_data)
            clothing_insights = self.insight_engine.assess_clothing_recommendations(weather_data)
            
            # Combine health and clothing insights
            combined_insights = {
                "health": health_insights.to_dict(),
                "clothing": clothing_insights.to_dict()
            }
            
            print(f"[{self.name}] Successfully assessed health factors")
            return TaskResult(
                success=True,
                data=combined_insights
            )
        except Exception as e:
            return TaskResult(
                success=False,
                data=None,
                error=f"Failed to assess health factors: {str(e)}"
            )