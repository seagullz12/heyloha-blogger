from agents import Agent, function_tool, ModelSettings
from agents import Runner
from pydantic import BaseModel
import requests

# Stap 1: User Interface Agent
class URLInput(BaseModel):
    url: str

@function_tool
def ask_for_url(prompt: str = "Welke website wil je laten analyseren?") -> URLInput:
    print(prompt)
    url = input("URL: ")
    return URLInput(url=url)

ui_agent = Agent(
    name="UserInterfaceAgent",
    instructions=(
        "Vraag de gebruiker om de volledige URL van de website die geanalyseerd moet worden. "
        "Bevestig dat de URL geldig en volledig is (inclusief http(s)://)."
    ),
    model="gpt-4o-mini",
    tools=[ask_for_url],
    output_type=URLInput,
)

# Stap 2: Website Scraper Agent
class WebsiteData(BaseModel):
    text: str

@function_tool
def scrape_site(url_input: URLInput) -> WebsiteData:
    try:
        r = requests.get(url_input.url, timeout=10)
        if r.status_code == 200:
            return WebsiteData(text=r.text)
        else:
            return WebsiteData(text=f"Error {r.status_code} bij ophalen van {url_input.url}")
    except Exception as e:
        return WebsiteData(text=f"Fout bij ophalen: {str(e)}")

scraper_agent = Agent(
    name="WebsiteScraperAgent",
    instructions=(
        "Haal de volledige tekstuele inhoud van de opgegeven URL op. "
        "Concentreer je op leesbare content, zoals teksten van pagina, blogs, productbeschrijvingen. "
        "Negeer scripts en ongebruikte metadata."
    ),
    model="gpt-4o-mini",
    tools=[scrape_site],
    output_type=WebsiteData,
)

# Stap 3: Analyst Agent
class Insights(BaseModel):
    insights: str

@function_tool
def analyze_content(data: WebsiteData) -> Insights:
    prompt = f"""
Je krijgt de volgende webinhoud om te analyseren (maximaal 4000 tekens):

{data.text[:4000]}

Geef een helder en bondig overzicht van:
- De belangrijkste doelgroep(en) van het bedrijf
- De mogelijke bedrijfsdoelen op basis van de inhoud
- Centrale thema's en boodschappen die opvallen

Gebruik heldere, begrijpelijke taal en beperk jargon.

Ter context: Heyloha is een AI-oplossing voor klantcontact die klantvragen automatisch en vriendelijk afhandelt, werkdruk verlaagt, klanttevredenheid verhoogt en 24/7 beschikbaar is. Meer info: heyloha.ai
"""
    return Insights(insights=prompt)

analyst_agent = Agent(
    name="AnalystAgent",
    instructions=(
        "Analyseer de gegeven webinhoud en geef concrete marketinginzichten: "
        "doelgroep, bedrijfsdoelen, en hoofdthema's. "
        "Wees bondig en relevant."
    ),
    model="gpt-4o-mini",
    tools=[analyze_content],
    output_type=Insights,
)

# Stap 4: Campaign Idea Agent
class CampaignIdeas(BaseModel):
    ideas: str

@function_tool
def generate_campaigns(insights: Insights) -> CampaignIdeas:
    prompt = f"""
Hier is een samenvatting van marketinginzichten:

{insights.insights}

Bedenk 3 duidelijke, creatieve en gerichte marketingcampagne-ideeën. Zorg dat ze aansluiten op:
- De doelgroep en doelen van het bedrijf
- Heyloha’s kernwaarden: AI-klantenservice die 24/7 werkt, menselijk en vriendelijk is, werkdruk verlaagt, klanttevredenheid verhoogt

Formuleer de ideeën helder en praktisch, zodat een marketingteam ze gemakkelijk kan uitvoeren.

Website: heyloha.ai
"""
    return CampaignIdeas(ideas=prompt)

campaign_agent = Agent(
    name="CampaignIdeaAgent",
    instructions=(
        "Gebruik de inzichten om drie slimme en concrete marketingcampagnes te bedenken. "
        "Focus op praktische toepasbaarheid, duidelijke doelgroep, en Heyloha’s unieke voordelen."
    ),
    model="gpt-4o-mini",
    tools=[generate_campaigns],
    output_type=CampaignIdeas,
)

# Stap 5: Copywriter Agent
class CopyOutput(BaseModel):
    text: str

@function_tool
def write_copy(campaigns: CampaignIdeas) -> CopyOutput:
    prompt = f"""
Op basis van de volgende campagne-ideeën, schrijf korte en krachtige marketingcopy:

Campagnes:
{campaigns.ideas}

Maak:
- 1 social media post (max 280 tekens)
- 1 pakkende e-mail subject line en e-mail tekst (max 50 tekens voor subject en 1000 voor de e-mail)
- 1 blogtitel van maximaal 10 woorden, en een blog van maximaal 300 woorden

Merk: Heyloha (heyloha.ai) - AI-klantenservice die automatisch klantvragen beantwoordt, 24/7 beschikbaar is, menselijk en vriendelijk overkomt. Het verlaagt werkdruk en verhoogt klanttevredenheid.

Schrijf in een toegankelijke, aantrekkelijke en heldere stijl.
"""
    return CopyOutput(text=prompt)

copy_agent = Agent(
    name="CopywriterAgent",
    instructions=(
        "Schrijf overtuigende en toegankelijke marketingcontent volgens de gegeven richtlijnen. "
        "Houd het kort, duidelijk en passend bij Heyloha’s toon."
    ),
    model="gpt-4o-mini",
    tools=[write_copy],
    output_type=CopyOutput,
)

# Workflow
async def run_workflow():
    url_result = await Runner.run(ui_agent, input="") 
    url_input = url_result.final_output

    website_result = await Runner.run(scraper_agent, input=[{"role": "user", "content": url_input.url}])
    website_data = website_result.final_output

    insights_result = await Runner.run(analyst_agent, input=[{"role": "user", "content": website_data.text}])
    insights = insights_result.final_output

    campaigns_result = await Runner.run(campaign_agent, input=[{"role": "user", "content": insights.insights}])
    campaigns = campaigns_result.final_output

    copy_result = await Runner.run(copy_agent, input=[{"role": "user", "content": campaigns.ideas}])
    copy = copy_result.final_output

    print("\n--- COPY RESULTAAT ---\n")
    print(copy.text)

    with open("marketing_copy.txt", "w", encoding="utf-8") as f:
        f.write(copy.text)
    print("Resultaat opgeslagen in marketing_copy.txt")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_workflow())