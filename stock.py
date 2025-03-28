import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Email config
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password_here"
EMAIL_RECEIVER = "your_email@gmail.com"

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
    for store, url in urls.items():
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text().lower()

            if "ikke på lager" in text or "utsolgt" in text:
                print(f"[{store}] ❌ Not in stock.")
            elif "på lager" in text or "legge i handlekurv" in text:
                print(f"[{store}] ✅ Possibly in stock! Check here: {url}")
                send_email(
                    f"Stock Alert: {store}",
                    f"The Sapphire RX 9070 XT might be in stock at {store}!\nCheck here: {url}"
                )
            else:
                print(f"[{store}] 🤔 Status unclear. Check manually: {url}")

        except Exception as e:
            print(f"[{store}] ⚠️ Error checking {store}: {e}")

if __name__ == "__main__":
    while True:
        print("🔍 Checking stock status...")
        check_stock()
        print("⏱️ Waiting 5 minutes before next check...\n")
        time.sleep(300)  # Check every 5 mins
