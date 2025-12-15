from playwright.sync_api import sync_playwright
from twilio.rest import Client
import os

URL = "https://www.drytortugas.com/overnight-camping-reservations/"
TEST_MODE = True  # we will turn this off later

def send_sms(message):
    client = Client(
        os.environ["TWILIO_ACCOUNT_SID"],
        os.environ["TWILIO_AUTH_TOKEN"]
    )
    client.messages.create(
        body=message,
        from_=os.environ["TWILIO_FROM_NUMBER"],
        to=os.environ["TO_NUMBER"]
    )

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, timeout=60000)
    page.wait_for_timeout(3000)

    # click calendar forward several months to reach April
    for _ in range(6):
        page.click("button[aria-label*='Next']")
        page.wait_for_timeout(1500)

    if TEST_MODE:
        send_sms("✅ TEST SUCCESS: Dry Tortugas checker ran correctly.")
