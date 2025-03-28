import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Email config


# Product URLs
urls = {
    "Komplett": "https://www.komplett.no/search?q=Sapphire%20RX%209070%20XT",
    "Elkjøp": "https://www.elkjop.no/search?search=Sapphire%20RX%209070%20XT",
    "Dustin": "https://www.dustin.no/search/sapphire%20rx%209070%20xt"
}

headers = {
    'User-Agent': 'Mozilla/5.0'
}

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            print("📧 Email sent!")
    except Exception as e:
        print(f"⚠️ Failed to send email: {e}")

def check_stock():
    for store, url in
