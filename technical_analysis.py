# technical_analysis_server.py
import pandas as pd
import numpy as np
import talib
from mcp.server.fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP("TechnicalAnalysis")

def get_stock_data(ticker, period="1y"):
    """Helper to get stock price data"""
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

@mcp.tool()
def analyze_moving_averages(ticker: str, short_term: int = 50, long_term: int = 200) -> dict:
    """
    Analyze moving averages to identify trends and crossovers
    
    Args:
        ticker: Stock ticker symbol
        short_term: Short-term MA period (default: 50)
        long_term: Long-term MA period (default: 200)
    """
    try:
        df = get_stock_data(ticker)
        
        # Calculate moving averages
        df['SMA_short'] = talib.SMA(df['Close'].values, timeperiod=short_term)
        df['SMA_long'] = talib.SMA(df['Close'].values, timeperiod=long_term)
        
        # Get latest prices
        latest_close = df['Close'].iloc[-1]
        latest_short_ma = df['SMA_short'].iloc[-1]
        latest_long_ma = df['SMA_long'].iloc[-1]
        
        # Identify trend
        if latest_short_ma > latest_long_ma:
            trend = "Bullish"
        else:
            trend = "Bearish"
        
        # Detect crossover in last 10 days
        crossover = "None"
        for i in range(min(10, len(df)-1)):
            if (df['SMA_short'].iloc[-(i+2)] < df['SMA_long'].iloc[-(i+2)] and 
                df['SMA_short'].iloc[-(i+1)] > df['SMA_long'].iloc[-(i+1)]):
                crossover = "Golden Cross (Bullish)"
                break
            elif (df['SMA_short'].iloc[-(i+2)] > df['SMA_long'].iloc[-(i+2)] and 
                  df['SMA_short'].iloc[-(i+1)] < df['SMA_long'].iloc[-(i+1)]):
                crossover = "Death Cross (Bearish)"
                break
        
        # Prepare result
        return {
            "ticker": ticker,
            "current_price": latest_close,
            f"SMA_{short_term}": latest_short_ma,
            f"SMA_{long_term}": latest_long_ma,
            "trend": trend,
            "recent_crossover": crossover,
            "above_short_ma": latest_close > latest_short_ma,
            "above_long_ma": latest_close > latest_long_ma,
            "price_to_short_ma_ratio": latest_close / latest_short_ma if latest_short_ma else None,
            "price_to_long_ma_ratio": latest_close / latest_long_ma if latest_long_ma else None
        }
    except Exception as e:
        return {"error": f"Failed to analyze moving averages: {str(e)}"}

@mcp.tool()
def calculate_rsi(ticker: str, period: int = 14) -> dict:
    """
    Calculate Relative Strength Index (RSI) to identify overbought/oversold conditions
    
    Args:
        ticker: Stock ticker symbol
        period: RSI period (default: 14)
    """
    try:
        df = get_stock_data(ticker)
        
        # Calculate RSI
        df['RSI'] = talib.RSI(df['Close'].values, timeperiod=period)
        
        # Get latest RSI
        latest_rsi = df['RSI'].iloc[-1]
        
        # Determine condition
        if latest_rsi >= 70:
            condition = "Overbought"
        elif latest_rsi <= 30:
            condition = "Oversold"
        else:
            condition = "Neutral"
        
        # RSI trend
        rsi_trend = "Neutral"
        if len(df) >= 5:
            rsi_5_days_ago = df['RSI'].iloc[-5]
            if latest_rsi > rsi_5_days_ago:
                rsi_trend = "Increasing"
            elif latest_rsi < rsi_5_days_ago:
                rsi_trend = "Decreasing"
        
        return {
            "ticker": ticker,
            "current_price": df['Close'].iloc[-1],
            "rsi": latest_rsi,
            "condition": condition,
            "rsi_trend": rsi_trend,
            "rsi_history": df['RSI'].dropna().tail(5).tolist()
        }
    except Exception as e:
        return {"error": f"Failed to calculate RSI: {str(e)}"}

@mcp.tool()
def analyze_macd(ticker: str) -> dict:
    """
    Analyze Moving Average Convergence Divergence (MACD) for buy/sell signals
    
    Args:
        ticker: Stock ticker symbol
    """
    try:
        df = get_stock_data(ticker)
        
        # Calculate MACD
        macd, signal, hist = talib.MACD(
            df['Close'].values, 
            fastperiod=12, 
            slowperiod=26, 
            signalperiod=9
        )
        
        df['MACD'] = macd
        df['Signal'] = signal
        df['Histogram'] = hist
        
        # Get latest values
        latest_macd = df['MACD'].iloc[-1]
        latest_signal = df['Signal'].iloc[-1]
        latest_hist = df['Histogram'].iloc[-1]
        
        # Determine signal
        if latest_macd > latest_signal and latest_hist > 0:
            signal_type = "Buy"
        elif latest_macd < latest_signal and latest_hist < 0:
            signal_type = "Sell"
        else:
            signal_type = "Neutral"
        
        # Detect crossover in last 5 days
        crossover = "None"
        for i in range(min(5, len(df)-1)):
            if (df['MACD'].iloc[-(i+2)] < df['Signal'].iloc[-(i+2)] and 
                df['MACD'].iloc[-(i+1)] > df['Signal'].iloc[-(i+1)]):
                crossover = "Bullish Crossover"
                break
            elif (df['MACD'].iloc[-(i+2)] > df['Signal'].iloc[-(i+2)] and 
                  df['MACD'].iloc[-(i+1)] < df['Signal'].iloc[-(i+1)]):
                crossover = "Bearish Crossover"
                break
        
        return {
            "ticker": ticker,
            "current_price": df['Close'].iloc[-1],
            "macd": latest_macd,
            "signal_line": latest_signal,
            "histogram": latest_hist,
            "signal": signal_type,
            "recent_crossover": crossover,
            "macd_above_signal": latest_macd > latest_signal,
            "histogram_increasing": df['Histogram'].iloc[-1] > df['Histogram'].iloc[-2] if len(df) > 1 else None
        }
    except Exception as e:
        return {"error": f"Failed to analyze MACD: {str(e)}"}

if __name__ == "__main__":
    mcp.run()