import os
import smtplib
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright
from datetime import datetime
import time

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

def check_availability():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S CST")
    print(f"Checking Dry Tortugas availability at {now_str}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL, timeout=60000)
            page.wait_for_timeout(5000)
            body_text = page.inner_text("body")

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

            browser.close()

    except Exception as e:
        send_email(
            f"❌ Dry Tortugas Script Error ({now_str})",
            str(e)
        )
        print(f"Error: {e}")

# ===========================
# Main loop: run every hour
# ===========================
if __name__ == "__main__":
    while True:
        check_availability()
        print("Sleeping for 1 hour...")
        time.sleep(3600)  # sleep for 1 hour
