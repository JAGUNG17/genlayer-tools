# GenLayer Tools & Infrastructure

This repository provides a collection of simple and informative libraries and services for **GenLayer Intelligent Contracts**. These tools are designed to help developers interact with external APIs, manage API keys securely, and improve the overall development experience (Studio and UX).

## 🚀 Features

- **External API Libraries**: Easy-to-use Python libraries for interacting with:
  - 🌦️ **Weather APIs**: Fetch real-time weather data for any city.
  - 📈 **Price Feeds**: Get the latest cryptocurrency and stock prices.
  - 📱 **Social Media**: Retrieve GitHub profiles and Twitter metrics.
- **Secure API Key Management**: A dedicated service to store and manage encrypted API keys, keeping them private while maintaining security.
- **Studio & UX Utilities**: Helper functions to format JSON output, log events, and validate inputs for a better developer experience in the GenLayer Studio.

## 📂 Project Structure

```text
genlayer-tools/
├── libraries/
│   ├── weather.py         # Weather API integration
│   ├── price_feed.py      # Crypto and stock price feeds
│   └── social_media.py    # GitHub and Twitter integration
├── services/
│   ├── secure_api_key_manager.py  # Secure API key storage contract
│   └── studio_ux_utils.py         # Studio and UX helper utilities
└── README.md              # Project documentation
```

## 🛠️ Getting Started

### Prerequisites

- A GenLayer development environment.
- Basic knowledge of Python and Intelligent Contracts.

### Using the Libraries

To use the libraries in your Intelligent Contract, simply import the desired class:

```python
from genlayer import *
from libraries.weather import WeatherLib

class MyWeatherContract(gl.Contract):
    @gl.public.write
    def update_weather(self, city: str):
        temp = WeatherLib.get_temperature(city)
        # Use the temperature in your contract logic
```

### Secure API Key Management

Deploy the `SecureAPIKeyManager` contract to store your encrypted API keys:

```python
from services.secure_api_key_manager import SecureAPIKeyManager

# Deploy and use the set_api_key method to store your keys
```

## 🌟 Improving Studio & UX

Use the `StudioUXUtils` to enhance your development workflow:

```python
from services.studio_ux_utils import StudioUXUtils

# Format JSON for better readability in the Studio
formatted_data = StudioUXUtils.format_json_output(my_data)
```

## 📄 License

This project is licensed under the MIT License.

---

*Built with ❤️ for the GenLayer community.*
