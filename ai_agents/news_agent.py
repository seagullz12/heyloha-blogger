from agents import Agent, function_tool
from pydantic import BaseModel
from typing import List
import os
import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class Article(BaseModel):
    title: str
    description: str
    source_name: str | None = None
    source_id: str | None = None
    published_at: str | None = None
    url: str | None = None

@function_tool
def fetch_news(query: str = "technology") -> List[Article]:
    """
    Haalt recente nieuwsartikelen op via NewsAPI.org.

    Args:
        query (str): Zoekterm, standaard "technology".

    Returns:
        List[Article]: Lijst van artikelen met titel, samenvatting en metadata.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5,
        "sortBy": "relevancy",  # meest relevante eerst
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        articles = []
        for item in data.get("articles", []):
            title = item.get("title", "").strip()
            desc = item.get("description") or ""
            source = item.get("source", {})
            articles.append(Article(
                title=title,
                description=desc,
                source_name=source.get("name"),
                source_id=source.get("id"),
                published_at=item.get("publishedAt"),
                url=item.get("url"),
            ))
        return articles
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

news_agent = Agent(
    name="NewsAgent",
    instructions=(
        "Haal maximaal 5 relevante, recente Engelstalige nieuwsartikelen op over het onderwerp dat wordt opgegeven. "
        "Retourneer een lijst van artikelen met titel, korte samenvatting en broninformatie."
    ),
    model="gpt-4o-mini",
    tools=[fetch_news],
    output_type=List[Article],
)
