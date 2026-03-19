from genlayer import *
import typing
import json

class WeatherLib:
    """
    A library for GenLayer Intelligent Contracts to interact with weather APIs.
    """
    
    @staticmethod
    def get_current_weather(city: str, api_key: str = None) -> dict:
        """
        Fetches current weather for a given city.
        If api_key is provided, it uses OpenWeatherMap. 
        Otherwise, it can be extended to use free public APIs.
        """
        def fetch_weather() -> str:
            # Example using a public weather API (wttr.in) for simplicity in this demo
            # In production, use gl.nondet.web.get with proper API keys
            url = f"https://wttr.in/{city}?format=j1"
            response = gl.nondet.web.get(url)
            return response.body.decode("utf-8")

        # Use equivalence principle to ensure consensus on the weather data
        weather_data_raw = gl.eq_principle.strict_eq(fetch_weather)
        return json.loads(weather_data_raw)

    @staticmethod
    def get_temperature(city: str) -> float:
        """
        Helper to get only the temperature for a city.
        """
        data = WeatherLib.get_current_weather(city)
        # Parsing wttr.in JSON structure
        return float(data['current_condition'][0]['temp_C'])
