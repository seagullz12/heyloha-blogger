from agents import Agent, function_tool
from ai_agents.news_agent import Article
import logging

logger = logging.getLogger("agents")

@function_tool
def is_relevant(article: Article) -> bool:
    # Geen harde keywords meer, AI beslist op basis van instructie en content
    logger.info(f"Beoordeel relevantie artikel: '{article.title}'")
    # We geven alleen de tekst door, terugkomst via model
    return None  # placeholder, de Agent gebruikt de prompt om te beslissen

relevance_agent = Agent(
    name="RelevanceAgent",
    instructions=(
        "Lees het nieuwsartikel en beoordeel of het relevant is voor een blog over ai, klantcontact, "
        "customer service, werkdruk, klantvragen, digitalisering of slimme bedrijfsvoering. "
        "Verbindingen leggen mag – als het haakjes heeft met klantvragen, efficiëntie of toekomst van werk, is het bruikbaar. "
        "Geef **true** als er enige relevantie is. Geef **false** als het echt totaal geen bruikbare haakjes heeft."
    ),
    model="gpt-4o-mini",
    tools=[is_relevant],
)