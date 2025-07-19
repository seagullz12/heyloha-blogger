import asyncio
from agents import Runner
from ai_agents.orchestrator_agent import orchestrator_agent
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText

from flask import Flask

app = Flask(__name__)

if not os.getenv("GOOGLE_MAIL_PW"):
    print("ERROR: Missing GOOGLE_MAIL_PW environment variable!")

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("ERROR: Missing OPENAI_API_KEY environment variable!")

if not os.getenv("GOOGLE_MAIL_PW") or not os.getenv("OPENAI_API_KEY"):
    print("ERROR: Missing environment variables. Stop.")
    exit(1)

# Email configuratie
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

async def main():
    prompt = (
        "Fetch recent news "
        "Filter the news relevant to Heyloha.ai, then generate a blog post"
    )
    result = await Runner.run(orchestrator_agent, prompt, context={})
    print("Final result:", result)

    blog_text = None
    blog_html = None

    if result.final_output:
        blog_text = result.final_output.text
        blog_html = result.final_output.html

    else:
        print("Geen output ontvangen.")

    if blog_text:
        os.makedirs("blogs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blogs/blog_{timestamp}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(blog_text)

    if blog_html:
        stuur_email(blog_html)
    else:
        print("Geen HTML-content ontvangen om te mailen.")

@app.route("/", methods=["GET", "POST"])
def run_task():
    asyncio.run(main())
    return "Taak uitgevoerd."

if __name__ == "__main__":
    # Start Flask app op poort 8080, vereist door Cloud Run
    app.run(host="0.0.0.0", port=8080)