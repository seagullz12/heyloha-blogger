import smtplib
from email.mime.text import MIMEText
import os
from bs4 import BeautifulSoup

EMAIL_SENDER = "stefanhoogers@gmail.com"
EMAIL_PASSWORD = os.getenv("GOOGLE_MAIL_PW")
EMAIL_RECEIVER = "stefanhoogers@gmail.com"
DEFAULT_SUBJECT = "Je nieuwste blog van Heyloha"

def extract_title_from_html(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    h1 = soup.find("h1")
    if h1 and h1.text.strip():
        return h1.text.strip()
    return DEFAULT_SUBJECT

def send_email(html_content: str, ontvanger: str = EMAIL_RECEIVER):
    subject = extract_title_from_html(html_content)
    msg = MIMEText(html_content, "html", "utf-8")
    msg["Subject"] = "Heyloha Blog | " + subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = ontvanger

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"E-mail verzonden naar {ontvanger} met onderwerp: {subject}")
    except Exception as e:
        print(f"Fout bij e-mail verzenden: {e}")