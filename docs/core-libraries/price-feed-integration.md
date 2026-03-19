# Price Feed Integration

## Overview

The `PriceFeedLib` empowers GenLayer Intelligent Contracts to access real-time financial market data, specifically cryptocurrency and stock prices. It integrates with CoinGecko for crypto prices and Alpha Vantage for stock prices, providing essential data for decentralized finance (DeFi) applications and other financial instruments built on GenLayer.

## Features

- **Cryptocurrency Prices**: Fetches current prices for a wide range of cryptocurrencies via CoinGecko.
- **Stock Prices**: Retrieves real-time stock quotes using Alpha Vantage (requires an API key).
- **Robust Error Handling**: Designed to gracefully handle API errors, rate limits, and invalid responses.
- **Equivalence Principle**: Ensures data consistency across validators for critical financial data.

## Usage

To utilize the `PriceFeedLib`, import it into your Intelligent Contract and call the relevant static methods. Ensure your contract declares the `py-genlayer` dependency.

### Example: Fetching Cryptocurrency Price

This example demonstrates how to fetch the current price of a cryptocurrency (e.g., Ethereum) against a fiat currency (e.g., USD).

```python
# { "Depends": "py-genlayer:YOUR_GENLAYER_SDK_VERSION" }
from genlayer import *
from libraries.price_feed import PriceFeedLib
from services.studio_ux_utils import StudioUXUtils

class CryptoPriceContract(gl.Contract):
    crypto_symbol: str
    current_price: typing.Optional[float]
    last_updated: int

    def __init__(self):
        self.crypto_symbol = ""
        self.current_price = None
        self.last_updated = 0

    @gl.public.write
    def update_crypto_price(self, symbol: str, currency: str = "usd"):
        """
        Fetches the current price of a cryptocurrency and updates the contract state.
        """
        try:
            price = PriceFeedLib.get_crypto_price(symbol, currency)
            if price is not None:
                self.crypto_symbol = symbol
                self.current_price = price
                self.last_updated = gl.timestamp()
                StudioUXUtils.log_event("CryptoPriceUpdateSuccess", {
                    "symbol": symbol,
                    "currency": currency,
                    "price": price,
                    "timestamp": self.last_updated
                })
            else:
                StudioUXUtils.log_event("CryptoPriceUpdateFailed", {"symbol": symbol, "reason": "Could not retrieve price"})
                raise Exception(f"Failed to retrieve crypto price for {symbol}")
        except Exception as e:
            StudioUXUtils.log_event("CryptoPriceUpdateError", {"symbol": symbol, "error": str(e)})
            raise

    @gl.public.view
    def get_last_crypto_price(self) -> typing.Optional[float]:
        """
        Returns the last successfully fetched cryptocurrency price.
        """
        return self.current_price
```

### Example: Fetching Stock Price

This example demonstrates how to fetch the current stock price for a given ticker symbol using Alpha Vantage. An API key is required for Alpha Vantage.

```python
# { "Depends": "py-genlayer:YOUR_GENLAYER_SDK_VERSION" }
from genlayer import *
from libraries.price_feed import PriceFeedLib
from services.studio_ux_utils import StudioUXUtils
from services.secure_api_key_manager import SecureAPIKeyManager

class StockPriceContract(gl.Contract):
    stock_symbol: str
    current_price: typing.Optional[float]
    last_updated: int

    def __init__(self):
        self.stock_symbol = ""
        self.current_price = None
        self.last_updated = 0

    @gl.public.write
    def update_stock_price(self, symbol: str, api_key_manager_address: Address):
        """
        Fetches the current stock price and updates the contract state.
        Retrieves Alpha Vantage API key from SecureAPIKeyManager.
        """
        try:
            # Retrieve API key securely
            api_key_manager = gl.Contract.at(SecureAPIKeyManager, api_key_manager_address)
            # In a real scenario, the encrypted_key would be decrypted by a trusted oracle/proxy
            # For this example, we assume the API key is directly usable after retrieval
            alphavantage_api_key = api_key_manager.get_api_key_for_proxy("AlphaVantage")

            price = PriceFeedLib.get_stock_price(symbol, alphavantage_api_key)
            if price is not None:
                self.stock_symbol = symbol
                self.current_price = price
                self.last_updated = gl.timestamp()
                StudioUXUtils.log_event("StockPriceUpdateSuccess", {
                    "symbol": symbol,
                    "price": price,
                    "timestamp": self.last_updated
                })
            else:
                StudioUXUtils.log_event("StockPriceUpdateFailed", {"symbol": symbol, "reason": "Could not retrieve price"})
                raise Exception(f"Failed to retrieve stock price for {symbol}")
        except Exception as e:
            StudioUXUtils.log_event("StockPriceUpdateError", {"symbol": symbol, "error": str(e)})
            raise

    @gl.public.view
    def get_last_stock_price(self) -> typing.Optional[float]:
        """
        Returns the last successfully fetched stock price.
        """
        return self.current_price
```

## Error Handling and Robustness

- **API Specific Errors**: Both `_fetch_from_coingecko` and `_fetch_from_alphavantage` methods include checks for HTTP status codes and print detailed error messages in case of failure. Alpha Vantage also has specific checks for its response format.
- **`None` Return on Failure**: All `get_..._price` methods return `None` if data retrieval or parsing fails, allowing the calling contract to handle these scenarios.
- **Contract-Level Exception Handling**: It is crucial for Intelligent Contracts to implement `try-except` blocks to catch exceptions raised by the `PriceFeedLib` and handle them appropriately (e.g., revert, log, or retry).

## Security Considerations

- **API Key Management**: For Alpha Vantage, an API key is mandatory. **Never embed API keys directly in your contract code.** Always use the `SecureAPIKeyManager` service to store encrypted API keys and retrieve them via an authorized proxy contract or trusted oracle service at runtime. This prevents exposure of sensitive credentials.
- **Data Integrity**: The `gl.eq_principle.strict_eq` is used for all external data fetches to ensure that all validators agree on the exact price data, which is critical for financial applications.
- **Data Source Reliability**: Financial data is highly sensitive. Always choose reputable and reliable price feed providers. Consider implementing additional checks for data freshness and validity within your contract logic.
- **Decentralized Oracles**: For production-grade DeFi applications, consider integrating with decentralized oracle networks (e.g., Chainlink) that aggregate data from multiple sources, providing a more robust and censorship-resistant price feed.
