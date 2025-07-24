from agents import Agent, function_tool
from pydantic import BaseModel

class EditOutput(BaseModel):
    improved_text: str
    notes: str 

@function_tool
def edit_blog(text: str) -> EditOutput:
    prompt = f"""
        Je bent een ervaren redacteur. Verbeter de volgende blogtekst:
        - Zorg voor vloeiende zinnen en goede leesbaarheid.
        - Verbeter grammatica en spelling.
        - Verbeter structuur waar nodig.
        - Houd de originele boodschap en toon casual en toegankelijk.
        - Geef een korte samenvatting van verbeteringen die je hebt gedaan.

        Blogtekst:
        {text}

        Verbeterde blogtekst:
    """
    return EditOutput(improved_text=prompt, notes="Redactie prompt gegenereerd")

redactie_agent = Agent(
    name="RedactieAgent",
    instructions=(
        "Verbeter en redigeer de gegeven blogtekst op leesbaarheid, grammatica, spelling en structuur. "
        "Behoud een casual en toegankelijke toon. Geef ook een korte samenvatting van de aangebrachte verbeteringen."
    ),
    model="gpt-4o-mini",
    tools=[edit_blog],
    output_type=EditOutput,
)