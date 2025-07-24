from typing import List, Optional
from pydantic import BaseModel
from agents import Agent, function_tool, ModelSettings
import logging
import re

logger = logging.getLogger("agents")

class Article(BaseModel):
    title: str
    description: str
    source_name: Optional[str]
    source_id: Optional[str]
    published_at: Optional[str]
    url: Optional[str]

class BlogOutput(BaseModel):
    text: str
    summary: str
    
@function_tool
def generate_blog(articles: List[Article], previous_blogs: str = "", heyloha_info: str = "") -> str:
    logger.info(f"Received previous blogs for context (first 500 chars): {previous_blogs[:500]}")
    
    # Ensure Article objects are converted to dictionaries for JSON serialization safety if needed by the framework
    # (This line is a safeguard based on previous debugging, ensure it's in sync with your Runner's needs)
    articles_as_dicts = [article.model_dump() for article in articles]

    artikelen_tekst = ""
    for article_dict in articles_as_dicts:
        artikelen_tekst += (
            f"- {article_dict['title']}: {article_dict['description'].strip()} "
            f"(Bron: {article_dict['source_name']})\n"
        )
    logger.info(f"Genereren blog prompt met {len(articles)} artikelen")
    prompt = f"""
    Je krijgt deze achtergrond over Heyloha:

    {heyloha_info}

    En deze eerdere blogs:

    {previous_blogs}

    ---

    **Opdracht:**

    Kies uit de onderstaande nieuwsartikelen **één** artikel dat het beste past bij Heyloha en haar doelgroep.

    Schrijf vervolgens een goed gestructureerde, en makkelijk leesbare Nederlandstalige blog **alleen over dat artikel**.

    - Gebruik duidelijke koppen (zoals H1, H2) en tussenkopjes om de tekst overzichtelijk te maken.
    - Zorg voor paragrafen, geen lange lappen tekst.
    - De tone-of-voice moet **menselijk, helder en vriendelijk** zijn.
    - Schrijf **resultaatgericht** en **toegankelijk**. Vermijd vakjargon.
    - Zoek een natuurlijk en relevant verband met Heyloha, bijvoorbeeld rondom klantvragen, slimme automatisering van klantenservice, het verminderen van werkdruk of het verbeteren van klantbeleving.
    - Leg uit hoe Heyloha hier een slimme oplossing voor biedt en koppel dit duidelijk aan het gekozen nieuwsartikel.
    - Voeg af en toe een link toe naar [https://heyloha.ai](https://heyloha.ai) voor meer informatie.
    - Maak er een vloeiend verhaal van, geen opsommingen.
    - Vat kort samen, koppel trends aan klantcontact en eindig met Heyloha als slimme oplossing.
    - Vermijd herhaling van onderwerpen die al in eerdere blogs zijn genoemd.
    - Bedenk nieuwe invalshoeken en wees origineel.
    - Laat de blog op een natuurlijke manier Heyloha noemen als onderdeel van het verhaal, zonder dat het voelt als een promotie.

    ---

    **Nieuwsartikelen:**

    {artikelen_tekst}
"""
    bronnenlijst = "\n".join(
        f"- {article['title']} ({article['source_name']}, {article['url']})"
        for article in articles_as_dicts if article.get("url")
    )

    prompt += f"\n\n**Bronnenlijst:**\n\n{bronnenlijst}"

    return prompt

generate_blog_tool = generate_blog

blog_agent = Agent(
    name="BlogAgent",
    instructions=(
        "Je bent een ervaren Nederlandstalige tekstschrijver die blogs schrijft voor bedrijven. "
        "Je stijl is **menselijk, helder en vriendelijk**. "
        "Kies uit de nieuwsartikelen **één artikel** dat het beste past bij Heyloha en haar doelgroep. "
        "Schrijf een toegankelijke, casual Nederlandstalige blog **alleen over dat artikel**, met duidelijke koppen en paragrafen voor goede leesbaarheid. "
        "De focus ligt op **resultaatgericht** en **toegankelijk** schrijven, waarbij vakjargon wordt vermeden en concrete voordelen worden benadrukt. "
        "Laat de blog op een natuurlijke manier Heyloha noemen als onderdeel van het verhaal, zonder dat het voelt als promotie. "
        "Maak een natuurlijk en relevant verband met Heyloha, bijvoorbeeld rondom klantvragen, slimme automatisering van klantenservice, het verminderen van werkdruk of het verbeteren van klantbeleving. "
        "Leg uit hoe Heyloha hier een slimme oplossing voor biedt. "
        "Verwerk af en toe een link naar https://heyloha.ai, maar maak het geen spam. "
        "Schrijf vloeiend en vermijd opsommingen. "
        "Vat bondig samen, houd rekening met eerdere blogs om herhaling te voorkomen. "
        "Bedenk nieuwe invalshoeken en schrijf origineel. "
        "Noem de bron van het gekozen artikel, inclusief de url en titel. "
        "Geef alleen platte tekst terug."
    ),
    model="gpt-4o-mini",
    model_settings=ModelSettings(temperature=0.8),
    tools=[generate_blog_tool],
    output_type=BlogOutput,
)