import asyncio
from typing import List, Optional
from pydantic import BaseModel
from agents import Agent, Runner, trace, function_tool
import os
import logging
import httpx
import re
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

logger = logging.getLogger("agents")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

EMAIL_SENDER = "stefanhoogers@gmail.com"
EMAIL_PASSWORD = os.getenv("GOOGLE_MAIL_PW")
EMAIL_RECEIVER = "stefanhoogers@gmail.com"
EMAIL_SUBJECT = "Je nieuwste blog van Heyloha"

def stuur_email(html_content: str):
    msg = MIMEText(html_content, "html", "utf-8")
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("E-mail verzonden.")
    except Exception as e:
        print(f"Fout bij e-mail verzenden: {e}")

class Article(BaseModel):
    title: str
    description: str
    source_name: Optional[str]
    source_id: Optional[str]
    published_at: Optional[str]
    url: Optional[str]

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return "-".join(text.strip().split())[:40]

@function_tool
def is_relevant(article: Article) -> bool:
    keywords = [
        "klantenservice", "chatbot", "ai", "automatisering", "support",
        "e-mail", "telefoon", "customer service", "digitalisering",
        "reserveringen", "retour", "crm", "makelaar", "makelaardij",
        "klanttevredenheid", "orderstatus", "callcenter", "webcare",
        "servicedruk", "supportkosten", "self service", "werkdruk",
        "customer experience", "klantvraag", "wachttijd", "efficiëntie"
    ]
    content = f"{article.title} {article.description} {article.source_name or ''}".lower()
    return any(k in content for k in keywords)

@function_tool
async def fetch_news(query: str = "technology") -> List[Article]:
    logger.info(f"Fetching news for query: {query}")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 5,
        "sortBy": "relevancy",
    }
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            articles = []
            for item in data.get("articles", []):
                articles.append(
                    Article(
                        title=item.get("title", "").strip(),
                        description=item.get("description") or "",
                        source_name=item.get("source", {}).get("name"),
                        source_id=item.get("source", {}).get("id"),
                        published_at=item.get("publishedAt"),
                        url=item.get("url"),
                    )
                )
            for a in articles:
                logger.info(f"Article: {a.title} | {a.url} | {a.description[:100]}...")
            return articles
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []

@function_tool
def generate_blog(articles: List[Article], previous_blogs: str = "", heyloha_info: str = "") -> str:
    artikelen_tekst = ""
    for article in articles:
        artikelen_tekst += (
            f"- {article.title}: {article.description.strip()} "
            f"(Bron: {article.source_name})\n"
        )
    prompt = (
        "Je krijgt deze achtergrond over Heyloha:\n"
        f"{heyloha_info}\n\n"
        "En deze eerdere blogs:\n"
        f"{previous_blogs}\n\n"
        "Schrijf een casual, makkelijk leesbare Nederlandstalige blog op basis van deze nieuwsartikelen. "
        "Maak er een vloeiend verhaal van, geen opsommingen. "
        "Vat kort samen, koppel trends aan klantcontact en eindig met Heyloha als slimme oplossing.\n\n"
        f"Nieuwsartikelen:\n{artikelen_tekst}\n\n"
        "Vermijd herhaling van onderwerpen die al in eerdere blogs zijn genoemd. "
        "Bedenk nieuwe invalshoeken en wees origineel."
    )
    return prompt

generate_blog_tool = generate_blog

def blog_to_html(blog_text: str) -> str:
    html = blog_text.replace("\n\n", "</p><p>").replace("\n", "<br>")
    html = html.replace("📰", "<h3>Nieuwsartikel:</h3>")
    return f"<html><body><p>{html}</p></body></html>"

generate_html_tool = function_tool(blog_to_html)

news_agent = Agent(
    name="NewsAgent",
    instructions="Haal maximaal 5 recente Engelstalige nieuwsartikelen op over het onderwerp dat wordt opgegeven.",
    model="gpt-4o-mini",
    tools=[fetch_news],
    output_type=List[Article],
)

relevance_agent = Agent(
    name="RelevanceAgent",
    instructions="Beoordeel of het nieuwsartikel relevant is voor een blog over klantcontact, werkdruk, digitalisering, of slimme bedrijfsvoering.",
    model="gpt-4o-mini",
    tools=[is_relevant],
)

blog_agent = Agent(
    name="BlogAgent",
    instructions="Schrijf een casual Nederlandstalige blog over de nieuwsartikelen, met bronvermelding en zonder opsommingen.",
    model="gpt-4o-mini",
    tools=[generate_blog_tool],
)

html_agent = Agent(
    name="HtmlAgent",
    instructions="Zet de gegeven blogtekst om in overzichtelijke HTML met paragrafen.",
    model="gpt-4o-mini",
    tools=[generate_html_tool],
    output_type=str,
)

async def main():
    context = {
        "heyloha_info": "Heyloha helpt bedrijven met klantcontact efficiënter te maken.",
        "previous_blogs": "",  # Of vul met eerdere blogs
    }

    with trace("Nieuwsblog flow"):
        print("Fetching news...")
        news_result = await Runner.run(news_agent, input=[{"role": "system", "content": "Fetch recent news"}], context=context)
        articles = news_result.final_output or []
        print(f"{len(articles)} artikelen opgehaald.")

        relevant_articles = []
        print("Checken relevantie...")
        for article in articles:
            rel_result = await Runner.run(
                relevance_agent,
                input=[{"role": "user", "content": str(article.model_dump())}],
                context=context,
            )
            print(f"- {article.title} → relevant: {rel_result.final_output}")
            if rel_result.final_output:
                relevant_articles.append(article)

        print(f"{len(relevant_articles)} relevante artikelen.")

        if not relevant_articles:
            print("Geen relevante artikelen. Stoppen.")
            return

        print("Blog genereren...")
        articles_dicts = [a.model_dump() for a in relevant_articles]
        content = ""
        for a in articles_dicts:
            content += f"- {a['title']}: {a['description'].strip()} (Bron: {a.get('source_name', '')})\n"

        input_for_blog = [
            {"role": "system", "content": "Je bent een blog schrijver."},
            {"role": "user", "content": content},
        ]

        blog_result = await Runner.run(blog_agent, input=input_for_blog, context=context)
        if blog_result.final_output:
            blog_text = blog_result.final_output.text 
        else:
            blog_text = ""

        print(f"Blogtekst lengte: {len(blog_text)}")
        if not blog_text:
            print("Geen blogtekst gegenereerd. Stoppen.")
            return

        print("HTML genereren...")
        html_result = await Runner.run(html_agent, input=blog_text, context=context)
        blog_html = html_result.final_output or ""
        print(f"HTML lengte: {len(blog_html)}")

        if not blog_html:
            print("Geen HTML gegenereerd. Stoppen.")
            return

        # Opslaan
        os.makedirs("blogs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blogs/blog_{timestamp}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(blog_text)
        print(f"Blog opgeslagen in {filename}")

        # E-mail sturen
        stuur_email(blog_html)

if __name__ == "__main__":
    asyncio.run(main())