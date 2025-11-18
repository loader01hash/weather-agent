"""Smart Agent A using OpenRouter instead of OpenAI for contextual responses."""

import json
import requests
from typing import List, Dict, Any, Optional
from utils.message import Task, TaskType, TaskResult
from agents.agent_b import AgentB


class OpenRouterSmartAgent:
    """
    Smart Coordinator Agent that provides contextual, query-specific responses
    using OpenRouter API (works with your existing setup).
    """
    
    def __init__(self, openrouter_api_key: str, agent_b: AgentB):
        """Initialize Smart Agent with OpenRouter API and reference to Agent B."""
        import os
        self.name = "OpenRouter Smart Agent (Contextual Coordinator)"
        self.api_key = openrouter_api_key
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-oss-20b:free")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.agent_b = agent_b
        print(f"[{self.name}] Initialized with contextual capabilities using OpenRouter ({self.model})")
    
    def process_request(self, user_request: str) -> str:
        """
        Process a user request with contextual understanding.
        
        Args:
            user_request: Natural language request from user
            
        Returns:
            Contextual response string
        """
        print(f"\n[{self.name}] Processing contextual request: '{user_request}'")
        
        # Step 1: Analyze the query for context and intent
        query_analysis = self._analyze_query_context(user_request)
        
        if not query_analysis.get("needs_weather", True):
            return "I can help you with weather-related questions. Please ask about weather conditions, clothing recommendations, activities, or health considerations for a specific location."
        
        # Step 2: Check if this is a comparison query
        intent = query_analysis.get("intent", "general")
        if intent == "comparison":
            return self._handle_comparison_query(user_request)
        
        # Step 3: Extract location for single city queries
        location = query_analysis.get("location")
        if not location or location == "unknown":
            return "I need to know the location to provide weather insights. Please specify a city or location in your request."
        
        # Step 4: Get weather data
        weather_task = Task(
            task_type=TaskType.GET_WEATHER,
            parameters={"city": location, "units": "metric"},
            description=f"Get weather for {location}"
        )
        
        weather_result = self.agent_b.execute_task(weather_task)
        
        if not weather_result.success:
            return f"I couldn't get weather data for {location}. Please check the location name and try again."
        
        weather_data = weather_result.data
        
        # Step 5: Generate contextual insights based on query intent
        contextual_response = self._generate_contextual_response(
            user_request, weather_data, query_analysis
        )
        
        print(f"[{self.name}] Generated contextual response")
        return contextual_response
    
    def _call_openrouter(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Call OpenRouter API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/weather-insights-agent",
            "X-Title": "Weather Insights Agent"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                raise Exception(f"OpenRouter API error: {response.status_code}")
            
            result = response.json()
            
            if "choices" not in result or not result["choices"]:
                raise Exception("No response from OpenRouter API")
            
            return result["choices"][0]["message"]["content"].strip()
            
        except Exception as e:
            print(f"[{self.name}] OpenRouter API call failed: {e}")
            raise e
    
    def _analyze_query_context(self, user_request: str) -> Dict[str, Any]:
        """Analyze user query to understand context and intent."""
        
        analysis_prompt = f"""
        Analyze this weather-related query to understand the user's specific intent and needs:
        
        Query: "{user_request}"
        
        Determine:
        1. Primary intent (clothing, activities, health, comfort, general, priority)
        2. Location mentioned (city name or "unknown")
        3. Specific needs (what exactly they want to know)
        4. Time context (morning, evening, today, etc. or "none")
        5. Activity type if mentioned (running, hiking, driving, etc. or "none")
        6. Whether this needs weather data (true/false)
        
        Examples:
        - "What should I wear in Paris?" → intent: clothing, location: Paris, needs: outfit_advice
        - "Is it good for running in Chicago?" → intent: activities, location: Chicago, needs: running_conditions, activity_type: running
        - "Should I worry about Phoenix heat?" → intent: health, location: Phoenix, needs: heat_safety
        - "What's most important about Seattle weather?" → intent: priority, location: Seattle, needs: key_information
        
        Respond in JSON format:
        {{
            "intent": "clothing|activities|health|comfort|general|priority",
            "location": "city name or unknown",
            "specific_needs": ["need1", "need2"],
            "time_context": "time context or none",
            "activity_type": "activity or none",
            "needs_weather": true
        }}
        """
        
        try:
            messages = [
                {"role": "system", "content": "You are a query analysis expert. Always respond with valid JSON."},
                {"role": "user", "content": analysis_prompt}
            ]
            
            content = self._call_openrouter(messages, temperature=0.1)
            
            # Clean up JSON response
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            analysis = json.loads(content)
            
            # Validate and set defaults
            analysis.setdefault("intent", "general")
            analysis.setdefault("location", "unknown")
            analysis.setdefault("specific_needs", ["weather_info"])
            analysis.setdefault("time_context", "none")
            analysis.setdefault("activity_type", "none")
            analysis.setdefault("needs_weather", True)
            
            return analysis
            
        except (json.JSONDecodeError, Exception) as e:
            print(f"[{self.name}] Query analysis failed: {e}")
            # Fallback analysis
            return {
                "intent": self._simple_intent_detection(user_request),
                "location": self._simple_location_extraction(user_request),
                "specific_needs": ["weather_info"],
                "time_context": "none",
                "activity_type": "none",
                "needs_weather": True
            }
    
    def _simple_intent_detection(self, query: str) -> str:
        """Simple fallback intent detection."""
        query_lower = query.lower()
        
        # Multi-city comparison queries
        if any(word in query_lower for word in ["compare", "comparison", "vs", "versus", "difference", "between"]):
            return "comparison"
        # Travel and planning queries
        elif any(word in query_lower for word in ["travel", "trip", "vacation", "holiday", "visit", "going to"]):
            return "travel_planning"
        elif any(word in query_lower for word in ["pack", "packing", "luggage", "suitcase", "bring"]):
            return "packing_advice"
        elif any(word in query_lower for word in ["weekend", "tomorrow", "next week", "this week", "plan"]):
            return "planning"
        # Event and occasion queries
        elif any(word in query_lower for word in ["wedding", "party", "event", "celebration", "ceremony"]):
            return "event_planning"
        elif any(word in query_lower for word in ["work", "office", "meeting", "business", "professional"]):
            return "work_attire"
        elif any(word in query_lower for word in ["date", "dinner", "restaurant", "going out"]):
            return "social_occasion"
        # Specific weather condition queries
        elif any(word in query_lower for word in ["raining", "rain", "rainy", "drizzle", "shower"]):
            return "rain_check"
        elif any(word in query_lower for word in ["sunny", "sun", "clear", "bright"]):
            return "sun_check"
        elif any(word in query_lower for word in ["cloudy", "clouds", "overcast"]):
            return "cloud_check"
        elif any(word in query_lower for word in ["windy", "wind", "breezy"]):
            return "wind_check"
        elif any(word in query_lower for word in ["snowing", "snow", "snowy"]):
            return "snow_check"
        elif any(word in query_lower for word in ["hot", "heat", "warm", "temperature"]):
            return "temperature_check"
        elif any(word in query_lower for word in ["cold", "cool", "chilly", "freezing"]):
            return "cold_check"
        elif any(word in query_lower for word in ["humid", "humidity", "muggy", "sticky"]):
            return "humidity_check"
        # Activity-specific queries
        elif any(word in query_lower for word in ["cricket", "play cricket", "cricket match"]):
            return "cricket"
        elif any(word in query_lower for word in ["football", "soccer", "play football"]):
            return "football"
        elif any(word in query_lower for word in ["tennis", "play tennis"]):
            return "tennis"
        elif any(word in query_lower for word in ["running", "jogging", "run", "jog"]):
            return "running"
        elif any(word in query_lower for word in ["cycling", "bike", "biking"]):
            return "cycling"
        elif any(word in query_lower for word in ["swimming", "swim"]):
            return "swimming"
        elif any(word in query_lower for word in ["hiking", "trekking", "trek"]):
            return "hiking"
        # General intents
        elif any(word in query_lower for word in ["wear", "clothing", "dress", "jacket", "coat"]):
            return "clothing"
        elif any(word in query_lower for word in ["activity", "exercise", "sports", "outdoor", "play"]):
            return "activities"
        elif any(word in query_lower for word in ["health", "safe", "safety", "dangerous", "concern"]):
            return "health"
        elif any(word in query_lower for word in ["important", "priority", "main", "key", "most"]):
            return "priority"
        else:
            return "general"
    
    def _extract_multiple_locations(self, query: str) -> List[str]:
        """Extract multiple locations from query for comparison."""
        cities = [
            "new york", "london", "paris", "tokyo", "miami", "chicago", 
            "seattle", "phoenix", "berlin", "sydney", "toronto", "boston",
            "los angeles", "san francisco", "denver", "atlanta", "houston",
            "bangalore", "mumbai", "delhi", "chennai", "kolkata", "hyderabad"
        ]
        
        query_lower = query.lower()
        found_cities = []
        
        # Find all cities mentioned in the query
        for city in cities:
            if city in query_lower:
                found_cities.append(city.title())
        
        # Also check for "and" patterns like "city1 and city2"
        words = query.split()
        for i, word in enumerate(words):
            if word.lower() in ["and", "&", "vs", "versus"] and i > 0 and i < len(words) - 1:
                # Check words around "and"
                prev_word = words[i-1].lower().replace(",", "").replace(".", "")
                next_word = words[i+1].lower().replace(",", "").replace(".", "")
                
                for city in cities:
                    if city == prev_word and city.title() not in found_cities:
                        found_cities.append(city.title())
                    if city == next_word and city.title() not in found_cities:
                        found_cities.append(city.title())
        
        return found_cities if found_cities else ["unknown"]
    
    def _simple_location_extraction(self, query: str) -> str:
        """Simple location extraction - returns first city found."""
        locations = self._extract_multiple_locations(query)
        return locations[0] if locations else "unknown"
    
    def _handle_comparison_query(self, user_request: str) -> str:
        """Handle multi-city comparison queries."""
        cities = self._extract_multiple_locations(user_request)
        
        if len(cities) < 2:
            return "I need at least two cities to compare. Please specify cities like 'compare weather in Delhi and Mumbai'."
        
        if len(cities) > 3:
            cities = cities[:3]  # Limit to 3 cities for performance
        
        weather_data_list = []
        
        # Get weather data for each city
        for city in cities:
            weather_task = Task(
                task_type=TaskType.GET_WEATHER,
                parameters={"city": city, "units": "metric"},
                description=f"Get weather for {city}"
            )
            
            weather_result = self.agent_b.execute_task(weather_task)
            
            if weather_result.success:
                weather_data_list.append({
                    "city": city,
                    "data": weather_result.data
                })
            else:
                weather_data_list.append({
                    "city": city,
                    "data": None,
                    "error": f"Could not get weather data for {city}"
                })
        
        # Generate comparison response
        return self._create_comparison_response(weather_data_list, user_request)
    
    def _create_comparison_response(self, weather_data_list: List[Dict], user_request: str) -> str:
        """Create a comparison response for multiple cities."""
        
        response = "🌤️ Weather Comparison:\n\n"
        
        # Add individual city data
        for item in weather_data_list:
            city = item["city"]
            data = item.get("data")
            
            if data:
                temp = data.get("temperature", "N/A")
                temp_unit = "°C" if data.get("units") == "metric" else "°F"
                description = data.get("description", "N/A")
                humidity = data.get("humidity", "N/A")
                wind_speed = data.get("wind_speed", "N/A")
                feels_like = data.get("feels_like", temp)
                
                response += f"📍 {city}:\n"
                response += f"   Temperature: {temp}{temp_unit} (feels like {feels_like}{temp_unit})\n"
                response += f"   Conditions: {description}\n"
                response += f"   Humidity: {humidity}%\n"
                response += f"   Wind: {wind_speed} m/s\n\n"
            else:
                response += f"📍 {city}: ❌ {item.get('error', 'Data unavailable')}\n\n"
        
        # Add comparison insights
        valid_data = [item for item in weather_data_list if item.get("data")]
        
        if len(valid_data) >= 2:
            response += "📊 Comparison Insights:\n"
            
            # Temperature comparison
            temps = []
            for item in valid_data:
                temp = item["data"].get("temperature")
                if temp and isinstance(temp, (int, float)):
                    temps.append((item["city"], temp))
            
            if temps:
                temps.sort(key=lambda x: x[1])
                response += f"🌡️ Temperature: {temps[0][0]} is coolest ({temps[0][1]}°C), "
                response += f"{temps[-1][0]} is warmest ({temps[-1][1]}°C)\n"
            
            # Humidity comparison
            humidities = []
            for item in valid_data:
                humidity = item["data"].get("humidity")
                if humidity and isinstance(humidity, (int, float)):
                    humidities.append((item["city"], humidity))
            
            if humidities:
                humidities.sort(key=lambda x: x[1])
                response += f"💧 Humidity: {humidities[0][0]} is driest ({humidities[0][1]}%), "
                response += f"{humidities[-1][0]} is most humid ({humidities[-1][1]}%)\n"
            
            # Weather condition insights
            conditions = {}
            for item in valid_data:
                condition = item["data"].get("description", "").lower()
                city = item["city"]
                if "rain" in condition:
                    conditions[city] = "🌧️ Rainy"
                elif "clear" in condition or "sunny" in condition:
                    conditions[city] = "☀️ Clear"
                elif "cloud" in condition:
                    conditions[city] = "☁️ Cloudy"
                else:
                    conditions[city] = f"🌤️ {condition.title()}"
            
            if conditions:
                response += f"🌈 Conditions: "
                response += ", ".join([f"{city} - {cond}" for city, cond in conditions.items()])
        
        return response
    
    def _wants_detailed_response(self, query: str) -> bool:
        """Check if user wants detailed information."""
        query_lower = query.lower()
        
        detailed_indicators = [
            "detailed", "detail", "complete", "comprehensive", "full",
            "top to bottom", "head to toe", "everything", "all",
            "step by step", "thorough", "extensive"
        ]
        
        return any(indicator in query_lower for indicator in detailed_indicators)
    
    def _is_simple_query(self, query: str) -> bool:
        """Check if this is a simple temperature/weather query."""
        query_lower = query.lower()
        
        # Simple query patterns (basic weather info only)
        simple_patterns = [
            "temperature in",
            "temperature of", 
            "temp in",
            "temp of",
            "current temperature",
            "today's temperature"
        ]
        
        # Complex query indicators (need detailed responses)
        complex_indicators = [
            "wear", "clothing", "dress", "jacket", "coat", "outfit",
            "activity", "activities", "running", "hiking", "exercise",
            "health", "safe", "safety", "concern", "worried",
            "important", "priority", "should i", "can i",
            "good for", "bad for", "recommend", "suggest",
            "what to", "how to", "advice", "tips",
            # Specific weather condition queries
            "raining", "rain", "rainy", "drizzle", "shower",
            "sunny", "sun", "clear", "bright",
            "cloudy", "clouds", "overcast",
            "windy", "wind", "breezy",
            "snowing", "snow", "snowy",
            "is it", "will it", "does it",
            # Sports and activities
            "cricket", "football", "soccer", "tennis", "swimming", "cycling",
            "bike", "biking", "jogging", "jog", "trek", "trekking",
            "play", "sport", "sports", "game", "match", "outdoor",
            # Comparison queries
            "compare", "comparison", "vs", "versus", "difference", "between",
            # Travel and planning
            "travel", "trip", "vacation", "holiday", "visit", "going to",
            "pack", "packing", "luggage", "suitcase", "bring",
            "weekend", "tomorrow", "next week", "this week", "plan",
            # Events and occasions
            "wedding", "party", "event", "celebration", "ceremony",
            "work", "office", "meeting", "business", "professional",
            "date", "dinner", "restaurant", "going out",
            # Weather condition checks
            "hot", "heat", "warm", "cold", "cool", "chilly", "freezing",
            "humid", "humidity", "muggy", "sticky"
        ]
        
        # Weather queries that should get detailed responses
        detailed_weather_patterns = [
            "weather in",
            "weather of", 
            "how's the weather",
            "what's the weather"
        ]
        
        # Check if it's a simple pattern
        has_simple_pattern = any(pattern in query_lower for pattern in simple_patterns)
        
        # Check if it has complex indicators
        has_complex_indicators = any(indicator in query_lower for indicator in complex_indicators)
        
        # Check if it's a detailed weather query
        has_detailed_weather = any(pattern in query_lower for pattern in detailed_weather_patterns)
        
        # It's simple only if it has simple patterns and no complex indicators
        # Detailed weather queries are treated as complex for better responses
        return has_simple_pattern and not has_complex_indicators and not has_detailed_weather
    
    def _generate_contextual_response(self, user_request: str, weather_data: Dict[str, Any], 
                                    query_analysis: Dict[str, Any]) -> str:
        """Generate contextual response based on query analysis."""
        
        intent = query_analysis.get("intent", "general")
        specific_needs = query_analysis.get("specific_needs", [])
        activity_type = query_analysis.get("activity_type", "none")
        time_context = query_analysis.get("time_context", "none")
        
        # Create context-specific prompt
        contextual_prompt = self._create_contextual_prompt(
            user_request, weather_data, intent, specific_needs, activity_type, time_context
        )
        
        try:
            messages = [
                {"role": "system", "content": "You are a helpful weather assistant that provides specific, actionable advice based on the user's exact question. Be conversational and focus on what they actually need to know."},
                {"role": "user", "content": contextual_prompt}
            ]
            
            return self._call_openrouter(messages, temperature=0.7)
            
        except Exception as e:
            print(f"[{self.name}] Contextual response generation failed: {e}")
            return self._create_fallback_response(user_request, weather_data, intent)
    
    def _create_contextual_prompt(self, user_request: str, weather_data: Dict[str, Any], 
                                intent: str, specific_needs: List[str], activity_type: str, 
                                time_context: str) -> str:
        """Create a context-specific prompt."""
        
        # Base weather information
        temp = weather_data.get("temperature", "N/A")
        temp_unit = "°C" if weather_data.get("units") == "metric" else "°F"
        city = weather_data.get("city", "Unknown")
        description = weather_data.get("description", "N/A")
        humidity = weather_data.get("humidity", "N/A")
        wind_speed = weather_data.get("wind_speed", "N/A")
        
        base_info = f"""
        Current Weather in {city}:
        - Temperature: {temp}{temp_unit}
        - Conditions: {description}
        - Humidity: {humidity}%
        - Wind Speed: {wind_speed} m/s
        """
        
        # Check if this is a simple temperature query and if user wants detailed info
        is_simple_query = self._is_simple_query(user_request)
        wants_detailed = self._wants_detailed_response(user_request)
        
        if is_simple_query and not wants_detailed:
            # For simple queries, provide short and crisp responses
            simple_instruction = f"""
            The user asked a simple question about temperature/weather. Provide a SHORT and CRISP response (1-2 sentences max).
            
            Examples:
            - "What's the temperature in Bangalore?" → "It's 24.9°C in Bangalore with hazy conditions."
            - "How's the weather in Delhi?" → "Delhi is 18°C with clear skies and light wind."
            - "Temperature in Mumbai?" → "Mumbai is currently 28°C with partly cloudy skies."
            
            Keep it brief and direct. Only mention temperature and main condition.
            """
        else:
            # For specific queries, provide detailed contextual responses
            if intent == "clothing":
                specific_instruction = """
                Focus specifically on clothing recommendations:
                - What to wear for this temperature and conditions
                - Layering advice if needed
                - Accessories (umbrella, hat, sunglasses)
                - Fabric choices for comfort
                
                Be specific about clothing items and explain why they're recommended.
                """
            elif intent == "activities":
                activity_context = f" for {activity_type}" if activity_type != "none" else ""
                specific_instruction = f"""
                Focus on activity recommendations{activity_context}:
                - Safety for outdoor vs indoor activities
                - Best timing during the day
                - Specific activities that would be enjoyable
                - Activities to avoid in these conditions
                
                Be specific about what activities are good and when to do them.
                """
            elif intent == "health":
                specific_instruction = """
                Focus on health and safety considerations:
                - Health risks from current conditions
                - Hydration and safety needs
                - UV exposure and protection
                - Temperature-related health concerns
                
                Prioritize safety and health recommendations.
                """
            elif intent == "priority":
                specific_instruction = """
                Focus on the most important information:
                - What's the key thing to know about this weather
                - Top priority for planning the day
                - Most important precaution or preparation
                
                Identify and emphasize the most important aspect.
                """
            else:
                specific_instruction = """
                Provide focused weather insights:
                - Key conditions to be aware of
                - General recommendations for the day
                - Notable weather patterns
                """
        
        time_context_text = f"\nTime Context: {time_context}" if time_context != "none" else ""
        needs_text = f"\nSpecific Needs: {', '.join(specific_needs)}" if specific_needs else ""
        
        if is_simple_query:
            full_prompt = f"""
            User asked: "{user_request}"
            
            {base_info}
            
            {simple_instruction}
            """
        else:
            full_prompt = f"""
            User asked: "{user_request}"
            
            {base_info}
            {time_context_text}
            {needs_text}
            
            {specific_instruction}
            
            Provide a natural, conversational response that directly answers their question with actionable advice.
            """
        
        return full_prompt
    
    def _create_fallback_response(self, user_request: str, weather_data: Dict[str, Any], intent: str) -> str:
        """Create an enhanced fallback response with more weather details."""
        
        temp = weather_data.get("temperature", "N/A")
        temp_unit = "°C" if weather_data.get("units") == "metric" else "°F"
        description = weather_data.get("description", "N/A")
        city = weather_data.get("city", "Unknown")
        humidity = weather_data.get("humidity", "N/A")
        wind_speed = weather_data.get("wind_speed", "N/A")
        feels_like = weather_data.get("feels_like", temp)
        
        # Create a more comprehensive response
        base_response = f"Current weather in {city}: {temp}{temp_unit} with {description}."
        
        # Add feels like temperature if different
        if feels_like != temp:
            base_response += f" Feels like {feels_like}{temp_unit}."
        
        # Add humidity and wind if available
        if humidity != "N/A":
            base_response += f" Humidity: {humidity}%."
        
        if wind_speed != "N/A":
            base_response += f" Wind: {wind_speed} m/s."
        
        # Add detailed clothing recommendations
        if intent == "clothing":
            if temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 15
                
                base_response += "\n\n👕 Clothing Recommendations (Top to Bottom):\n"
                
                if temp_val < 5:  # Very cold
                    base_response += "• Head: Warm beanie or winter hat\n"
                    base_response += "• Upper: Thermal base layer + warm sweater + heavy winter jacket\n"
                    base_response += "• Lower: Thermal underwear + warm pants/jeans\n"
                    base_response += "• Feet: Thick socks + insulated boots\n"
                    base_response += "• Accessories: Gloves, scarf, warm layers essential"
                    
                elif temp_val < 10:  # Cold
                    base_response += "• Head: Light beanie or cap (optional)\n"
                    base_response += "• Upper: Long-sleeve shirt + warm sweater + jacket\n"
                    base_response += "• Lower: Long pants or jeans\n"
                    base_response += "• Feet: Regular socks + closed shoes or boots\n"
                    base_response += "• Accessories: Light scarf, consider gloves"
                    
                elif temp_val < 15:  # Cool
                    base_response += "• Head: Light cap (optional)\n"
                    base_response += "• Upper: Long-sleeve shirt + light sweater or cardigan\n"
                    base_response += "• Lower: Long pants or jeans\n"
                    base_response += "• Feet: Regular socks + comfortable shoes\n"
                    base_response += "• Accessories: Light jacket for evening"
                    
                elif temp_val < 20:  # Mild
                    base_response += "• Head: Sun hat (if sunny)\n"
                    base_response += "• Upper: Long-sleeve shirt or light sweater\n"
                    base_response += "• Lower: Long pants, jeans, or light trousers\n"
                    base_response += "• Feet: Regular socks + comfortable shoes\n"
                    base_response += "• Accessories: Light jacket for cooler moments"
                    
                elif temp_val < 25:  # Comfortable
                    base_response += "• Head: Sun hat or cap (if sunny)\n"
                    base_response += "• Upper: T-shirt or light blouse\n"
                    base_response += "• Lower: Light pants, jeans, or knee-length shorts\n"
                    base_response += "• Feet: Light socks + comfortable shoes or sneakers\n"
                    base_response += "• Accessories: Light cardigan for air-conditioned spaces"
                    
                elif temp_val < 30:  # Warm
                    base_response += "• Head: Sun hat or cap for UV protection\n"
                    base_response += "• Upper: Light t-shirt or tank top\n"
                    base_response += "• Lower: Shorts or light, breathable pants\n"
                    base_response += "• Feet: Light socks + breathable shoes or sandals\n"
                    base_response += "• Accessories: Sunglasses, light cardigan for indoors"
                    
                else:  # Hot
                    base_response += "• Head: Wide-brim hat for sun protection\n"
                    base_response += "• Upper: Light, breathable t-shirt or tank top\n"
                    base_response += "• Lower: Light shorts or breathable pants\n"
                    base_response += "• Feet: Minimal socks + sandals or breathable shoes\n"
                    base_response += "• Accessories: Sunglasses, umbrella for shade, stay hydrated"
                
                # Add weather condition specific advice
                if "rain" in description.lower() or "drizzle" in description.lower():
                    base_response += "\n\n☔ Rain Protection:\n"
                    base_response += "• Waterproof jacket or raincoat\n"
                    base_response += "• Umbrella\n"
                    base_response += "• Waterproof shoes or boots"
                    
                elif "snow" in description.lower():
                    base_response += "\n\n❄️ Snow Protection:\n"
                    base_response += "• Waterproof winter boots with good grip\n"
                    base_response += "• Water-resistant outer layer\n"
                    base_response += "• Extra warm layers"
                
                if wind_speed != "N/A" and isinstance(wind_speed, (int, float)) and wind_speed > 10:
                    base_response += "\n\n💨 Windy Conditions:\n"
                    base_response += "• Wind-resistant jacket\n"
                    base_response += "• Secure hat or avoid loose accessories\n"
                    base_response += "• Extra layer for wind chill"
        
        # Handle travel and planning queries
        elif intent == "travel_planning":
            base_response = f"Travel weather advice for {city}: "
            if temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 20
                base_response += f"Current temperature: {temp}{temp_unit}, conditions: {description}. "
                
                if temp_val > 30:
                    base_response += "Hot destination - pack light, breathable clothing, sunscreen, and stay hydrated."
                elif temp_val < 10:
                    base_response += "Cold destination - pack warm layers, waterproof jacket, and winter accessories."
                else:
                    base_response += "Moderate climate - pack versatile clothing for layering."
                
                if "rain" in description.lower():
                    base_response += " Rain expected - bring waterproof gear and umbrella."
        
        elif intent == "packing_advice":
            base_response = f"Packing advice for {city} weather: "
            if temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 20
                
                base_response += f"Temperature: {temp}{temp_unit}, conditions: {description}.\n\n"
                base_response += "📦 Packing Essentials:\n"
                
                if temp_val > 25:
                    base_response += "• Light, breathable fabrics (cotton, linen)\n"
                    base_response += "• Shorts, t-shirts, sundresses\n"
                    base_response += "• Sandals and breathable shoes\n"
                    base_response += "• Sunscreen, sunglasses, hat\n"
                elif temp_val < 15:
                    base_response += "• Warm layers (sweaters, jackets)\n"
                    base_response += "• Long pants, thermal underwear\n"
                    base_response += "• Closed shoes, warm socks\n"
                    base_response += "• Gloves, scarf, beanie\n"
                else:
                    base_response += "• Versatile layers for temperature changes\n"
                    base_response += "• Mix of short and long-sleeve items\n"
                    base_response += "• Comfortable walking shoes\n"
                    base_response += "• Light jacket for evenings\n"
                
                if "rain" in description.lower() or humidity != "N/A" and int(humidity) > 80:
                    base_response += "• Waterproof jacket and umbrella\n"
                    base_response += "• Quick-dry clothing materials"
        
        elif intent == "event_planning":
            base_response = f"Event weather considerations for {city}: "
            base_response += f"Temperature: {temp}{temp_unit}, conditions: {description}. "
            
            if "rain" in description.lower():
                base_response += "⚠️ Rain expected - consider indoor backup plans, provide umbrellas for guests."
            elif temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 20
                if temp_val > 30:
                    base_response += "🌡️ Hot weather - ensure shade, hydration stations, and cooling options for guests."
                elif temp_val < 10:
                    base_response += "❄️ Cold weather - consider heating, warm beverages, and indoor alternatives."
                else:
                    base_response += "✅ Pleasant conditions for outdoor events."
        
        elif intent == "work_attire":
            base_response = f"Professional attire for {city} weather: "
            if temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 20
                
                if temp_val > 25:
                    base_response += "Light business attire - breathable fabrics, lighter colors, minimal layers."
                elif temp_val < 15:
                    base_response += "Professional layers - suit with warm underlayers, dress coat, closed shoes."
                else:
                    base_response += "Standard business attire - suit or professional dress with optional light jacket."
                
                if "rain" in description.lower():
                    base_response += " Bring umbrella and waterproof coat to protect professional appearance."
        
        elif intent == "temperature_check":
            if temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 20
                base_response = f"Temperature in {city}: {temp}{temp_unit}. "
                
                if temp_val > 35:
                    base_response += "🔥 Very hot - heat warning in effect. Stay indoors during peak hours, stay hydrated."
                elif temp_val > 30:
                    base_response += "🌡️ Hot weather - limit outdoor activities, drink plenty of water."
                elif temp_val > 25:
                    base_response += "☀️ Warm and pleasant - good weather for most activities."
                elif temp_val > 15:
                    base_response += "🌤️ Mild temperature - comfortable for outdoor activities."
                elif temp_val > 5:
                    base_response += "🧥 Cool weather - light jacket recommended."
                else:
                    base_response += "❄️ Cold conditions - dress warmly, limit exposure time."
        
        elif intent == "cold_check":
            if temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 20
                if temp_val < 10:
                    base_response = f"Yes, it's cold in {city} at {temp}{temp_unit}. Dress warmly with layers."
                else:
                    base_response = f"No, it's not particularly cold in {city} at {temp}{temp_unit}. Mild conditions."
        
        elif intent == "humidity_check":
            if humidity != "N/A":
                humidity_val = int(humidity)
                base_response = f"Humidity in {city}: {humidity}%. "
                
                if humidity_val > 80:
                    base_response += "Very humid - expect muggy conditions, slower cooling, increased discomfort."
                elif humidity_val > 60:
                    base_response += "High humidity - may feel warmer than actual temperature."
                elif humidity_val < 30:
                    base_response += "Low humidity - dry conditions, stay hydrated, consider moisturizing."
                else:
                    base_response += "Comfortable humidity levels."
        
        # Handle specific weather condition queries
        elif intent == "rain_check":
            if "rain" in description.lower() or "drizzle" in description.lower() or "shower" in description.lower():
                base_response = f"Yes, it is raining in {city}. Current conditions: {description}."
                if humidity != "N/A" and int(humidity) > 80:
                    base_response += f" High humidity ({humidity}%) indicates wet conditions."
            else:
                base_response = f"No, it is not currently raining in {city}. Current conditions: {description}."
                if humidity != "N/A" and int(humidity) > 90:
                    base_response += f" However, very high humidity ({humidity}%) - rain may be likely soon."
        
        elif intent == "sun_check":
            if "clear" in description.lower() or "sunny" in description.lower():
                base_response = f"Yes, it is sunny in {city}. Current conditions: {description}."
            else:
                base_response = f"No, it is not sunny in {city}. Current conditions: {description}."
        
        elif intent == "cloud_check":
            if "cloud" in description.lower() or "overcast" in description.lower():
                base_response = f"Yes, it is cloudy in {city}. Current conditions: {description}."
            else:
                base_response = f"No, it is not particularly cloudy in {city}. Current conditions: {description}."
        
        elif intent == "wind_check":
            if wind_speed != "N/A":
                wind_val = float(wind_speed) if isinstance(wind_speed, (int, float, str)) and str(wind_speed).replace('.', '').isdigit() else 0
                if wind_val > 10:
                    base_response = f"Yes, it is windy in {city}. Wind speed: {wind_speed} m/s."
                elif wind_val > 5:
                    base_response = f"There is a moderate breeze in {city}. Wind speed: {wind_speed} m/s."
                else:
                    base_response = f"No, it is not particularly windy in {city}. Wind speed: {wind_speed} m/s."
            else:
                base_response = f"Wind information not available for {city}. Current conditions: {description}."
        
        elif intent == "snow_check":
            if "snow" in description.lower():
                base_response = f"Yes, it is snowing in {city}. Current conditions: {description}."
            else:
                base_response = f"No, it is not snowing in {city}. Current conditions: {description}."
        
        # Handle specific sport/activity queries
        elif intent == "cricket":
            base_response = f"Cricket conditions in {city}: "
            if "rain" in description.lower() or "drizzle" in description.lower():
                base_response += "❌ Not suitable for cricket - rain/wet conditions. Wait for clear weather."
            elif "storm" in description.lower() or "thunder" in description.lower():
                base_response += "❌ Dangerous for cricket - thunderstorm conditions. Stay indoors."
            elif wind_speed != "N/A" and float(wind_speed) > 15:
                base_response += f"⚠️ Challenging for cricket - strong winds ({wind_speed} m/s) will affect ball movement."
            elif temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 25
                if temp_val > 35:
                    base_response += f"⚠️ Very hot ({temp}{temp_unit}) - take frequent breaks, stay hydrated. Early morning/evening recommended."
                elif temp_val < 10:
                    base_response += f"⚠️ Cold ({temp}{temp_unit}) - dress warmly, may affect performance."
                else:
                    base_response += f"✅ Good for cricket! Temperature: {temp}{temp_unit}, conditions: {description}."
                    if humidity != "N/A" and int(humidity) > 80:
                        base_response += " High humidity - stay hydrated."
        
        elif intent == "football":
            base_response = f"Football conditions in {city}: "
            if "rain" in description.lower():
                base_response += "⚠️ Wet conditions - slippery field, be careful with tackles and turns."
            elif "storm" in description.lower():
                base_response += "❌ Not safe for football - thunderstorm conditions."
            elif temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 25
                if temp_val > 32:
                    base_response += f"⚠️ Hot ({temp}{temp_unit}) - take water breaks every 15-20 minutes."
                elif temp_val < 5:
                    base_response += f"⚠️ Very cold ({temp}{temp_unit}) - warm up thoroughly, risk of injury."
                else:
                    base_response += f"✅ Good for football! Temperature: {temp}{temp_unit}, conditions: {description}."
        
        elif intent == "tennis":
            base_response = f"Tennis conditions in {city}: "
            if "rain" in description.lower():
                base_response += "❌ Not suitable for tennis - wet courts are dangerous."
            elif wind_speed != "N/A" and float(wind_speed) > 12:
                base_response += f"⚠️ Windy ({wind_speed} m/s) - will significantly affect ball trajectory."
            elif temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 25
                if temp_val > 30:
                    base_response += f"⚠️ Hot ({temp}{temp_unit}) - stay hydrated, consider indoor courts."
                else:
                    base_response += f"✅ Good for tennis! Temperature: {temp}{temp_unit}, conditions: {description}."
        
        elif intent == "running":
            base_response = f"Running conditions in {city}: "
            if "rain" in description.lower():
                base_response += "⚠️ Wet conditions - be careful of slippery surfaces, consider indoor alternatives."
            elif temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 25
                if temp_val > 30:
                    base_response += f"⚠️ Hot ({temp}{temp_unit}) - run early morning/evening, stay hydrated."
                elif temp_val < 0:
                    base_response += f"⚠️ Freezing ({temp}{temp_unit}) - dress in layers, warm up indoors first."
                else:
                    base_response += f"✅ Good for running! Temperature: {temp}{temp_unit}, conditions: {description}."
                    if humidity != "N/A" and int(humidity) > 85:
                        base_response += " High humidity - pace yourself."
        
        elif intent == "cycling":
            base_response = f"Cycling conditions in {city}: "
            if "rain" in description.lower():
                base_response += "❌ Not safe for cycling - wet roads increase accident risk."
            elif wind_speed != "N/A" and float(wind_speed) > 20:
                base_response += f"⚠️ Very windy ({wind_speed} m/s) - challenging headwinds, be careful."
            elif temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 25
                if temp_val > 35:
                    base_response += f"⚠️ Very hot ({temp}{temp_unit}) - early morning rides recommended."
                else:
                    base_response += f"✅ Good for cycling! Temperature: {temp}{temp_unit}, conditions: {description}."
        
        elif intent == "swimming":
            base_response = f"Swimming conditions in {city}: "
            if "storm" in description.lower() or "thunder" in description.lower():
                base_response += "❌ Dangerous for outdoor swimming - thunderstorm risk."
            elif temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 25
                if temp_val < 20:
                    base_response += f"⚠️ Cool ({temp}{temp_unit}) - indoor pool recommended."
                else:
                    base_response += f"✅ Good for swimming! Temperature: {temp}{temp_unit}, conditions: {description}."
        
        elif intent == "hiking":
            base_response = f"Hiking conditions in {city}: "
            if "rain" in description.lower() or "storm" in description.lower():
                base_response += "❌ Not safe for hiking - slippery trails and poor visibility."
            elif temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 25
                if temp_val > 35:
                    base_response += f"⚠️ Very hot ({temp}{temp_unit}) - start early, carry extra water."
                elif temp_val < 5:
                    base_response += f"⚠️ Cold ({temp}{temp_unit}) - dress warmly, check trail conditions."
                else:
                    base_response += f"✅ Good for hiking! Temperature: {temp}{temp_unit}, conditions: {description}."
        
        elif intent == "activities":
            if "rain" in description.lower() or "storm" in description.lower():
                base_response += " Indoor activities recommended due to weather conditions."
            else:
                base_response += " Good conditions for outdoor activities."
        
        elif intent == "health":
            if temp != "N/A":
                temp_val = float(temp) if isinstance(temp, (int, float, str)) and str(temp).replace('.', '').isdigit() else 15
                if temp_val > 30:
                    base_response += " Stay hydrated and avoid prolonged sun exposure."
                elif temp_val < 5:
                    base_response += " Dress warmly to prevent cold-related health issues."
                else:
                    base_response += " Comfortable conditions, stay hydrated."
        
        return base_response