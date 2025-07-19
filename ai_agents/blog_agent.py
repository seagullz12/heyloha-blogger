from agents import Agent, function_tool
from pydantic import BaseModel
import re
from typing import List

class Article(BaseModel):
    title: str
    description: str
    source_name: str  # nieuwe metadata

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return "-".join(text.strip().split())[:40]

@function_tool
def generate_blog(articles: List[Article]) -> str:
    artikelen_tekst = ""
    for article in articles:
        artikelen_tekst += (
            f"- {article.title}: {article.description.strip()} "
            f"(Bron: {article.source_name})\n"
        )

    prompt = (
        "Schrijf een casual, makkelijk leesbare Nederlandstalige blog op basis van deze nieuwsartikelen. "
        "Maak er een vloeiend verhaal van, geen opsommingen. "
        "Vat kort samen, koppel trends aan klantcontact en eindig met Heyloha als slimme oplossing.\n\n"
        f"Nieuwsartikelen:\n{artikelen_tekst}"
    )

    return prompt

generate_blog_tool = generate_blog

blog_agent = Agent(
    name="BlogAgent",
    instructions=(
        "Schrijf een casual en makkelijk leesbare Nederlandstalige blog over de nieuwsartikelen. "
        "Maak er een vloeiend verhaal van, geen opsommingen. "
        "Vat kort samen, koppel trends aan klantcontact en eindig met Heyloha als slimme oplossing. "
        "Noem bij elk artikel de bron. Geef alleen platte tekst terug."
    ),
    model="gpt-4o-mini",
    tools=[generate_blog_tool],
)
