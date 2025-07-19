from agents import Agent, function_tool

def blog_to_html(blog_text: str) -> str:
    # Simpele conversie: nieuwe paragrafen, kopjes en opsommingstekens
    html = blog_text.replace("\n\n", "</p><p>")
    html = html.replace("\n", "<br>")
    # Bijvoorbeeld 📰 vervangen door <h3>
    html = html.replace("📰", "<h3>Nieuwsartikel:</h3>")
    html = f"<html><body><p>{html}</p></body></html>"
    return html

generate_html_tool = function_tool(blog_to_html)

html_agent = Agent(
    name="HtmlAgent",
    instructions=(
        "Zet de gegeven blogtekst om in overzichtelijke HTML. Gebruik paragrafen, kopjes en zorg voor leesbaarheid."
    ),
    model="ogpt-4o-mini",
    tools=[generate_html_tool],
)
