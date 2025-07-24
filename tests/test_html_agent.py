import asyncio
from agents import Runner
from ai_agents.html_agent import html_agent, HtmlOutput

async def test_html_agent():
    sample_blog_text = """
# Slimmer Klantcontact met AI: De Toekomst van Klantenservice

In de wereld van klantenservice zien we een opvallende trend. Bedrijven omarmen steeds vaker de kracht van Artificial Intelligence (AI) om hun klantcontact te verbeteren. Een recent artikel van Tech Today benadrukt hoe nieuwe AI-tools bedrijven helpen om klantvragen sneller te beantwoorden. Dit is niet alleen een technologische doorbraak, maar ook een kans om de klantbeleving aanzienlijk te verbeteren.

## Wat zijn AI-tools en hoe werken ze?

AI-tools maken gebruik van geavanceerde algoritmes die klantfeedback en vragen analyseren. Door deze technologie kunnen bedrijven veel sneller inspelen op de behoeften van hun klanten. In plaats van dat een medewerker handmatig elke vraag moet verwerken, kan AI deze taken automatiseren. Dit leidt tot een snellere responstijd en een efficiënter werkproces.

Stel je voor dat je als klant een vraag hebt. In plaats van lange wachttijden aan de telefoon of eindeloos zoeken op een website, krijg je binnen enkele seconden een antwoord dat specifiek op jouw vraag is afgestemd. Dit is de toekomst van klantcontact, en bedrijven die deze technologie omarmen, zullen een streepje voor hebben.

## Heyloha en de voordelen van AI

Bij Heyloha begrijpen we dat klantcontact niet alleen om snelheid draait, maar ook om kwaliteit. Onze slimme oplossingen zijn ontworpen om bedrijven te helpen bij het efficiënt beheren van klantvragen. Door gebruik te maken van AI kunnen we de werkdruk van medewerkers verminderen en tegelijkertijd de klanttevredenheid verhogen. Dit sluit perfect aan bij de trends die in het artikel worden besproken.

Met Heyloha kunnen bedrijven profiteren van een geautomatiseerde klantenservice die niet alleen de snelheid verbetert, maar ook de consistentie en relevantie van de antwoorden. Dit zorgt ervoor dat klanten zich gehoord en gewaardeerd voelen, wat cruciaal is voor hun loyaliteit.

## De toekomst van klantenservice

De integratie van AI in klantcontact is meer dan een tijdelijke trend; het is de toekomst. Bedrijven die nu investeren in deze technologie zullen niet alleen de tevredenheid van hun klanten verhogen, maar ook de efficiëntie van hun medewerkers verbeteren. Dit is een win-winsituatie die leidt tot een hogere productiviteit en betere service.

Het artikel van Tech Today biedt een inspirerende kijk op hoe AI-tools kunnen bijdragen aan een beter klantcontact. En met innovaties zoals die van Heyloha wordt deze toekomst al werkelijkheid. Wil je meer weten over hoe wij bedrijven helpen bij het optimaliseren van klantcontact? Neem dan een kijkje op [https://heyloha.ai](https://heyloha.ai).

## Bron
Dit artikel is geïnspireerd door het artikel "AI verbetert klantcontact: Nieuwe AI-tools helpen bedrijven klantvragen sneller te beantwoorden" van Tech Today. Je kunt het volledige artikel hier lezen: [Tech Today](https://techtoday.com/ai-verbeterd-klantcontact).
"""

    result = await Runner.run(html_agent, input=sample_blog_text)

    if isinstance(result.final_output, HtmlOutput):
        print("Gegenereerde HTML:")
        print(result.final_output.html)
    else:
        print("Geen geldige output ontvangen.")

if __name__ == "__main__":
    asyncio.run(test_html_agent())