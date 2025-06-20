from agno.agent import Agent
from agno.tools import Tool
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

# Eczane verisi çekecek tool
class NobetciEczaneTool(Tool):
    name = "nobetci_eczane_cek" #tools.py dosyasındaki fonksiyon 
    description = "Belirtilen il ve ilçedeki nöbetçi eczaneleri çeker."

    def run(self, il: str, ilce: str):
        url = f"https://www.eczaneler.gen.tr/nobetci-{ilce.lower()}-{il.lower()}-eczaneleri.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        eczaneler = []
        for card in soup.select('.eczane-card'):
            ad = card.select_one('.eczane-title').text.strip()
            adres = card.select_one('.eczane-adres').text.strip()
            tel = card.select_one('.eczane-tel').text.strip()
            eczaneler.append(f"{ad}\nAdres: {adres}\nTel: {tel}\n")
        return '\n---\n'.join(eczaneler)

class MailGonderTool(Tool):
    name = "mail_gonder"
    description = "Belirtilen e-posta adresine Gmail ile içerik gönderir."

    def run(self, to: str, subject: str, content: str):
        user = os.getenv("GMAIL_USER")
        password = os.getenv("GMAIL_PASSWORD")
        msg = MIMEText(content)
        msg["Subject"] = subject
        msg["From"] = user
        msg["To"] = to
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(user, [to], msg.as_string())
        return "E-posta gönderildi."

