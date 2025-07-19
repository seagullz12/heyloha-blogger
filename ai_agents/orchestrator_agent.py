from agents import Agent, Runner
from ai_agents.news_agent import news_agent
from ai_agents.relevance_agent import relevance_agent
from ai_agents.blog_agent import blog_agent
from ai_agents.html_agent import html_agent  
import json
from pydantic import BaseModel

class BlogOutputModel(BaseModel):
    text: str
    html: str

async def orchestrate(context):
    # Nieuws ophalen
    news_result = await Runner.run(news_agent, input=None, context=context)
    news_items = news_result.output or []

    if not news_items:
        return {"text": "Geen nieuwsartikelen gevonden.", "html": ""}

    # Filter relevante artikelen
    relevant = []
    for item in news_items:
        rel = await Runner.run(relevance_agent, input=item, context=context)
        if rel.output is True:
            relevant.append(item)

    if not relevant:
        return {"text": "Geen relevante artikelen gevonden.", "html": ""}

    # Blog genereren op basis van relevante artikelen (platte tekst)
    blog_result = await Runner.run(blog_agent, input=relevant, context=context)
    blog_text = blog_result.output or ""

    # HTML genereren op basis van de blogtekst
    html_result = await Runner.run(html_agent, input=blog_text, context=context)
    blog_html = html_result.output or ""
    
    result_dict = {"text": blog_text, "html": blog_html}
    return result_dict

orchestrator_agent = Agent(
    name="OrchestratorAgent",
    instructions=(
        "Haal nieuws op en selecteer artikelen relevant voor blogs over trends als klantgedrag, werkdruk, personeelstekort, technologie of digitalisering. "
        "Gebruik de relevance_agent om irrelevante artikelen te filteren. "
        "Genereer met blog_agent een Nederlandstalige blog gericht op ondernemers, met een subtiele link naar Heyloha.ai indien passend. "
        "Geef de blogtekst terug en vervolgens een HTML-versie van die blogtekst."
    ),
    
    model="gpt-4o-mini",
    output_type=BlogOutputModel
)

orchestrator_agent.run = orchestrate
