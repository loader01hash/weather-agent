"""Insight Engine for generating weather-based recommendations and insights."""

from typing import Dict, Any, List
from utils.message import InsightResult


class InsightEngine:
    """
    Analyzes weather data and generates contextual insights and recommendations.
    Provides intelligent analysis for comfort, activities, health, and safety.
    """
    
    def __init__(self):
        """Initialize the Insight Engine."""
        self.name = "Insight Engine"
        print(f"[{self.name}] Initialized and ready to generate insights")
    
    def generate_comfort_insights(self, weather_data: Dict[str, Any]) -> InsightResult:
        """
        Analyze weather conditions and generate comfort level insights.
        
        Args:
            weather_data: Weather information dictionary
            
        Returns:
            InsightResult with comfort analysis and recommendations
        """
        temperature = weather_data.get("temperature", 0)
        humidity = weather_data.get("humidity", 0)
        wind_speed = weather_data.get("wind_speed", 0)
        units = weather_data.get("units", "metric")
        
        # Convert temperature to Celsius for consistent analysis
        temp_c = temperature if units == "metric" else (temperature - 32) * 5/9
        
        insights = []
        recommendations = []
        priority = 1
        
        # Temperature comfort analysis
        if temp_c < 0:
            insights.append("Freezing conditions detected")
            recommendations.append("Dress in multiple layers and limit outdoor exposure")
            priority = 5
        elif temp_c < 10:
            insights.append("Cold weather conditions")
            recommendations.append("Wear warm clothing and consider indoor activities")
            priority = 4
        elif temp_c < 18:
            insights.append("Cool and comfortable for light activities")
            recommendations.append("Light jacket recommended for outdoor activities")
            priority = 2
        elif temp_c <= 25:
            insights.append("Ideal temperature conditions")
            recommendations.append("Perfect weather for most outdoor activities")
            priority = 1
        elif temp_c <= 30:
            insights.append("Warm and pleasant conditions")
            recommendations.append("Stay hydrated and seek shade during peak hours")
            priority = 2
        elif temp_c <= 35:
            insights.append("Hot weather conditions")
            recommendations.append("Limit outdoor activities and stay well-hydrated")
            priority = 4
        else:
            insights.append("Extreme heat detected")
            recommendations.append("Avoid outdoor activities and stay in air-conditioned spaces")
            priority = 5
        
        # Humidity analysis
        if humidity > 80:
            insights.append("Very high humidity levels")
            recommendations.append("Expect reduced comfort and slower cooling")
            priority = max(priority, 3)
        elif humidity > 60:
            insights.append("High humidity conditions")
            recommendations.append("May feel warmer than actual temperature")
            priority = max(priority, 2)
        elif humidity < 30:
            insights.append("Low humidity conditions")
            recommendations.append("Stay hydrated and consider moisturizing")
            priority = max(priority, 2)
        
        # Wind analysis
        if wind_speed > 15:  # Assuming m/s for metric, mph for imperial
            wind_unit = "m/s" if units == "metric" else "mph"
            insights.append(f"Strong winds at {wind_speed} {wind_unit}")
            recommendations.append("Secure loose items and be cautious outdoors")
            priority = max(priority, 3)
        elif wind_speed > 8:
            insights.append("Moderate wind conditions")
            recommendations.append("Pleasant breeze for outdoor activities")
        
        return InsightResult(
            category="comfort",
            insights=insights,
            recommendations=recommendations,
            priority=priority,
            confidence=0.9
        )
    
    def identify_weather_patterns(self, weather_data: Dict[str, Any]) -> InsightResult:
        """
        Identify notable weather patterns and conditions.
        
        Args:
            weather_data: Weather information dictionary
            
        Returns:
            InsightResult with pattern analysis
        """
        description = weather_data.get("description", "").lower()
        main_condition = weather_data.get("main", "").lower()
        clouds = weather_data.get("clouds", 0)
        pressure = weather_data.get("pressure", 1013)
        
        insights = []
        recommendations = []
        priority = 1
        
        # Weather condition analysis
        if "storm" in description or "thunder" in description:
            insights.append("Thunderstorm activity detected")
            recommendations.append("Stay indoors and avoid outdoor activities")
            priority = 5
        elif "rain" in description or "drizzle" in description:
            insights.append("Precipitation expected")
            recommendations.append("Carry an umbrella and wear waterproof clothing")
            priority = 3
        elif "snow" in description:
            insights.append("Snow conditions present")
            recommendations.append("Drive carefully and dress warmly")
            priority = 4
        elif "fog" in description or "mist" in description:
            insights.append("Reduced visibility conditions")
            recommendations.append("Exercise caution when driving or walking")
            priority = 3
        
        # Cloud cover analysis
        if clouds > 80:
            insights.append("Overcast skies")
            recommendations.append("Limited sun exposure, good for outdoor activities")
        elif clouds < 20:
            insights.append("Clear skies")
            recommendations.append("Excellent visibility, apply sun protection")
        
        # Pressure analysis
        if pressure < 1000:
            insights.append("Low atmospheric pressure")
            recommendations.append("Weather changes possible, monitor conditions")
            priority = max(priority, 2)
        elif pressure > 1025:
            insights.append("High atmospheric pressure")
            recommendations.append("Stable weather conditions expected")
        
        return InsightResult(
            category="patterns",
            insights=insights,
            recommendations=recommendations,
            priority=priority,
            confidence=0.8
        )
    
    def suggest_activities(self, weather_data: Dict[str, Any]) -> InsightResult:
        """
        Suggest appropriate activities based on current weather conditions.
        
        Args:
            weather_data: Weather information dictionary
            
        Returns:
            InsightResult with activity suggestions
        """
        temperature = weather_data.get("temperature", 0)
        humidity = weather_data.get("humidity", 0)
        wind_speed = weather_data.get("wind_speed", 0)
        description = weather_data.get("description", "").lower()
        clouds = weather_data.get("clouds", 0)
        units = weather_data.get("units", "metric")
        
        # Convert temperature to Celsius for consistent analysis
        temp_c = temperature if units == "metric" else (temperature - 32) * 5/9
        
        insights = []
        recommendations = []
        priority = 2
        
        # Check for adverse conditions first
        if "storm" in description or "thunder" in description:
            insights.append("Severe weather conditions")
            recommendations.extend([
                "Stay indoors and avoid outdoor activities",
                "Good time for indoor hobbies, reading, or movies",
                "Consider indoor exercise or yoga"
            ])
            priority = 5
        elif "rain" in description or "drizzle" in description:
            insights.append("Wet weather conditions")
            recommendations.extend([
                "Indoor activities recommended",
                "Visit museums, shopping centers, or cafes",
                "Good time for indoor sports or gym activities"
            ])
            priority = 3
        elif "snow" in description:
            insights.append("Snowy conditions")
            recommendations.extend([
                "Winter sports opportunities available",
                "Skiing, snowboarding, or snowshoeing",
                "Build snowmen or have snowball fights"
            ])
            priority = 3
        else:
            # Good weather activity suggestions
            if 15 <= temp_c <= 25 and humidity < 70:
                insights.append("Ideal conditions for outdoor activities")
                recommendations.extend([
                    "Perfect for hiking, cycling, or jogging",
                    "Great weather for picnics or outdoor sports",
                    "Excellent time for photography or sightseeing"
                ])
                priority = 1
            elif temp_c > 25:
                if temp_c > 30:
                    insights.append("Hot weather - limited outdoor activities")
                    recommendations.extend([
                        "Early morning or evening outdoor activities",
                        "Swimming or water sports recommended",
                        "Indoor activities during peak heat hours"
                    ])
                    priority = 3
                else:
                    insights.append("Warm weather - great for water activities")
                    recommendations.extend([
                        "Swimming, beach activities, or water sports",
                        "Outdoor dining in shaded areas",
                        "Light outdoor activities with sun protection"
                    ])
                    priority = 2
            elif temp_c < 10:
                insights.append("Cold weather activities")
                recommendations.extend([
                    "Brisk walks or winter hiking with proper clothing",
                    "Indoor activities like museums or shopping",
                    "Cozy indoor activities like cooking or crafts"
                ])
                priority = 3
            else:
                insights.append("Moderate weather conditions")
                recommendations.extend([
                    "Light jacket recommended for outdoor activities",
                    "Walking, light jogging, or outdoor exploration",
                    "Good weather for most outdoor activities"
                ])
                priority = 2
        
        # Wind considerations
        if wind_speed > 15:
            insights.append("Strong winds affect outdoor activities")
            recommendations.append("Avoid activities involving loose objects or high structures")
            priority = max(priority, 3)
        elif 5 <= wind_speed <= 15:
            insights.append("Good breeze for wind-based activities")
            recommendations.append("Great conditions for kite flying or sailing")
        
        # Cloud cover considerations
        if clouds < 30:
            insights.append("Clear skies with good visibility")
            recommendations.append("Excellent for photography and sightseeing")
        elif clouds > 80:
            insights.append("Overcast conditions")
            recommendations.append("Reduced UV exposure - good for extended outdoor time")
        
        return InsightResult(
            category="activities",
            insights=insights,
            recommendations=recommendations,
            priority=priority,
            confidence=0.85
        )
    
    def analyze_health_factors(self, weather_data: Dict[str, Any]) -> InsightResult:
        """
        Analyze weather conditions for health-related considerations.
        
        Args:
            weather_data: Weather information dictionary
            
        Returns:
            InsightResult with health analysis and recommendations
        """
        temperature = weather_data.get("temperature", 0)
        humidity = weather_data.get("humidity", 0)
        description = weather_data.get("description", "").lower()
        units = weather_data.get("units", "metric")
        
        # Convert temperature to Celsius for consistent analysis
        temp_c = temperature if units == "metric" else (temperature - 32) * 5/9
        
        insights = []
        recommendations = []
        priority = 2
        
        # Temperature-related health considerations
        if temp_c > 35:
            insights.append("Extreme heat poses health risks")
            recommendations.extend([
                "Risk of heat exhaustion and dehydration",
                "Stay in air-conditioned spaces",
                "Drink water frequently, avoid alcohol and caffeine",
                "Seek immediate medical attention if feeling dizzy or nauseous"
            ])
            priority = 5
        elif temp_c > 30:
            insights.append("High temperature requires precautions")
            recommendations.extend([
                "Increased risk of dehydration",
                "Drink plenty of water throughout the day",
                "Limit strenuous outdoor activities",
                "Wear light-colored, loose-fitting clothing"
            ])
            priority = 4
        elif temp_c < -10:
            insights.append("Extreme cold poses health risks")
            recommendations.extend([
                "Risk of frostbite and hypothermia",
                "Limit outdoor exposure time",
                "Cover all exposed skin",
                "Watch for signs of cold-related illness"
            ])
            priority = 5
        elif temp_c < 0:
            insights.append("Freezing temperatures require caution")
            recommendations.extend([
                "Protect exposed skin from frostbite",
                "Dress in warm layers",
                "Limit time outdoors"
            ])
            priority = 4
        
        # Humidity-related health considerations
        if humidity > 80:
            insights.append("Very high humidity affects comfort and health")
            recommendations.extend([
                "Body's cooling system less effective",
                "Increased risk of heat-related illness",
                "Stay hydrated and seek air-conditioned spaces",
                "Monitor for signs of heat exhaustion"
            ])
            priority = max(priority, 3)
        elif humidity > 60 and temp_c > 25:
            insights.append("High humidity increases heat stress")
            recommendations.extend([
                "Feels hotter than actual temperature",
                "Take frequent breaks in shade or indoors",
                "Increase fluid intake"
            ])
            priority = max(priority, 3)
        elif humidity < 30:
            insights.append("Low humidity may cause discomfort")
            recommendations.extend([
                "May experience dry skin and respiratory irritation",
                "Use moisturizer and stay hydrated",
                "Consider using a humidifier indoors"
            ])
            priority = max(priority, 2)
        
        # Weather condition health impacts
        if "storm" in description or "thunder" in description:
            insights.append("Severe weather health considerations")
            recommendations.extend([
                "Stay indoors to avoid injury from lightning or debris",
                "Those with weather sensitivity may experience discomfort"
            ])
            priority = max(priority, 4)
        
        # UV and sun exposure (clear conditions)
        if "clear" in description or "sunny" in description:
            insights.append("High UV exposure risk")
            recommendations.extend([
                "Apply broad-spectrum sunscreen (SPF 30+)",
                "Wear sunglasses and protective clothing",
                "Seek shade during peak sun hours (10 AM - 4 PM)"
            ])
            priority = max(priority, 3)
        
        # Air quality considerations (basic inference)
        if "fog" in description or "haze" in description:
            insights.append("Reduced air quality possible")
            recommendations.extend([
                "Those with respiratory conditions should limit outdoor activities",
                "Consider wearing a mask if air quality is poor"
            ])
            priority = max(priority, 3)
        
        return InsightResult(
            category="health",
            insights=insights,
            recommendations=recommendations,
            priority=priority,
            confidence=0.8
        )
    
    def assess_clothing_recommendations(self, weather_data: Dict[str, Any]) -> InsightResult:
        """
        Provide clothing recommendations based on weather conditions.
        
        Args:
            weather_data: Weather information dictionary
            
        Returns:
            InsightResult with clothing suggestions
        """
        temperature = weather_data.get("temperature", 0)
        humidity = weather_data.get("humidity", 0)
        wind_speed = weather_data.get("wind_speed", 0)
        description = weather_data.get("description", "").lower()
        units = weather_data.get("units", "metric")
        
        # Convert temperature to Celsius for consistent analysis
        temp_c = temperature if units == "metric" else (temperature - 32) * 5/9
        
        insights = []
        recommendations = []
        priority = 2
        
        # Base clothing recommendations by temperature
        if temp_c < -10:
            insights.append("Extreme cold clothing required")
            recommendations.extend([
                "Heavy winter coat with insulation",
                "Multiple layers including thermal underwear",
                "Insulated boots, gloves, and hat",
                "Cover all exposed skin"
            ])
            priority = 4
        elif temp_c < 0:
            insights.append("Cold weather clothing needed")
            recommendations.extend([
                "Warm winter coat or heavy jacket",
                "Long pants and warm layers",
                "Winter boots, gloves, and hat",
                "Scarf to protect neck and face"
            ])
            priority = 3
        elif temp_c < 10:
            insights.append("Cool weather clothing appropriate")
            recommendations.extend([
                "Medium jacket or sweater",
                "Long pants recommended",
                "Closed-toe shoes",
                "Light gloves if windy"
            ])
            priority = 2
        elif temp_c < 18:
            insights.append("Mild weather clothing")
            recommendations.extend([
                "Light jacket or cardigan",
                "Long or short pants depending on preference",
                "Comfortable walking shoes"
            ])
            priority = 1
        elif temp_c < 25:
            insights.append("Comfortable weather clothing")
            recommendations.extend([
                "Light clothing - t-shirt or light blouse",
                "Shorts or light pants",
                "Comfortable shoes or sandals"
            ])
            priority = 1
        elif temp_c < 30:
            insights.append("Warm weather clothing")
            recommendations.extend([
                "Light, breathable fabrics",
                "Shorts and t-shirt or tank top",
                "Sandals or breathable shoes",
                "Hat for sun protection"
            ])
            priority = 2
        else:
            insights.append("Hot weather clothing essential")
            recommendations.extend([
                "Minimal, light-colored clothing",
                "Loose-fitting, breathable fabrics",
                "Wide-brimmed hat and sunglasses",
                "Light-colored shoes to reflect heat"
            ])
            priority = 3
        
        # Weather condition adjustments
        if "rain" in description or "drizzle" in description:
            insights.append("Wet weather protection needed")
            recommendations.extend([
                "Waterproof jacket or raincoat",
                "Waterproof shoes or boots",
                "Umbrella recommended"
            ])
            priority = max(priority, 3)
        elif "snow" in description:
            insights.append("Snow protection required")
            recommendations.extend([
                "Waterproof winter boots with good traction",
                "Water-resistant outer layer",
                "Extra warm layers"
            ])
            priority = max(priority, 4)
        
        # Wind adjustments
        if wind_speed > 15:
            insights.append("Windy conditions require adjustments")
            recommendations.extend([
                "Wind-resistant outer layer",
                "Secure hat or avoid loose accessories",
                "Extra layer for wind chill effect"
            ])
            priority = max(priority, 3)
        
        # Humidity adjustments
        if humidity > 70 and temp_c > 20:
            insights.append("High humidity clothing considerations")
            recommendations.extend([
                "Choose moisture-wicking fabrics",
                "Avoid heavy or non-breathable materials",
                "Light colors to reflect heat"
            ])
            priority = max(priority, 2)
        
        return InsightResult(
            category="clothing",
            insights=insights,
            recommendations=recommendations,
            priority=priority,
            confidence=0.9
        )