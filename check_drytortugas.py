import os
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
    print("Email sent successfully!")

# ===========================
# Dry Tortugas availability check
# ===========================
DRY_TORT_URL = "https://www.drytortugas.com/overnight-camping-reservations/"
TARGET_DATE = "2026-04-09"

try:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(DRY_TORT_URL)
    
    time.sleep(5)  # wait for JS to render

    body_text = driver.find_element(By.TAG_NAME, "body").text

    # ---- TWEAK: Always send an email ----
    if TARGET_DATE in body_text:
        subject = f"Dry Tortugas Alert: {TARGET_DATE} Available!"
        body = f"✅ {TARGET_DATE} for 1 night is now available. Go book it!"
    else:
        subject = f"Dry Tortugas Alert: {TARGET_DATE} NOT Available (TEST)"
        body = f"❌ {TARGET_DATE} is not available yet. This is a test email."

    send_email(subject, body)
    driver.quit()

except Exception as e:
    send_email(
        "Dry Tortugas Script Error",
        f"Something went wrong when checking availability:\n{e}"
    )
    raise
