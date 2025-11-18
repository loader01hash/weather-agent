"""OpenRouter AI-Powered Insight Engine for generating intelligent weather-based recommendations."""

import json
import requests
from typing import Dict, Any, List, Optional
from utils.message import InsightResult


class OpenRouterInsightEngine:
    """
    OpenRouter AI-powered weather insights engine that uses various models through OpenRouter API.
    Provides contextual, natural, and personalized weather recommendations.
    """
    
    def __init__(self, api_key: str, fallback_engine=None):
        """
        Initialize the OpenRouter Insight Engine.
        
        Args:
            api_key: OpenRouter API key
            fallback_engine: Fallback engine for when AI fails (optional)
        """
        import os
        self.name = "OpenRouter AI Insight Engine"
        self.api_key = api_key
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-20b:free")
        self.fallback_engine = fallback_engine
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        print(f"[{self.name}] Initialized with {self.model}")
    
    def generate_comfort_insights(self, weather_data: Dict[str, Any]) -> InsightResult:
        """Generate AI-powered comfort insights."""
        prompt = self._create_comfort_prompt(weather_data)
        
        try:
            ai_response = self._call_openrouter(prompt)
            return self._parse_ai_response(ai_response, "comfort")
        except Exception as e:
            print(f"[{self.name}] OpenRouter service failed for comfort insights: {e}")
            return self._fallback_comfort_insights(weather_data)
    
    def suggest_activities(self, weather_data: Dict[str, Any]) -> InsightResult:
        """Generate AI-powered activity suggestions."""
        prompt = self._create_activity_prompt(weather_data)
        
        try:
            ai_response = self._call_openrouter(prompt)
            return self._parse_ai_response(ai_response, "activities")
        except Exception as e:
            print(f"[{self.name}] OpenRouter service failed for activity suggestions: {e}")
            return self._fallback_activity_suggestions(weather_data)
    
    def analyze_health_factors(self, weather_data: Dict[str, Any]) -> InsightResult:
        """Generate AI-powered health analysis."""
        prompt = self._create_health_prompt(weather_data)
        
        try:
            ai_response = self._call_openrouter(prompt)
            return self._parse_ai_response(ai_response, "health")
        except Exception as e:
            print(f"[{self.name}] OpenRouter service failed for health analysis: {e}")
            return self._fallback_health_analysis(weather_data)
    
    def assess_clothing_recommendations(self, weather_data: Dict[str, Any]) -> InsightResult:
        """Generate AI-powered clothing recommendations."""
        prompt = self._create_clothing_prompt(weather_data)
        
        try:
            ai_response = self._call_openrouter(prompt)
            return self._parse_ai_response(ai_response, "clothing")
        except Exception as e:
            print(f"[{self.name}] OpenRouter service failed for clothing recommendations: {e}")
            return self._fallback_clothing_recommendations(weather_data)
    
    def identify_weather_patterns(self, weather_data: Dict[str, Any]) -> InsightResult:
        """Generate AI-powered weather pattern analysis."""
        prompt = self._create_pattern_prompt(weather_data)
        
        try:
            ai_response = self._call_openrouter(prompt)
            return self._parse_ai_response(ai_response, "patterns")
        except Exception as e:
            print(f"[{self.name}] OpenRouter service failed for pattern analysis: {e}")
            return self._fallback_pattern_analysis(weather_data)
    
    def _create_comfort_prompt(self, weather_data: Dict[str, Any]) -> str:
        """Create prompt for comfort analysis."""
        return f"""
Analyze the following weather conditions and provide comfort insights:

Weather Data:
- Location: {weather_data.get('city', 'Unknown')}
- Temperature: {weather_data.get('temperature', 'N/A')}°{('C' if weather_data.get('units') == 'metric' else 'F')}
- Humidity: {weather_data.get('humidity', 'N/A')}%
- Wind Speed: {weather_data.get('wind_speed', 'N/A')} {'m/s' if weather_data.get('units') == 'metric' else 'mph'}
- Conditions: {weather_data.get('description', 'N/A')}
- Cloud Cover: {weather_data.get('clouds', 'N/A')}%

Provide a comfort analysis focusing on:
1. How the weather will feel to an average person
2. Heat index or wind chill effects
3. Overall comfort level assessment
4. Practical recommendations for staying comfortable

Respond in JSON format:
{{
    "insights": ["insight1", "insight2"],
    "recommendations": ["rec1", "rec2", "rec3"],
    "priority": 1-5 (5 being most urgent),
    "confidence": 0.8-1.0
}}
"""
    
    def _create_activity_prompt(self, weather_data: Dict[str, Any]) -> str:
        """Create prompt for activity suggestions."""
        return f"""
Based on the current weather conditions, suggest appropriate activities:

Weather Data:
- Location: {weather_data.get('city', 'Unknown')}
- Temperature: {weather_data.get('temperature', 'N/A')}°{('C' if weather_data.get('units') == 'metric' else 'F')}
- Humidity: {weather_data.get('humidity', 'N/A')}%
- Wind Speed: {weather_data.get('wind_speed', 'N/A')} {'m/s' if weather_data.get('units') == 'metric' else 'mph'}
- Conditions: {weather_data.get('description', 'N/A')}
- Cloud Cover: {weather_data.get('clouds', 'N/A')}%

Provide activity suggestions considering:
1. Indoor vs outdoor suitability
2. Physical activity recommendations
3. Timing considerations (best times of day)
4. Specific activities that would be enjoyable
5. Activities to avoid

Be creative and specific with activity suggestions.

Respond in JSON format:
{{
    "insights": ["insight1", "insight2"],
    "recommendations": ["activity1", "activity2", "activity3"],
    "priority": 1-5,
    "confidence": 0.8-1.0
}}
"""
    
    def _create_health_prompt(self, weather_data: Dict[str, Any]) -> str:
        """Create prompt for health analysis."""
        return f"""
Analyze the weather conditions for health and safety considerations:

Weather Data:
- Location: {weather_data.get('city', 'Unknown')}
- Temperature: {weather_data.get('temperature', 'N/A')}°{('C' if weather_data.get('units') == 'metric' else 'F')}
- Humidity: {weather_data.get('humidity', 'N/A')}%
- Wind Speed: {weather_data.get('wind_speed', 'N/A')} {'m/s' if weather_data.get('units') == 'metric' else 'mph'}
- Conditions: {weather_data.get('description', 'N/A')}
- Pressure: {weather_data.get('pressure', 'N/A')} hPa

Focus on:
1. Heat/cold related health risks
2. Hydration needs and recommendations
3. UV exposure considerations
4. Air quality implications
5. Special considerations for vulnerable populations
6. Preventive health measures

Respond in JSON format:
{{
    "insights": ["health_insight1", "health_insight2"],
    "recommendations": ["health_rec1", "health_rec2", "health_rec3"],
    "priority": 1-5,
    "confidence": 0.8-1.0
}}
"""
    
    def _create_clothing_prompt(self, weather_data: Dict[str, Any]) -> str:
        """Create prompt for clothing recommendations."""
        return f"""
Provide detailed clothing recommendations based on the weather conditions:

Weather Data:
- Location: {weather_data.get('city', 'Unknown')}
- Temperature: {weather_data.get('temperature', 'N/A')}°{('C' if weather_data.get('units') == 'metric' else 'F')}
- Humidity: {weather_data.get('humidity', 'N/A')}%
- Wind Speed: {weather_data.get('wind_speed', 'N/A')} {'m/s' if weather_data.get('units') == 'metric' else 'mph'}
- Conditions: {weather_data.get('description', 'N/A')}
- Cloud Cover: {weather_data.get('clouds', 'N/A')}%

Consider:
1. Base layer clothing for the temperature
2. Weather protection (rain, wind, sun)
3. Fabric choices for comfort and functionality
4. Accessories (hats, gloves, sunglasses, umbrella)
5. Footwear recommendations
6. Layering strategies for changing conditions

Be specific and practical with clothing suggestions.

Respond in JSON format:
{{
    "insights": ["clothing_insight1", "clothing_insight2"],
    "recommendations": ["clothing_rec1", "clothing_rec2", "clothing_rec3"],
    "priority": 1-5,
    "confidence": 0.8-1.0
}}
"""
    
    def _create_pattern_prompt(self, weather_data: Dict[str, Any]) -> str:
        """Create prompt for weather pattern analysis."""
        return f"""
Analyze the weather patterns and identify notable conditions:

Weather Data:
- Location: {weather_data.get('city', 'Unknown')}
- Temperature: {weather_data.get('temperature', 'N/A')}°{('C' if weather_data.get('units') == 'metric' else 'F')}
- Humidity: {weather_data.get('humidity', 'N/A')}%
- Wind Speed: {weather_data.get('wind_speed', 'N/A')} {'m/s' if weather_data.get('units') == 'metric' else 'mph'}
- Conditions: {weather_data.get('description', 'N/A')}
- Pressure: {weather_data.get('pressure', 'N/A')} hPa
- Cloud Cover: {weather_data.get('clouds', 'N/A')}%

Identify:
1. Notable or unusual weather patterns
2. Seasonal appropriateness of conditions
3. Weather stability indicators
4. Potential weather changes to watch for
5. Interesting meteorological observations

Respond in JSON format:
{{
    "insights": ["pattern_insight1", "pattern_insight2"],
    "recommendations": ["pattern_rec1", "pattern_rec2"],
    "priority": 1-5,
    "confidence": 0.8-1.0
}}
"""
    
    def _call_openrouter(self, prompt: str) -> str:
        """Call OpenRouter API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/weather-insights-agent",
            "X-Title": "Weather Insights Agent"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a weather analysis expert providing practical, actionable insights. Always respond in valid JSON format as requested. Be specific, helpful, and focus on actionable recommendations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(
            self.base_url,
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")
        
        result = response.json()
        
        if "choices" not in result or not result["choices"]:
            raise Exception("No response from OpenRouter API")
        
        return result["choices"][0]["message"]["content"].strip()
    
    def _parse_ai_response(self, response: str, category: str) -> InsightResult:
        """Parse AI response into InsightResult."""
        try:
            # Clean up response to ensure valid JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            # Remove any markdown formatting
            response = response.replace("```", "").strip()
            
            data = json.loads(response)
            
            return InsightResult(
                category=category,
                insights=data.get("insights", []),
                recommendations=data.get("recommendations", []),
                priority=data.get("priority", 2),
                confidence=data.get("confidence", 0.85)
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[{self.name}] Failed to parse AI response: {e}")
            print(f"Raw response: {response}")
            
            # Try to extract useful information from malformed response
            return self._extract_fallback_insights(response, category)
    
    def _extract_fallback_insights(self, response: str, category: str) -> InsightResult:
        """Extract insights from malformed AI response."""
        # Simple extraction of useful information
        lines = response.split('\n')
        insights = []
        recommendations = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('{') and not line.startswith('}'):
                if len(line) > 10:  # Filter out short/meaningless lines
                    if len(insights) < 2:
                        insights.append(line)
                    elif len(recommendations) < 3:
                        recommendations.append(line)
        
        if not insights:
            insights = ["AI analysis provided general weather guidance"]
        if not recommendations:
            recommendations = ["Follow standard weather precautions"]
        
        return InsightResult(
            category=category,
            insights=insights,
            recommendations=recommendations,
            priority=2,
            confidence=0.6
        )
    
    def _fallback_comfort_insights(self, weather_data: Dict[str, Any]) -> InsightResult:
        """Fallback comfort insights when AI fails."""
        if self.fallback_engine:
            return self.fallback_engine.generate_comfort_insights(weather_data)
        
        temp = weather_data.get("temperature", 20)
        return InsightResult(
            category="comfort",
            insights=["Basic comfort analysis"],
            recommendations=[f"Temperature is {temp}°, dress accordingly"],
            priority=2,
            confidence=0.6
        )
    
    def _fallback_activity_suggestions(self, weather_data: Dict[str, Any]) -> InsightResult:
        """Fallback activity suggestions when AI fails."""
        if self.fallback_engine:
            return self.fallback_engine.suggest_activities(weather_data)
        
        return InsightResult(
            category="activities",
            insights=["Basic activity analysis"],
            recommendations=["Check weather conditions for outdoor activities"],
            priority=2,
            confidence=0.6
        )
    
    def _fallback_health_analysis(self, weather_data: Dict[str, Any]) -> InsightResult:
        """Fallback health analysis when AI fails."""
        if self.fallback_engine:
            return self.fallback_engine.analyze_health_factors(weather_data)
        
        return InsightResult(
            category="health",
            insights=["Basic health analysis"],
            recommendations=["Stay hydrated and dress appropriately"],
            priority=2,
            confidence=0.6
        )
    
    def _fallback_clothing_recommendations(self, weather_data: Dict[str, Any]) -> InsightResult:
        """Fallback clothing recommendations when AI fails."""
        if self.fallback_engine:
            return self.fallback_engine.assess_clothing_recommendations(weather_data)
        
        return InsightResult(
            category="clothing",
            insights=["Basic clothing analysis"],
            recommendations=["Dress according to temperature and conditions"],
            priority=2,
            confidence=0.6
        )
    
    def _fallback_pattern_analysis(self, weather_data: Dict[str, Any]) -> InsightResult:
        """Fallback pattern analysis when AI fails."""
        if self.fallback_engine:
            return self.fallback_engine.identify_weather_patterns(weather_data)
        
        return InsightResult(
            category="patterns",
            insights=["Basic pattern analysis"],
            recommendations=["Monitor weather conditions"],
            priority=1,
            confidence=0.6
        )