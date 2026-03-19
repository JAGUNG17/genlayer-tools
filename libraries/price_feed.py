from genlayer import *
import typing
import json

class PriceFeedLib:
    """
    A library for GenLayer Intelligent Contracts to interact with various price feed APIs.
    Supports CoinGecko for crypto prices and Alpha Vantage for stock prices, with robust error handling.
    """
    
    @staticmethod
    def _fetch_from_coingecko(symbol: str, currency: str = "usd") -> typing.Optional[dict]:
        """
        Fetches crypto price data from CoinGecko.
        """
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies={currency}"
            response = gl.nondet.web.get(url)
            if response.status_code == 200:
                return json.loads(response.body.decode("utf-8"))
            else:
                print(f"CoinGecko API error for {symbol}: {response.status_code} - {response.body.decode("utf-8")}")
                return None
        except Exception as e:
            print(f"Error fetching from CoinGecko for {symbol}: {e}")
            return None

    @staticmethod
    def _fetch_from_alphavantage(symbol: str, api_key: str) -> typing.Optional[dict]:
        """
        Fetches stock price data from Alpha Vantage.
        """
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
            response = gl.nondet.web.get(url)
            if response.status_code == 200:
                data = json.loads(response.body.decode("utf-8"))
                if "Global Quote" in data and "05. price" in data["Global Quote"]:
                    return data
                else:
                    print(f"Alpha Vantage API error for {symbol}: Invalid response format or API limit reached. {data}")
                    return None
            else:
                print(f"Alpha Vantage API error for {symbol}: {response.status_code} - {response.body.decode("utf-8")}")
                return None
        except Exception as e:
            print(f"Error fetching from Alpha Vantage for {symbol}: {e}")
            return None

    @staticmethod
    def get_crypto_price(symbol: str, currency: str = "usd") -> typing.Optional[float]:
        """
        Fetches current crypto price using CoinGecko API.
        """
        price_data = gl.eq_principle.strict_eq(lambda: PriceFeedLib._fetch_from_coingecko(symbol, currency))
        if price_data and symbol in price_data and currency in price_data[symbol]:
            return float(price_data[symbol][currency])
        return None

    @staticmethod
    def get_stock_price(symbol: str, api_key: str) -> typing.Optional[float]:
        """
        Fetches current stock price using Alpha Vantage API.
        Requires an API key.
        """
        stock_data = gl.eq_principle.strict_eq(lambda: PriceFeedLib._fetch_from_alphavantage(symbol, api_key))
        if stock_data and "Global Quote" in stock_data and "05. price" in stock_data["Global Quote"]:
            return float(stock_data["Global Quote"]["05. price"])
        return None
