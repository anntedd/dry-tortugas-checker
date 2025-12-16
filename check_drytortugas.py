import os
import smtplib
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright
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
    print("Email sent successfully!")

# ===========================
# Dry Tortugas availability check
# ===========================
TARGET_DATE = "2026-04-09"
URL = "https://www.drytortugas.com/overnight-camping-reservations/"

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)
        page.wait_for_timeout(5000)  # wait for JS to render

        body_text = page.inner_text("body")

        if TARGET_DATE in body_text:
            send_email(
                f"Dry Tortugas Alert: {TARGET_DATE} Available!",
                f"✅ {TARGET_DATE} is now available for booking. Go check it!"
            )
        else:
            send_email(
                f"Dry Tortugas Update: {TARGET_DATE} Not Available",
                f"❌ {TARGET_DATE} is not available yet."
            )

        browser.close()

except Exception as e:
    send_email(
        "Dry Tortugas Script Error",
        f"Something went wrong:\n{e}"
    )
    raise
