# news_service.py
# This service fetches financial news articles using the NewsAPI.
# It loads the API key from the .env file so it's never hardcoded.

import requests
import os
from dotenv import load_dotenv

# Load the .env file so we can access NEWS_API_KEY
load_dotenv()

def get_news(query: str = "stock market", num_articles: int = 10) -> list:
    """
    Fetch recent news articles for a given search query.
    query: search term like 'Apple stock' or 'stock market'
    num_articles: how many articles to return
    Returns a list of article dicts with title, description, url, source
    """
    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        return [{"error": "NEWS_API_KEY not found in .env file"}]

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": api_key,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": num_articles,
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "ok":
            return [{"error": data.get("message", "Unknown error")}]

        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title", "No title"),
                "description": article.get("description", "No description"),
                "url": article.get("url", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "published_at": article.get("publishedAt", ""),
            })

        return articles

    except Exception as e:
        return [{"error": str(e)}]