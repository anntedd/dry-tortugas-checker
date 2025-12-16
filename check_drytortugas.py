import os
import smtplib
import time
import random
from email.mime.text import MIMEText
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

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
            page.goto(URL)
            page.wait_for_timeout(5000)  # wait for JS to render
            body_text = page.inner_text("body")

            if TARGET_DATE in body_text:
                send_email(
                    f"Dry Tortugas Alert: {TARGET_DATE} Available! ({now_str})",
                    f"✅ {TARGET_DATE} is now available for booking. Checked at {now_str}"
                )
            else:
                send_email(
                    f"Dry Tortugas Update: {TARGET_DATE} Not Available ({now_str})",
                    f"❌ {TARGET_DATE} is not available yet. Checked at {now_str}"
                )

            browser.close()

    except Exception as e:
        send_email(
            f"Dry Tortugas Script Error ({now_str})",
            f"Something went wrong:\n{e}"
        )
        raise

# ===========================
# Main loop: random minute each hour
# ===========================
# Run the first check immediately
check_availability()

while True:
    now = datetime.now()
    # Pick a random minute (0–59) for next run
    random_minute = random.randint(0, 59)
    # Next run = next hour at the random minute
    next_run = (now + timedelta(hours=1)).replace(minute=random_minute, second=0, microsecond=0)
    sleep_seconds = (next_run - now).total_seconds()
    print(f"Sleeping {sleep_seconds} seconds until next check at {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(sleep_seconds)
    check_availability()
