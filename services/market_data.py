# market_data.py
# This service handles all stock data fetching using yfinance.
# It acts as a wrapper so the rest of the app never talks to yfinance directly.
# If we ever switch data providers, we only change this file.

import yfinance as yf

def get_stock_info(ticker: str) -> dict:
    """
    Fetch basic information about a stock.
    ticker: stock symbol like 'AAPL' or 'TSLA'
    Returns a dictionary with company name, price, change, etc.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "name": info.get("longName", "N/A"),
            "symbol": ticker.upper(),
            "price": info.get("currentPrice", info.get("regularMarketPrice", "N/A")),
            "change_percent": info.get("52WeekChange", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "website": info.get("website", "N/A"),
        }
    except Exception as e:
        return {"error": str(e)}


def get_stock_history(ticker: str, period: str = "1mo") -> object:
    """
    Fetch historical price data for charting.
    period options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y
    Returns a pandas DataFrame with columns: Open, High, Low, Close, Volume
    """
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)
        return history
    except Exception as e:
        return None


def get_market_overview() -> list:
    """
    Fetch current data for major market indices.
    Returns a list of dicts with name and current price.
    """
    indices = {
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC",
        "Dow Jones": "^DJI",
    }

    results = []
    for name, symbol in indices.items():
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            results.append({
                "name": name,
                "symbol": symbol,
                "price": info.get("regularMarketPrice", "N/A"),
                "change_percent": info.get("regularMarketChangePercent", "N/A"),
            })
        except Exception as e:
            results.append({"name": name, "symbol": symbol, "error": str(e)})

    return results