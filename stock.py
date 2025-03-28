import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Email config
EMAIL_SENDER = "your_email@gmail.com"         # ← Your Gmail
EMAIL_PASSWORD = "your_app_password_here"     # ← Your Gmail app password
EMAIL_RECEIVER = "your_email@gmail.com"       # ← Where alerts are sent

# URLs to monitor
urls = {
    "Komplett": "https://www.komplett.no/search?q=Sapphire%20RX%209070%20XT",
    "Elkjøp": "https://www.elkjop.no/search?search=Sapphire%20RX%209070%20XT",
    "Dustin": "https://www.dustin.no/search/sapphire%20rx%209070%20xt",
    "Proshop": "https://www.proshop.no/?s=Sapphire+RX+9070+XT",
    "ComputerSalg": "https://www.computersalg.no/search?s=Sapphire+RX+9070+XT"
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

            print(f"\n--- Checking {store} ---")

            # OUT OF STOCK indicators (site-specific keywords)
            out_keywords = [
                "overvåk lagersaldo",
                "ukjent leveringsdato",
                "ikke på lager",
                "ikke tilgjengelig",
                "midlertidig utsolgt",
                "ikke på lager online",
                "forudbestil",  # Danish for preorder (ComputerSalg)
                "bestillingsvare",
                "udsolgt"
            ]

            # IN STOCK indicators (site-specific keywords)
            in_keywords = [
                "legg i handlekurv",
                "på lager",
                "på lager i nettbutikk",
                "klar til levering",
                "på fjernlager",
                "add to basket",
                "add to cart",
                "på lager (1-2 hverdage)"
            ]

            if any(keyword in text for keyword in out_keywords):
                print(f"[{store}] ❌ Not in stock.")
            elif any(keyword in text for keyword in in_keywords):
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
        time.sleep(300)
