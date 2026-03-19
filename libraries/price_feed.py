from genlayer import *
import typing
import json

class PriceFeedLib:
    """
    A library for GenLayer Intelligent Contracts to interact with price feeds.
    """
    
    @staticmethod
    def get_crypto_price(symbol: str, currency: str = "usd") -> float:
        """
        Fetches current crypto price using CoinGecko API.
        """
        def fetch_price() -> str:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies={currency}"
            response = gl.nondet.web.get(url)
            return response.body.decode("utf-8")

        # Use equivalence principle to ensure consensus on the price data
        price_data_raw = gl.eq_principle.strict_eq(fetch_price)
        price_data = json.loads(price_data_raw)
        return float(price_data[symbol][currency])

    @staticmethod
    def get_stock_price(symbol: str, api_key: str) -> float:
        """
        Fetches current stock price using Alpha Vantage API.
        """
        def fetch_stock() -> str:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
            response = gl.nondet.web.get(url)
            return response.body.decode("utf-8")

        # Use equivalence principle to ensure consensus on the stock data
        stock_data_raw = gl.eq_principle.strict_eq(fetch_stock)
        stock_data = json.loads(stock_data_raw)
        return float(stock_data["Global Quote"]["05. price"])
