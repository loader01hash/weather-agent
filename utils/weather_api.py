"""Weather API integration using OpenWeatherMap."""

import requests
from typing import Dict, Any, Optional


class WeatherAPI:
    """Handles weather data retrieval from OpenWeatherMap API."""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key: str):
        """Initialize with API key."""
        self.api_key = api_key
    
    def get_weather(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Get current weather for a city.
        
        Args:
            city: City name
            units: Temperature units (metric/imperial)
            
        Returns:
            Weather data dictionary
            
        Raises:
            Exception: If API request fails
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract relevant information
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "description": data["weather"][0]["description"],
                "main": data["weather"][0]["main"],
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"].get("deg", 0),
                "clouds": data["clouds"]["all"],
                "units": units
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch weather data: {str(e)}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: {str(e)}")
    
    def format_weather_data(self, weather_data: Dict[str, Any]) -> str:
        """
        Format weather data into a readable string.
        
        Args:
            weather_data: Weather data dictionary
            
        Returns:
            Formatted weather string
        """
        units = weather_data.get("units", "metric")
        temp_unit = "°C" if units == "metric" else "°F"
        speed_unit = "m/s" if units == "metric" else "mph"
        
        return (
            f"Weather in {weather_data['city']}, {weather_data['country']}:\n"
            f"Temperature: {weather_data['temperature']}{temp_unit} "
            f"(feels like {weather_data['feels_like']}{temp_unit})\n"
            f"Conditions: {weather_data['description'].capitalize()}\n"
            f"Humidity: {weather_data['humidity']}%\n"
            f"Wind: {weather_data['wind_speed']} {speed_unit}\n"
            f"Cloud coverage: {weather_data['clouds']}%"
        )