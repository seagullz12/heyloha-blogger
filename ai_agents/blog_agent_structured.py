from agents import Agent, function_tool
from pydantic import BaseModel
import re

class Article(BaseModel):
    title: str
    description: str
    source_name: str  # nieuwe metadata

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return "-".join(text.strip().split())[:40]

def generate_blog(articles: list[Article]) -> str:
    intro = (
        "De wereld verandert snel. Technologie en klantgedrag veranderen ook. "
        "Bedrijven voelen de druk en zoeken slimme oplossingen. "
        "Deze week zagen we een paar interessante dingen die daarbij helpen.\n"
    )

    body = ""
    for article in articles:
        body += (
            f"\n📰 **{article.title}**\n"
            f"{article.description.strip()}\n"
            f"*Bron: {article.source_name}*\n"
        )

    bridge = (
        "\nWat betekent dit voor ondernemers? Ze willen makkelijker werken, "
        "klanten sneller helpen en personeel beter inzetten.\n"
    )

    heyloha_pitch = (
        "\nHeyloha speelt hier slim op in. Deze chatbot helpt veelgestelde vragen te automatiseren, "
        "bijvoorbeeld in service, horeca, webshops en makelaardij. Zo bespaar je kosten en houd je klanten tevreden, "
        "ook buiten kantooruren.\n"
    )

    closing = (
        "\nHeyloha kan al meer dan de helft van de vragen zelf beantwoorden. Zo blijft je team vrij voor ingewikkelde dingen, "
        "zonder dat klanten langer hoeven te wachten.\n"
    )

    return intro + body + bridge + heyloha_pitch + closing

generate_blog_tool = function_tool(generate_blog)

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
