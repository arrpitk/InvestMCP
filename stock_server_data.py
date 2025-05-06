# stock_data_server.py
import yfinance as yf
import pandas as pd
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("StockData")

@mcp.tool()
def get_fundamentals(ticker: str) -> dict:
    """
    Get fundamental data for a company
    
    Args:
        ticker: Stock ticker symbol (e.g., AAPL, MSFT)
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            "ticker": ticker,
            "name": info.get("shortName", "Unknown"),
            "sector": info.get("sector", "Unknown"),
            "industry": info.get("industry", "Unknown"),
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE", None),
            "forward_pe": info.get("forwardPE", None),
            "peg_ratio": info.get("pegRatio", None),
            "price_to_book": info.get("priceToBook", None),
            "dividend_yield": info.get("dividendYield", None) * 100 if info.get("dividendYield") else None,
            "earnings_growth": info.get("earningsGrowth", None),
            "revenue_growth": info.get("revenueGrowth", None),
            "profit_margins": info.get("profitMargins", None) * 100 if info.get("profitMargins") else None,
            "debt_to_equity": info.get("debtToEquity", None),
            "current_ratio": info.get("currentRatio", None),
            "return_on_equity": info.get("returnOnEquity", None) * 100 if info.get("returnOnEquity") else None,
            "beta": info.get("beta", None),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh", None),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow", None),
            "current_price": info.get("currentPrice", None),
            "target_price": info.get("targetMeanPrice", None)
        }
    except Exception as e:
        return {"error": f"Failed to fetch fundamental data: {str(e)}"}

@mcp.tool()
def get_historical_data(ticker: str, period: str = "1y") -> dict:
    """
    Get historical price data for analysis
    
    Args:
        ticker: Stock ticker symbol
        period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    """
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)
        
        # Convert to lists for JSON serialization
        data = {
            "ticker": ticker,
            "period": period,
            "dates": history.index.strftime('%Y-%m-%d').tolist(),
            "open": history['Open'].tolist(),
            "high": history['High'].tolist(),
            "low": history['Low'].tolist(),
            "close": history['Close'].tolist(),
            "volume": history['Volume'].tolist()
        }
        
        return data
    except Exception as e:
        return {"error": f"Failed to fetch historical data: {str(e)}"}

if __name__ == "__main__":
    mcp.run()