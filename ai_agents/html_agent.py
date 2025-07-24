from typing import TypedDict
from agents import Agent, function_tool
from pydantic import BaseModel
import re

class HtmlOutput(BaseModel):
    html: str

def blog_to_html(blog_text: str) -> HtmlOutput:
    # Heyloha Brand Guide Styling (based on Heyloha brand guide V2.pdf)
    # Kleuren:
    # Heyloha Green: #4AAB9A (Primair voor koppen)
    # Aloha Coral: #EF7D62 (Links, bolletjes)
    # Sunbeam Yellow: #FCC120 (Accentkleur - voor hover, maar dat is complex met inline CSS voor e-mail)
    # Deep Charcoal: #333333 (Bodytekst)
    # Sand White: #FFFCF3 (Achtergronden)

    # Typografie: Roboto (Alle koppen en bodyteksten)

    # Base styling to be applied inline
    body_style = "font-family: 'Roboto', sans-serif; color: #333333; background-color: #FFFCF3; line-height: 1.6; margin: 0; padding: 0;"
    container_style = "max-width: 800px; margin: 20px auto; padding: 25px; background-color: #FFFFFF; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.05);"
    h_style = "font-family: 'Roboto', sans-serif; color: #4AAB9A; margin-top: 1.5em; margin-bottom: 0.8em; line-height: 1.2;"
    p_style = "font-family: 'Roboto', sans-serif; color: #333333; margin-bottom: 1em;"
    a_style = "font-family: 'Roboto', sans-serif; color: #EF7D62; text-decoration: none; font-weight: bold;"
    ul_style = "font-family: 'Roboto', sans-serif; color: #333333; list-style-type: none; padding-left: 0; margin-bottom: 1em;"
    li_style = "font-family: 'Roboto', sans-serif; color: #333333;" # li text color

    html_content = blog_text.strip()

    # 1. Convert Markdown links to HTML links FIRST with inline style
    html_content = re.sub(
        r'\[(.*?)\]\((https?://[^\s)]+)\)',
        lambda m: f'<a href="{m.group(2)}" style="{a_style}">{m.group(1)}</a>',
        html_content,
    )
    # Ensure raw heyloha.ai URLs are also linked with style
    html_content = re.sub(
        r'https://heyloha\.ai',
        f'<a href="https://heyloha.ai" style="{a_style}">heyloha.ai</a>',
        html_content,
    )

    # 2. Convert Markdown headings to HTML headings with inline styles
    html_content = re.sub(r'^\s*#\s+(.*)$', r'<h1 style="' + h_style + r'font-size: 2.2em;">\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^\s*##\s+(.*)$', r'<h2 style="' + h_style + r'font-size: 1.8em;">\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^\s*###\s+(.*)$', r'<h3 style="' + h_style + r'font-size: 1.4em;">\1</h3>', html_content, flags=re.MULTILINE)

    # 3. Convert bold and italic markdown with inline styles
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong style="font-weight: bold;">\1</strong>', html_content) # Bold
    html_content = re.sub(r'\*(.*?)\*', r'<em style="font-style: italic;">\1</em>', html_content)   # Italic

    # 4. Convert markdown list items (- Item or * Item) to HTML list items with inline styles
    lines = html_content.split('\n')
    processed_lines = []
    in_list = False
    for line in lines:
        stripped_line = line.strip()
        if re.match(r'^[\-\*]\s+', stripped_line):
            if not in_list:
                processed_lines.append(f'<ul style="{ul_style}">')
                in_list = True
            item_content = re.sub(r'^[\-\*]\s*(.*)$', r'\1', stripped_line)
            processed_lines.append(f'<li style="{li_style}"><span style="color: #4AAB9A;">•</span> {item_content}</li>')
        else:
            if in_list:
                processed_lines.append('</ul>')
                in_list = False
            processed_lines.append(line)
    if in_list:
        processed_lines.append('</ul>')
    html_content = "\n".join(processed_lines)

    # 5. Replace multiple newlines with paragraph tags and single newlines with <br>, but avoid inside blocks
    # Split by double newlines first to paragraphs
    paragraphs = re.split(r'\n{2,}', html_content)
    html_content = ''
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # If para starts with a block tag, just append
        if re.match(r'^<(h[1-3]|ul|ol|div|p|li|table|blockquote)', para):
            html_content += para
        else:
            # replace single newlines with <br>
            para = para.replace('\n', '<br>')
            html_content += f'<p style="{p_style}">{para}</p>'

    # 6. Clean up stray <br> tags after block elements or before block ends
    html_content = re.sub(r'(</h\d>|</p>|</ul>|</li>)\s*<br\s*/?>', r'\1', html_content)
    html_content = re.sub(r'<br\s*/?>\s*(</p>|</ul>|</li>)', r'\1', html_content)
    # Reduce multiple <br> to one
    html_content = re.sub(r'(<br\s*/?>){2,}', '<br/>', html_content)

    # 7. Add logo at top with margin
    logo_html = """
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://www.heyloha.ai/wp-content/uploads/2025/05/Heyloha-3.png" alt="Heyloha Logo" style="max-width: 200px; height: auto;">
    </div>
    """

    # Final HTML structure with embedded styles and logo
    html = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="nl">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Heyloha Blog</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style type="text/css">
        body {{ {body_style} }}
        .blog-container {{ {container_style} }}
        h1, h2, h3 {{ {h_style} }}
        h1 {{ font-size: 2.2em; }}
        h2 {{ font-size: 1.8em; }}
        h3 {{ font-size: 1.4em; }}
        p {{ {p_style} }}
        a {{ {a_style} }}
        ul {{ {ul_style} }}
        li {{ {li_style} }}
        strong {{ font-weight: bold; }}
        em {{ font-style: italic; }}
    </style>
</head>
<body style="{body_style}">
    <div class="blog-container" style="{container_style}">
        {logo_html}
        {html_content}
    </div>
</body>
</html>
"""
    return HtmlOutput(html=html)

generate_html_tool = function_tool(blog_to_html)

html_agent = Agent(
    name="HtmlAgent",
    instructions=(
        "Converteer de gegeven blogtekst naar schone, goed gestructureerde HTML, die voldoet aan de Heyloha huisstijlrichtlijnen. "
        "Voeg bovenaan de HTML het Heyloha-logo toe als een afbeelding, gecentreerd met een marge van 20 pixels onder de afbeelding. "
        "Gebruik de URL: https://www.heyloha.ai/wp-content/uploads/2025/05/Heyloha-3.png "
        "Pas de HTML-stijlen (kleuren, lettertype, marges, etc.) **inline** toe op de HTML-elementen voor maximale compatibiliteit, met name voor e-mail. "
        "Gebruik paragrafen voor nieuwe secties, duidelijke koppen (H1, H2, H3) waar van toepassing, en opsommingstekens indien aanwezig. "
        "De HTML moet makkelijk leesbaar zijn en geschikt voor zowel e-mail als webpublicatie. "
        "Pas de Heyloha-merkstijl toe: gebruik het lettertype **Roboto** voor alle tekst. "
        "Kleuren moeten zorgvuldig worden toegepast: "
        "- **Heyloha Green (#4AAB9A)** voor koppen. "
        "- **Deep Charcoal (#333333)** voor de algemene tekst. "
        "- **Sand White (#FFFCF3)** als achtergrondkleur. "
        "- **Aloha Coral (#EF7D62)** voor links en als bullet points voor lijsten. "
        "Zorg voor een menselijke, heldere en vriendelijke uitstraling die past bij Heyloha's merkpersoonlijkheid. "
        "Zet links naar heyloha.ai om in correcte HTML-hyperlinks. "
        "Vervang speciale symbolen of markdown-achtige syntax in de input naar correcte HTML-elementen (bijv. `# Titel` naar `<h1>Titel</h1>`, `**vet**` naar `<strong>vet</strong>`, `- lijst` naar `<ul><li>lijst</li></ul>`)."
    ),
    model="gpt-4o-mini",
    tools=[generate_html_tool],
    output_type=HtmlOutput,
)