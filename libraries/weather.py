from genlayer import *
import typing
import json

class WeatherLib:
    """
    A library for GenLayer Intelligent Contracts to interact with various weather APIs.
    Supports OpenWeatherMap and wttr.in, with a focus on robust error handling.
    """
    
    @staticmethod
    def _fetch_from_openweathermap(city: str, api_key: str) -> typing.Optional[dict]:
        """
        Fetches weather data from OpenWeatherMap.
        """
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = gl.nondet.web.get(url)
            if response.status_code == 200:
                return json.loads(response.body.decode("utf-8"))
            else:
                print(f"OpenWeatherMap API error for {city}: {response.status_code} - {response.body.decode('utf-8')}")
                return None
        except Exception as e:
            print(f"Error fetching from OpenWeatherMap for {city}: {e}")
            return None

    @staticmethod
    def _fetch_from_wttr_in(city: str) -> typing.Optional[dict]:
        """
        Fetches weather data from wttr.in (public API).
        """
        try:
            url = f"https://wttr.in/{city}?format=j1"
            response = gl.nondet.web.get(url)
            if response.status_code == 200:
                return json.loads(response.body.decode("utf-8"))
            else:
                print(f"wttr.in API error for {city}: {response.status_code} - {response.body.decode('utf-8')}")
                return None
        except Exception as e:
            print(f"Error fetching from wttr.in for {city}: {e}")
            return None

    @staticmethod
    def get_current_weather(city: str, openweathermap_api_key: typing.Optional[str] = None) -> typing.Optional[dict]:
        """
        Fetches current weather for a given city using multiple providers.
        Prioritizes OpenWeatherMap if an API key is provided, falls back to wttr.in.
        """
        weather_data = None

        if openweathermap_api_key:
            weather_data = gl.eq_principle.strict_eq(lambda: WeatherLib._fetch_from_openweathermap(city, openweathermap_api_key))
            if weather_data:
                return weather_data
            print(f"Failed to get weather from OpenWeatherMap for {city}, trying wttr.in...")
        
        # Fallback to wttr.in
        weather_data = gl.eq_principle.strict_eq(lambda: WeatherLib._fetch_from_wttr_in(city))
        
        if not weather_data:
            print(f"Could not retrieve weather data for {city} from any provider.")
            return None
        
        return weather_data

    @staticmethod
    def get_temperature(city: str, openweathermap_api_key: typing.Optional[str] = None) -> typing.Optional[float]:
        """
        Helper to get only the temperature for a city.
        """
        data = WeatherLib.get_current_weather(city, openweathermap_api_key)
        if data:
            # Try parsing OpenWeatherMap format first
            if 'main' in data and 'temp' in data['main']:
                return float(data['main']['temp'])
            # Fallback to wttr.in format
            elif 'current_condition' in data and len(data['current_condition']) > 0 and 'temp_C' in data['current_condition'][0]:
                return float(data['current_condition'][0]['temp_C'])
        return None
