import asyncio
from ai_agents.relevance_agent import is_relevant
from ai_agents.relevance_agent import Article  # your Pydantic model

async def test():
    article = Article(
        title="Heyloha launches new AI chatbot for customer service",
        description="This product automates repetitive customer questions efficiently."
    )
    result = await is_relevant(article)
    print("Is relevant:", result)

asyncio.run(test())
