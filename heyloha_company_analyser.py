from agents import Agent, function_tool, ModelSettings
from agents import Runner
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

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
        "Vraag de gebruiker om een volledige, geldige URL van de website die geanalyseerd moet worden."
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
            soup = BeautifulSoup(r.text, "html.parser")
            # Haal alle tekst uit <p>, <h1-h6>, <li>, <span> en andere relevante tags
            texts = []
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span', 'div']):
                if tag.string and tag.string.strip():
                    texts.append(tag.get_text(separator=" ", strip=True))
            # Combineer en beperk tot max 4000 chars
            content = "\n".join(texts)[:4000]
            return WebsiteData(text=content)
        else:
            return WebsiteData(text=f"Error {r.status_code} bij ophalen van {url_input.url}")
    except Exception as e:
        return WebsiteData(text=f"Fout bij ophalen: {str(e)}")

scraper_agent = Agent(
    name="WebsiteScraperAgent",
    instructions=(
        "Haal de tekstuele inhoud van de opgegeven URL op. Focus op de belangrijkste pagina-inhoud, "
        "zoals product- of dienstomschrijvingen en bedrijfsinformatie."
    ),
    model="gpt-4o-mini",
    tools=[scrape_site],
    output_type=WebsiteData,
)

# Stap 3: Analyseer hoe Heyloha past
class FitAnalysis(BaseModel):
    analysis: str

@function_tool
def analyze_fit(data: WebsiteData) -> FitAnalysis:
    prompt = f"""
Je krijgt de volgende webpagina-inhoud (max 4000 tekens):

{data.text[:4000]}

Analyseer kort en duidelijk:
1. Wat voor soort bedrijf of organisatie is dit?
2. Wat zijn de belangrijkste klantcontactbehoeften of uitdagingen die uit de tekst blijken?
3. Hoe kan Heyloha (AI-klantcontactoplossing die 24/7 werkt, vriendelijk en menselijk is, werkdruk verlaagt en klanttevredenheid verhoogt) waarde toevoegen aan dit bedrijf?
4. Geef een duidelijke conclusie over hoe goed Heyloha past bij dit bedrijf, met argumenten.

Schrijf in eenvoudige en duidelijke taal.
"""
    return FitAnalysis(analysis=prompt)

fit_agent = Agent(
    name="FitAnalysisAgent",
    instructions=(
        "Beoordeel hoe goed Heyloha past bij het bedrijf gebaseerd op de webinhoud. "
        "Focus op klantcontact uitdagingen en waarde die Heyloha kan bieden."
    ),
    model="gpt-4o-mini",
    tools=[analyze_fit],
    output_type=FitAnalysis,
)

# Workflow
async def run_workflow():
    url_result = await Runner.run(ui_agent, input="")
    url_input = url_result.final_output  # URLInput object

    website_result = await Runner.run(scraper_agent, input=[{"role": "user", "content": url_input.url}])
    website_data = website_result.final_output  # WebsiteData object

    fit_result = await Runner.run(fit_agent, input=[{"role": "user", "content": website_data.text}])
    fit_analysis = fit_result.final_output  # FitAnalysis object

    print("\n--- HEYLOHA MATCH ANALYSE ---\n")
    print(fit_analysis.analysis)

    with open("heyloha_fit_analysis.txt", "w", encoding="utf-8") as f:
        f.write(fit_analysis.analysis)
    print("Analyse opgeslagen in heyloha_fit_analysis.txt")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_workflow())