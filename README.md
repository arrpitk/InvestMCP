# InvestMCP

![MCP](https://img.shields.io/badge/MCP-Enabled-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**InvestMCP** is a comprehensive suite of Model Context Protocol (MCP) servers that transform Claude AI into a powerful stock analysis assistant. This project enables seamless integration between Claude and financial data sources, allowing for natural language investment analysis through conversation.

## 🚀 Features

### Implemented Servers

- **Stock Data Server**: Access fundamental financial data including P/E ratios, dividend yields, revenue growth, and more.
  
- **Technical Analysis Server**: Generate technical indicators like RSI, MACD, moving averages, and identify chart patterns.
  
- **Financial News Server**: Analyze news sentiment and track breaking stories about companies to incorporate market sentiment into investment decisions.

### Planned Servers

- **Stock Screener Server**: Filter stocks based on custom criteria to discover investment opportunities.
  
- **Investment Advisor Server**: Receive personalized investment recommendations based on risk tolerance and goals.
  
- **Portfolio Tracker Server**: Track portfolio performance and get rebalancing suggestions.

## 📋 Requirements

- Python 3.10+
- Claude Desktop app with MCP support
- Required Python packages:
    - mcp\[cli]>=1.4.0
    - yfinance>=0.2.30
    - pandas>=2.0.0
    - numpy>=1.24.0
    - requests>=2.31.0
    - nltk>=3.8.1

## 🔧 Installation

1. Clone this repository:
 ```bash
 git clone https://github.com/arrpitk/InvestMCP.git
 cd InvestMCP
```

Configure Claude Desktop:

* Open Claude Desktop settings
* Navigate to Developer tab
* Click "Edit Config"
* Add the MCP server configuration (see example below)

## 🔍 Usage

### Claude Desktop Configuration

```
json
{
  "mcpServers": {
    "stock-data": {
      "command": "python3",
      "args": ["/path/to/InvestMCP/servers/stock_data_server.py"]
    },
    "technical-analysis": {
      "command": "python3",
      "args": ["/path/to/InvestMCP/servers/technical_analysis_server.py"]
    },
    "financial-news": {
      "command": "python3",
      "args": ["/path/to/InvestMCP/servers/financial_news_server.py"],
      "env": {
        "NEWS_API_KEY": "your-news-api-key-here"
      }
    }
  }
}
```

### Example Conversations

Once configured, you can talk to Claude naturally about stocks:

* "What are the key financial metrics for AAPL?"
* "Show me the technical analysis for MSFT including RSI and MACD."
* "What's the current news sentiment around Tesla?"
* "Compare the fundamentals of AMZN and GOOGL."


## 🔜 Roadmap

1. Add Stock Screener functionality
2. Implement Investment Advisor capabilities
3. Add Portfolio Tracking and management
4. Create interactive visualizations for technical analysis
5. Add historical backtesting of investment strategies

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📢 Acknowledgements

* [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic
* [yfinance](https://github.com/ranaroussi/yfinance) for financial data
* [NLTK](https://www.nltk.org/) for sentiment analysis
