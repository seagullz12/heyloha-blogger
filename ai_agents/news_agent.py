from agents import Agent, function_tool
from typing import List
from pydantic import BaseModel
import httpx
import os
import logging

logger = logging.getLogger("agents")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class Article(BaseModel):
    title: str
    description: str
    source_name: str | None = None
    source_id: str | None = None
    published_at: str | None = None
    url: str | None = None

@function_tool
async def fetch_news(query: str = "") -> List[Article]:
    logger.info(f"Fetching news for query: {query}")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5,
        "sortBy": "popularity",
        "searchIn": "title,description,content"
    }
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        articles = [Article(
            title=item.get("title", "").strip(),
            description=item.get("content") or item.get("description") or "",
            source_name=item.get("source", {}).get("name"),
            source_id=item.get("source", {}).get("id"),
            published_at=item.get("publishedAt"),
            url=item.get("url"),
        ) for item in data.get("articles", [])]
        for a in articles:
                logger.info(f"Article: {a.title} | URL: {a.url} | Bron: {a.source_name} | Published: {a.published_at}")
        return articles

news_agent = Agent(
    name="NewsAgent",
    instructions="Haal maximaal 5 relevante, recente Engelstalige nieuwsartikelen op over het onderwerp.",
    model="gpt-4o-mini",
    tools=[fetch_news],
    output_type=List[Article],
)