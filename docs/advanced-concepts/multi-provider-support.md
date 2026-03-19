# Multi-Provider Support in Intelligent Contracts

To enhance the reliability and resilience of Intelligent Contracts, especially when relying on external data, implementing multi-provider support is a crucial strategy. This approach involves integrating with several independent data sources for the same type of information, allowing for fallback mechanisms and data verification.

## Why Multi-Provider Support?

External APIs can be prone to various issues, including:

-   **Downtime**: A single provider might experience outages, making your contract unable to fetch critical data.
-   **Rate Limiting**: APIs often impose limits on the number of requests, which can be a bottleneck for high-volume contracts.
-   **Data Inconsistency**: Different providers might offer slightly different data, or one might be compromised.
-   **Censorship/Bias**: Relying on a single source can introduce a single point of failure for censorship or biased data.

By integrating with multiple providers, Intelligent Contracts can mitigate these risks, leading to more robust and trustworthy applications.

## Implementation Strategy

The `WeatherLib` in this repository serves as a prime example of implementing multi-provider support. The general strategy involves:

1.  **Define Primary and Secondary Providers**: Identify a primary data source and one or more secondary (fallback) sources.
2.  **Encapsulate Provider-Specific Logic**: Create private helper methods (e.g., `_fetch_from_openweathermap`, `_fetch_from_wttr_in`) within your library to handle the unique API calls, request parameters, and response parsing for each provider.
3.  **Implement Fallback Logic**: In the main public method (e.g., `get_current_weather`), attempt to fetch data from the primary provider first. If it fails (returns `None` or raises an exception), then proceed to try the secondary provider(s).
4.  **Consensus with Equivalence Principle**: Crucially, each individual fetch operation from an external API must still be wrapped with `gl.eq_principle.strict_eq`. This ensures that even when trying multiple providers, all validators agree on *which* provider was successfully used and *what data* was returned by that provider.

### Example from `WeatherLib`

```python
# Simplified for illustration
class WeatherLib:
    # ... (private fetch methods for OpenWeatherMap and wttr.in)

    @staticmethod
    def get_current_weather(city: str, openweathermap_api_key: typing.Optional[str] = None) -> typing.Optional[dict]:
        weather_data = None

        # Try primary provider (OpenWeatherMap) if API key is available
        if openweathermap_api_key:
            weather_data = gl.eq_principle.strict_eq(lambda: WeatherLib._fetch_from_openweathermap(city, openweathermap_api_key))
            if weather_data:
                return weather_data
            print(f"Failed to get weather from OpenWeatherMap for {city}, trying wttr.in...")
        
        # Fallback to secondary provider (wttr.in)
        weather_data = gl.eq_principle.strict_eq(lambda: WeatherLib._fetch_from_wttr_in(city))
        
        if not weather_data:
            print(f"Could not retrieve weather data for {city} from any provider.")
            return None
        
        return weather_data
```

## Considerations for Multi-Provider Implementations

-   **API Key Management**: If multiple providers require API keys, ensure each key is securely managed using the `SecureAPIKeyManager` and retrieved appropriately.
-   **Data Format Consistency**: Be prepared to normalize data formats from different providers. Even if they provide similar information (e.g., temperature), the JSON structure or field names might differ.
-   **Cost**: Some premium APIs charge per request. Using multiple providers might increase operational costs.
-   **Latency**: Attempting multiple API calls sequentially can increase the overall latency of your contract's execution. Consider if parallel fetching (if supported by GenLayer's non-deterministic operations) or a more sophisticated oracle solution is necessary for high-performance scenarios.
-   **Consensus Logic**: While `strict_eq` is suitable for ensuring all validators agree on *one* successful fetch, for scenarios where you need to compare data from *multiple* providers (e.g., taking an average or verifying against a threshold), you might need to implement more complex equivalence principles or use an off-chain oracle that performs this aggregation.

By thoughtfully implementing multi-provider support, Intelligent Contracts can achieve a higher degree of fault tolerance and data reliability, making them more suitable for critical decentralized applications.
