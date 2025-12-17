import os
import smtplib
import requests
from email.mime.text import MIMEText
from datetime import datetime

# ===========================
# Email setup
# ===========================
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

    print(f"Email sent: {subject}")

# ===========================
# Dry Tortugas availability check
# ===========================
TARGET_DATE = "2026-04-09"
URL = "https://www.drytortugas.com/overnight-camping-reservations/"

# Browser-like headers
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/143.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def check_availability():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S CST")
    print(f"Checking Dry Tortugas availability at {now_str}")

    try:
        response = requests.get(URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        body_text = response.text

        if TARGET_DATE in body_text:
            send_email(
                f"🔥 Dry Tortugas AVAILABLE: {TARGET_DATE} ({now_str})",
                f"✅ {TARGET_DATE} is now available.\nChecked at {now_str}\n\n{URL}"
            )
        else:
            send_email(
                f"Dry Tortugas Check OK ({now_str})",
                f"❌ {TARGET_DATE} not available yet.\nChecked at {now_str}"
            )

    except requests.exceptions.HTTPError as e:
        send_email(
            f"❌ Dry Tortugas HTTP Error ({now_str})",
            f"HTTP error occurred:\n{e}"
        )
        print(f"HTTP Error: {e}")
    except Exception as e:
        send_email(
            f"❌ Dry Tortugas Script Error ({now_str})",
            str(e)
        )
        print(f"Error: {e}")

if __name__ == "__main__":
    check_availability()
