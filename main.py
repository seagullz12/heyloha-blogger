from flask import Flask, request
import asyncio
from ai_agents.news_agent import news_agent
from ai_agents.relevance_agent import relevance_agent
from ai_agents.blog_agent import blog_agent
from ai_agents.redactie_agent import redactie_agent
from ai_agents.html_agent import html_agent
from agents import Runner, trace
from datetime import datetime
import os
from email_sender import send_email
import logging
import glob

logger = logging.getLogger("agents")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    # Console output
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Log naar bestand
    file_handler = logging.FileHandler("agents.log", mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def read_previous_blogs(n=5):
    files = sorted(glob.glob("blogs/*.md"), reverse=True)[:n]
    texts = []
    for f in files:
        with open(f, encoding="utf-8") as file:
            texts.append(file.read())
    return "\n\n---\n\n".join(texts)

heyloha_info = (
    """
# Heyloha.ai: Automatiseer en Optimaliseer Je Klantcontact

Heyloha.ai is een geavanceerd AI-platform dat bedrijven helpt hun klantcontact te automatiseren. Het platform is ontworpen om veelvoorkomende klantvragen efficiënt af te handelen via diverse kanalen zoals chat, e-mail, telefonie en WhatsApp. Hierdoor kunnen bedrijven tot 80% van hun inkomende vragen foutloos en in hun eigen, specifieke tone of voice beantwoorden, wat resulteert in geen wachttijden voor klanten en minder druk op het personeel.

## Wat Heyloha.ai Biedt:

* **Multikanaal Ondersteuning:** Antwoord op klantvragen via chat, e-mail, telefoon en WhatsApp.
* **Realtime AI-spraakassistent:** Handelt inkomende telefoontjes af met een natuurlijke stem.
* **E-mail Automatisering:** Leest de inbox en stelt conceptantwoorden op voor inkomende e-mails.
* **Slimme Overdracht (Handoff):** Bij complexe vragen wordt het gesprek naadloos overgedragen aan een menselijke medewerker.
* **Uitgebreide Realtime Rapportage:** Biedt diepgaand inzicht in de meest gestelde vragen, klantbehoeften en de prestaties van de AI.

## Voordelen voor Jouw Bedrijf:

* **Verhoogde Klanttevredenheid:** Minder wachttijd voor klanten zorgt voor een betere ervaring.
* **Lagere Werkdruk & Kosten:** Automatisering reduceert de belasting op personeel en de operationele kosten.
* **Meer Conversie, Minder Stress:** Efficiënte afhandeling leidt tot betere resultaten en minder stress voor je team.
* **Volledig Overzicht:** Via een overzichtelijke inbox heb je altijd volledig zicht op alle klantgesprekken.

## Slim Omgaan met Pieken en Dalen in Klantcontact:

Veel bedrijven kampen met schommelingen in klantcontact:
* **Drukte:** Tijdens piekperiodes ontstaan lange wachtrijen en raakt personeel overbelast.
* **Rust:** In rustige tijden is er sprake van overcapaciteit en zijn medewerkers wellicht minder efficiënt.
* **Afleiding:** Medewerkers worden vaak afgeleid door herhaalde telefoontjes, e-mails en chats, wat de kosten opdrijft en de focus verlaagt.

Heyloha.ai biedt een uniforme eerstelijns communicatieoplossing die voorspelbare vragen automatisch afhandelt. Hierdoor kunnen je medewerkers zich richten op uitzonderingen en complexere kwesties. Dankzij de slimme overdracht tussen AI en menselijke medewerkers blijven wachttijden kort en de werkdruk laag. Heyloha schaalt moeiteloos mee met pieken en dalen in het klantcontact, zodat klanten altijd snel en correct antwoord krijgen, ongeacht het kanaal.

Met Heyloha.ai transformeer je klantcontact van een kostenpost naar een **groeimotor** voor je bedrijf.
"""
) 

app = Flask(__name__)

async def run_blog_flow(query: str, ontvanger: str = None):
    # Gebruik standaardwaarde als query leeg of None is
    if not query:
        query = "klantenservice"
    previous_blogs_text = read_previous_blogs()
    context = {
        "heyloha_info": heyloha_info,
        "previous_blogs": previous_blogs_text,
    }
    with trace("Nieuwsblog flow"):
        print(f"Calling NewsAgent with query: {query}")
        news_result = await Runner.run(
            news_agent,
            input=[{"role": "system", "content": f"Fetch news about: {query}"}],
            context=context,
        )
        articles = news_result.final_output or []
        print(f"NewsAgent: {len(articles)} articles opgehaald.")

        relevant_articles = []
        print("Checking relevance with RelevanceAgent...")
        for article in articles:
            rel_result = await Runner.run(
                relevance_agent,
                input=[{"role": "user", "content": str(article.model_dump())}],
                context=context
            )
            print(f"- {article.title} → relevant: {rel_result.final_output}")
            if rel_result.final_output:
                relevant_articles.append(article)

        print(f"RelevanceAgent: {len(relevant_articles)} relevante artikelen.")

        if not relevant_articles:
            print("Geen relevante artikelen gevonden. Stoppen.")
            return "Geen relevante artikelen gevonden."

        print("Calling BlogAgent...")
        articles_dicts = [a.model_dump() for a in relevant_articles]
        content = ""
        for a in articles_dicts:
            content += f"- {a['title']}: {a['description'].strip()} (Bron: {a.get('source_name', '')})\n"

        input_for_blog = [
            {"role": "system", "content": "Je bent een blog schrijver."},
            {"role": "user", "content": content}
        ]

        blog_result = await Runner.run(blog_agent, input=input_for_blog, context=context)
        if blog_result.final_output:
            blog_text = blog_result.final_output.text 
        else:
            blog_text = ""
        print(f"Blogtekst lengte: {len(blog_text)}")

        if not blog_text:
            print("Geen blogtekst gegenereerd. Stoppen.")
            return "Geen blogtekst gegenereerd."

        print("Calling RedactieAgent...")
        redactie_result = await Runner.run(redactie_agent, input=blog_text, context=context)
        if redactie_result.final_output:
            verbeterde_blog_text = redactie_result.final_output.improved_text
        else:
            verbeterde_blog_text = blog_text 
        print(f"Verbeterde blogtekst lengte: {len(verbeterde_blog_text)}")

        print("Calling HtmlAgent...")
        html_result = await Runner.run(html_agent, input=verbeterde_blog_text, context=context)
        blog_html = html_result.final_output.html if html_result.final_output else ""
        print(f"HTML lengte: {len(blog_html)}")

        if not blog_html:
            print("Geen HTML gegenereerd. Stoppen.")
            return "Geen HTML gegenereerd."

        # Opslaan
        os.makedirs("blogs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blogs/blog_{timestamp}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(verbeterde_blog_text)
        print(f"Blog opgeslagen in {filename}")

        # E-mail sturen met blog
        if not ontvanger:
            ontvanger = "stefanhoogers@gmail.com"
        send_email(blog_html, ontvanger)

        return "Blog succesvol gegenereerd en verzonden."

@app.route("/generate_blog", methods=["GET"])
def generate_blog_route():
    query = request.args.get("query") # optioneel
    ontvanger = request.args.get("email")  # optioneel
    if not query:
        query = "customer service"

    print(f"Received query param: {query}, email: {ontvanger}")
    result = asyncio.run(run_blog_flow(query, ontvanger))
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)