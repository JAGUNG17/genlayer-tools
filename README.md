# GenLayer Tools & Infrastructure

This repository presents a robust collection of libraries and services meticulously designed to enhance the capabilities and developer experience for **GenLayer Intelligent Contracts**. Our primary objective is to provide a standardized, secure, and efficient framework for integrating external data sources, managing sensitive API keys, and improving the overall usability of the GenLayer Studio environment.

## 🎯 Project Goal

The overarching goal of this project is to empower GenLayer developers with essential tools that facilitate seamless interaction with the broader internet ecosystem. By abstracting complex external API integrations and implementing best practices for security and user experience, we aim to accelerate the development of sophisticated and reliable Intelligent Contracts.

## 🌟 Key Features & Components

This repository is structured into two main categories: **Core Libraries** for external data integration and **Security & Infrastructure Services** for foundational support.

### Core Libraries

These libraries provide pre-built modules for Intelligent Contracts to interact with various external data sources, ensuring data integrity and consensus through GenLayer's equivalence principle.

- **Weather API Integration**: A flexible library to fetch real-time weather data from multiple providers. It demonstrates how to handle external data retrieval and integrate it into contract logic securely.
- **Price Feed Integration**: Modules for accessing up-to-date cryptocurrency and traditional stock market prices. This is crucial for financial Intelligent Contracts requiring accurate and timely market data.
- **Social Media Integration**: Tools to retrieve public data from social platforms like GitHub and Twitter, enabling contracts to react to real-world social events or user activities.

### Security & Infrastructure Services

These services address critical aspects of Intelligent Contract development, focusing on security, maintainability, and developer experience.

- **Secure API Key Management**: A specialized Intelligent Contract designed to securely store and manage sensitive API keys. It employs advanced security patterns to protect credentials while allowing authorized contracts to utilize them for external API calls.
- **Studio & UX Utilities**: A suite of helper functions aimed at improving the GenLayer Studio experience. This includes tools for structured logging, input validation, and enhanced data visualization within the development environment.

## 📂 Repository Structure

```text
genlayer-tools/
├── libraries/                     # Core libraries for external API integrations
│   ├── weather.py                 # Weather data fetching
│   ├── price_feed.py              # Cryptocurrency and stock price feeds
│   └── social_media.py            # GitHub and Twitter data retrieval
├── services/                      # Infrastructure services and utilities
│   ├── secure_api_key_manager.py  # Intelligent Contract for secure API key storage
│   └── studio_ux_utils.py         # Utilities for GenLayer Studio and UX improvements
├── docs/                          # Comprehensive documentation and guides
│   └── SUMMARY.md                 # Table of Contents for documentation
├── .github/                       # GitHub specific configurations (e.g., workflows, issue templates)
├── .gitignore                     # Specifies intentionally untracked files to ignore
└── README.md                      # Project overview and main documentation entry point
```

## 🛠️ Getting Started

To begin developing with these tools, ensure you have a GenLayer development environment set up. The following sections provide detailed guidance on how to integrate and utilize each component.

### Prerequisites

- **GenLayer SDK**: Installed and configured in your development environment.
- **Python 3.x**: Familiarity with Python programming is essential.
- **Basic Understanding of Intelligent Contracts**: Knowledge of GenLayer's core concepts, including the equivalence principle and non-deterministic operations.

### Installation

Clone this repository to your local development machine:

```bash
git clone https://github.com/JAGUNG17/genlayer-tools.git
cd genlayer-tools
```

### Usage Examples

Detailed usage examples for each library and service can be found in their respective documentation files within the `docs/` directory. Below are quick snippets to illustrate basic integration.

#### Integrating a Core Library (e.g., WeatherLib)

```python
# { "Depends": "py-genlayer:YOUR_GENLAYER_SDK_VERSION" }
from genlayer import *
from libraries.weather import WeatherLib

class MyWeatherContract(gl.Contract):
    current_temperature: float

    def __init__(self):
        self.current_temperature = 0.0

    @gl.public.write
    def update_city_temperature(self, city: str):
        """
        Fetches the current temperature for a specified city and updates the contract state.
        """
        try:
            temp = WeatherLib.get_temperature(city)
            self.current_temperature = temp
            StudioUXUtils.log_event("WeatherUpdate", {"city": city, "temperature": temp})
        except Exception as e:
            StudioUXUtils.log_event("WeatherError", {"city": city, "error": str(e)})
            # Implement contract-specific error handling, e.g., revert transaction or log for review

    @gl.public.view
    def get_city_temperature(self) -> float:
        """
        Returns the last fetched temperature for the city.
        """
        return self.current_temperature
```

#### Utilizing Secure API Key Management

First, deploy the `SecureAPIKeyManager` contract. Then, from your owner account, set an encrypted API key:

```python
# Assuming SecureAPIKeyManager is deployed at `api_key_manager_address`
from services.secure_api_key_manager import SecureAPIKeyManager

# In a separate script or owner-controlled contract:
# api_key_manager_contract = gl.Contract.at(SecureAPIKeyManager, api_key_manager_address)
# api_key_manager_contract.set_api_key("OpenWeatherMap", "ENCRYPTED_OPENWEATHER_API_KEY")

# In your Intelligent Contract that needs the key:
class MyContractWithAPI(gl.Contract):
    # ...
    @gl.public.write
    def call_external_api(self, service_name: str, api_key_manager_address: Address):
        api_key_manager = gl.Contract.at(SecureAPIKeyManager, api_key_manager_address)
        encrypted_key = api_key_manager.get_api_key(service_name)
        
        # In a real scenario, the encrypted_key would be decrypted within a secure environment
        # or passed to a trusted off-chain service for API calls.
        # For demonstration, assume `gl.nondet.web.get` can handle encrypted keys or a proxy service.
        # response = gl.nondet.web.get(f"https://api.example.com/data?key={encrypted_key}")
        # ... process response ...
```

**Note on Encryption**: The actual decryption of API keys should occur in a secure, trusted execution environment (TEE) or an off-chain oracle service that the GenLayer validators can verify. The `SecureAPIKeyManager` contract primarily provides a decentralized and auditable way to store *references* to these encrypted keys.

#### Enhancing UX with Studio Utilities

```python
from services.studio_ux_utils import StudioUXUtils

class MyDataProcessingContract(gl.Contract):
    processed_data: dict

    def __init__(self):
        self.processed_data = {}

    @gl.public.write
    def process_and_log_data(self, raw_input: str):
        # Simulate data processing
        result = {"input": raw_input, "status": "processed", "timestamp": gl.timestamp()}
        self.processed_data = result
        
        # Log event for Studio visibility
        StudioUXUtils.log_event("DataProcessed", result)
        
        # Format output for better readability in Studio if needed
        formatted_output = StudioUXUtils.format_json_output(result)
        print(f"Formatted Result:\n{formatted_output}")
```

## 🛡️ Security Considerations

Security is paramount in Intelligent Contract development. This project adheres to several best practices:

- **Equivalence Principle**: All external data fetching leverages GenLayer's equivalence principle (`gl.eq_principle.strict_eq`) to ensure consensus among validators on non-deterministic outcomes.
- **API Key Isolation**: Sensitive API keys are not directly exposed within the Intelligent Contract logic. Instead, they are managed by a dedicated `SecureAPIKeyManager` contract, reducing the risk of compromise.
- **Input Validation**: `StudioUXUtils` includes basic input validation, which should be extended with robust schema validation in production environments to prevent common vulnerabilities.
- **Trusted Data Sources**: Emphasize using reputable and stable external API providers to minimize data inconsistency and downtime risks.

## 🤝 Contributing

We welcome contributions from the GenLayer community! If you have suggestions for new libraries, services, or improvements to existing ones, please feel free to open an issue or submit a pull request. Refer to our `CONTRIBUTING.md` (to be added) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

*Built with ❤️ for the GenLayer community by Manus AI.*
