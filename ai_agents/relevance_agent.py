# from agents import Agent, function_tool
# from pydantic import BaseModel

# class Article(BaseModel):
#     title: str
#     description: str
#     source_name: str | None = None  # optioneel
#     url: str | None = None          # optioneel

# @function_tool
# def is_relevant(article: Article) -> bool:
#     keywords = [
#         "klantenservice", "chatbot", "ai", "automatisering", "support",
#         "e-mail", "telefoon", "customer service", "digitalisering",
#         "reserveringen", "retour", "crm", "makelaar", "makelaardij",
#         "klanttevredenheid", "orderstatus", "callcenter", "webcare",
#         "servicedruk", "supportkosten", "self service", "werkdruk",
#         "customer experience", "klantvraag", "wachttijd", "efficiëntie"
#     ]
#     content = f"{article.title} {article.description} {article.source_name or ''}".lower()
#     return any(k in content for k in keywords)

# relevance_agent = Agent(
#     name="RelevanceAgent",
#     instructions=(
#         "Beoordeel of dit nieuwsartikel relevant is voor een blog over klantcontact, werkdruk, digitalisering of slimme bedrijfsvoering. "
#         "Kijk breder dan alleen AI of chatbots. Denk ook aan trends, technologie, personeelstekorten of veranderend klantgedrag. "
#         "Geef **true** als het enig raakvlak heeft. Geef **false** als het totaal niet bruikbaar is."
#     ),
#     model="gpt-4o-mini",
#     tools=[is_relevant],
# )


from agents import Agent, function_tool
from pydantic import BaseModel

class Article(BaseModel):
    title: str
    description: str
    source_name: str | None = None  # optioneel
    url: str | None = None          # optioneel

@function_tool
def is_relevant(article: Article) -> bool:
    """Laat het model zelf inschatten of het artikel raakvlakken heeft met klantcontact of slimme bedrijfsvoering."""
    # Geen keyword-matching meer, AI bepaalt op basis van inhoud
    return "Laat het model bepalen"

relevance_agent = Agent(
    name="RelevanceAgent",
    instructions=(
        "Bepaal of het artikel relevant is voor een creatieve blog over klantcontact, werkdruk, digitalisering, personeelstekort of slimme bedrijfsvoering. "
        "Gebruik je creatief denkvermogen. Kijk niet alleen naar termen als 'AI' of 'chatbot', maar naar wat eronder ligt: trends in gedrag, technologie, communicatie of werk. "
        "Verbindingen leggen mag – als het haakjes heeft met klantvragen, efficiëntie of toekomst van werk, is het bruikbaar. "
        "Geef **true** als er enige relevantie is. Geef **false** als het echt totaal geen bruikbare haakjes heeft."
    ),
    model="gpt-4o-mini",
    tools=[is_relevant],
)
