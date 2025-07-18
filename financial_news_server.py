# financial_news_server.py
import requests
from datetime import datetime, timedelta
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("FinancialNews")

# Use an API key from environment variable
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "your_news_api_key")

@mcp.tool()
def get_company_news(ticker: str, company_name: str = None, days: int = 7) -> dict:
    """
    Get recent news articles about a company
    
    Args:
        ticker: Stock ticker symbol
        company_name: Company name for better search results (optional)
        days: Number of days to look back (default: 7)
    """
    try:
        search_term = company_name if company_name else ticker
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for API
        from_date = start_date.strftime('%Y-%m-%d')
        to_date = end_date.strftime('%Y-%m-%d')
        
        # Make API request to NewsAPI
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": f"{search_term} OR {ticker}",
            "from": from_date,
            "to": to_date,
            "language": "en",
            "sortBy": "relevancy",
            "apiKey": NEWS_API_KEY,
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get("status") != "ok":
            return {"error": f"API Error: {data.get('message', 'Unknown error')}"}
        
        # Process articles
        articles = []
        for article in data.get("articles", [])[:15]:  # Limit to 15 articles
            articles.append({
                "title": article.get("title"),
                "source": article.get("source", {}).get("name"),
                "published_at": article.get("publishedAt"),
                "url": article.get("url"),
                "description": article.get("description")
            })
        
        return {
            "ticker": ticker,
            "company": company_name if company_name else ticker,
            "date_range": f"{from_date} to {to_date}",
            "article_count": len(articles),
            "articles": articles
        }
    except Exception as e:
        return {"error": f"Failed to fetch news: {str(e)}"}

@mcp.tool()
def analyze_news_sentiment(ticker: str, company_name: str = None, days: int = 7) -> dict:
    """
    Analyze sentiment from recent news about a company
    
    Args:
        ticker: Stock ticker symbol
        company_name: Company name for better search results (optional)
        days: Number of days to look back (default: 7)
    """
    try:
        # First get the news
        news_result = get_company_news(ticker, company_name, days)
        
        if "error" in news_result:
            return news_result
        
        # Simple sentiment analysis using VADER
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        import nltk
        
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon')
        
        analyzer = SentimentIntensityAnalyzer()
        
        # Analyze each article
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        sentiment_scores = []
        
        for article in news_result["articles"]:
            text = f"{article['title']} {article['description'] or ''}"
            sentiment = analyzer.polarity_scores(text)
            
            article_sentiment = {
                "title": article["title"],
                "source": article["source"],
                "published_at": article["published_at"],
                "compound_score": sentiment["compound"],
                "sentiment": "positive" if sentiment["compound"] > 0.05 else 
                             "negative" if sentiment["compound"] < -0.05 else "neutral"
            }
            
            sentiment_scores.append(article_sentiment)
            
            if sentiment["compound"] > 0.05:
                positive_count += 1
            elif sentiment["compound"] < -0.05:
                negative_count += 1
            else:
                neutral_count += 1
        
        # Calculate aggregate sentiment
        total_articles = len(sentiment_scores)
        if total_articles > 0:
            avg_sentiment = sum(item["compound_score"] for item in sentiment_scores) / total_articles
            
            if avg_sentiment > 0.05:
                overall_sentiment = "Positive"
            elif avg_sentiment < -0.05:
                overall_sentiment = "Negative"
            else:
                overall_sentiment = "Neutral"
        else:
            avg_sentiment = 0
            overall_sentiment = "No data"
        
        return {
            "ticker": ticker,
            "company": company_name if company_name else ticker,
            "date_range": news_result["date_range"],
            "article_count": total_articles,
            "overall_sentiment": overall_sentiment,
            "sentiment_score": avg_sentiment,
            "positive_articles": positive_count,
            "neutral_articles": neutral_count,
            "negative_articles": negative_count,
            "sentiment_ratio": f"{positive_count}:{neutral_count}:{negative_count}",
            "article_sentiments": sentiment_scores
        }
    except Exception as e:
        return {"error": f"Failed to analyze sentiment: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
