# Getting Started

This section provides a step-by-step guide to setting up your development environment and integrating the GenLayer Tools & Infrastructure into your Intelligent Contracts.

## 1. Prerequisites

Before you begin, ensure you have the following installed and configured:

-   **GenLayer SDK**: The official GenLayer Software Development Kit. Follow the [official GenLayer documentation](https://docs.genlayer.com/developers/development-setup) for installation and setup instructions.
-   **Python 3.8+**: This project is developed using Python. We recommend using a virtual environment to manage dependencies.
-   **`pip`**: Python's package installer, usually comes with Python.
-   **`git`**: For cloning the repository.

## 2. Clone the Repository

First, clone this `genlayer-tools` repository to your local machine:

```bash
git clone https://github.com/JAGUNG17/genlayer-tools.git
cd genlayer-tools
```

## 3. Install Dependencies (if any)

Currently, the core libraries primarily rely on the `genlayer` SDK and standard Python libraries. If any additional Python dependencies are introduced in the future, they will be listed in a `requirements.txt` file. You would install them using:

```bash
pip install -r requirements.txt
```

## 4. Integrate into Your Intelligent Contract Project

To use the libraries and services in your own Intelligent Contract project, you can either:

### Option A: Copy Files Directly (Recommended for simplicity)

Copy the `libraries/` and `services/` directories directly into your Intelligent Contract project's directory. This is the simplest way to get started, especially for smaller projects.

```bash
cp -r genlayer-tools/libraries /path/to/your/genlayer_project/
cp -r genlayer-tools/services /path/to/your/genlayer_project/
```

Then, in your Intelligent Contract files, you can import them as shown in the examples:

```python
# { "Depends": "py-genlayer:YOUR_GENLAYER_SDK_VERSION" }
from genlayer import *
from libraries.weather import WeatherLib
from services.secure_api_key_manager import SecureAPIKeyManager
# ... and so on
```

### Option B: Install as a Python Package (Advanced)

For larger projects or if you plan to contribute back, you might consider packaging these tools as a local Python package. This would involve creating a `setup.py` or `pyproject.toml` file and installing it in your development environment. This is beyond the scope of this basic 
guide, but is a viable option for advanced users.

## 5. Configure API Keys (for services requiring them)

For libraries and services that interact with external APIs requiring authentication (e.g., OpenWeatherMap, Alpha Vantage, Twitter), you will need to obtain API keys from the respective service providers. Once obtained, follow the instructions in the [Secure API Key Management documentation](#secure-api-key-management) to securely store and manage these keys using the `SecureAPIKeyManager` contract.

## 6. Explore Examples

Refer to the usage examples provided within each library and service documentation (e.g., [Weather API Integration](#weather-api-integration), [Price Feed Integration](#price-feed-integration)) to understand how to integrate these components into your Intelligent Contracts. These examples demonstrate common patterns and best practices.

By following these steps, you will be well-equipped to leverage the GenLayer Tools & Infrastructure to build powerful and secure Intelligent Contracts.
