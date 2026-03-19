# Weather API Integration

## Overview

The `WeatherLib` provides a convenient and robust way for GenLayer Intelligent Contracts to fetch real-time weather data. It supports multiple weather data providers, including OpenWeatherMap (requiring an API key) and wttr.in (a public, free service), with built-in fallback mechanisms and error handling. This ensures that your Intelligent Contracts can reliably access weather information for dynamic decision-making.

## Features

- **Multi-Provider Support**: Seamlessly integrates with OpenWeatherMap and wttr.in.
- **Fallback Mechanism**: Automatically attempts to fetch data from a secondary provider if the primary fails.
- **Error Handling**: Includes robust error handling to manage API failures and network issues gracefully.
- **Equivalence Principle Integration**: Utilizes `gl.eq_principle.strict_eq` to ensure all validators agree on the fetched weather data, maintaining the integrity of your contract.

## Usage

To use the `WeatherLib` in your Intelligent Contract, import it and call its static methods. Remember to include the `py-genlayer` dependency in your contract declaration.

### Example: Fetching Current Temperature

This example demonstrates how to fetch the current temperature for a specified city. If an OpenWeatherMap API key is provided, it will be used; otherwise, the library will attempt to use wttr.in.

```python
# { "Depends": "py-genlayer:YOUR_GENLAYER_SDK_VERSION" }
from genlayer import *
from libraries.weather import WeatherLib
from services.studio_ux_utils import StudioUXUtils # For logging and UX improvements

class MyWeatherContract(gl.Contract):
    current_city: str
    current_temperature: typing.Optional[float]
    last_updated: int

    def __init__(self):
        self.current_city = ""
        self.current_temperature = None
        self.last_updated = 0

    @gl.public.write
    def update_weather_for_city(self, city: str, openweathermap_api_key: typing.Optional[str] = None):
        """
        Fetches the current weather for a given city and updates the contract state.
        Optionally accepts an OpenWeatherMap API key.
        """
        try:
            # Fetch weather data using WeatherLib
            temperature = WeatherLib.get_temperature(city, openweathermap_api_key)
            
            if temperature is not None:
                self.current_city = city
                self.current_temperature = temperature
                self.last_updated = gl.timestamp()
                StudioUXUtils.log_event("WeatherUpdateSuccess", {
                    "city": city,
                    "temperature": temperature,
                    "timestamp": self.last_updated
                })
            else:
                StudioUXUtils.log_event("WeatherUpdateFailed", {"city": city, "reason": "Could not retrieve temperature"})
                # Optionally, revert the transaction or take other corrective actions
                raise Exception(f"Failed to retrieve weather for {city}")

        except Exception as e:
            StudioUXUtils.log_event("WeatherUpdateError", {"city": city, "error": str(e)})
            raise # Re-raise the exception to indicate contract failure

    @gl.public.view
    def get_last_known_temperature(self) -> typing.Optional[float]:
        """
        Returns the last successfully fetched temperature.
        """
        return self.current_temperature

    @gl.public.view
    def get_last_updated_city(self) -> str:
        """
        Returns the city for which weather was last updated.
        """
        return self.current_city

    @gl.public.view
    def get_last_updated_timestamp(self) -> int:
        """
        Returns the timestamp of the last weather update.
        """
        return self.last_updated
```

## Error Handling and Robustness

The `WeatherLib` is designed with robustness in mind:

- **API Call Failures**: If an API call fails (e.g., network error, invalid API key, rate limiting), the internal `_fetch_from_openweathermap` or `_fetch_from_wttr_in` methods will return `None` and print an error message to the console (visible in GenLayer Studio logs).
- **Fallback Logic**: The `get_current_weather` method attempts to use OpenWeatherMap first. If it fails or no API key is provided, it falls back to wttr.in. This increases the reliability of data retrieval.
- **Contract-Level Handling**: In your Intelligent Contract, it's crucial to check if the returned temperature is `None`. You can then decide whether to revert the transaction, log the error, or use a default value.

## Security Considerations

- **API Key Management**: For OpenWeatherMap, an API key is required. **Never hardcode API keys directly into your Intelligent Contracts.** Instead, use the `SecureAPIKeyManager` service (documented [here](#secure-api-key-management)) to store and retrieve encrypted API keys securely. The API key should be passed to the `update_weather_for_city` method at runtime, ideally retrieved from a trusted proxy or oracle service.
- **Data Integrity**: The use of `gl.eq_principle.strict_eq` is vital. It ensures that all validators process the same web request and agree on the exact data returned, preventing discrepancies and maintaining the integrity of your contract's state.
- **Trusted Sources**: While wttr.in is convenient for public data, for critical applications, always prefer well-established and reliable weather data providers. Consider implementing additional data validation checks within your contract if the data source is less trusted.

## Extending Functionality

You can easily extend `WeatherLib` to support more weather providers or specific weather parameters (e.g., humidity, wind speed) by adding new internal `_fetch_from_...` methods and integrating them into the `get_current_weather` logic. Remember to maintain the use of `gl.eq_principle.strict_eq` for all external data fetches.
