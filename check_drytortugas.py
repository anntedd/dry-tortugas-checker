from playwright.sync_api import sync_playwright
import os
import smtplib
from email.mime.text import MIMEText

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
TARGET_DATE = "2026-04-09"
URL = "https://www.drytortugas.com/overnight-camping-reservations/"

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL)
    page.wait_for_timeout(5000)  # wait for JS to load

    body_text = page.inner_text("body")
    if TARGET_DATE in body_text:
        send_email(f"Dry Tortugas Alert: {TARGET_DATE} Available!", f"{TARGET_DATE} is now available!")
    else:
        print(f"{TARGET_DATE} not available yet.")

    browser.close()
