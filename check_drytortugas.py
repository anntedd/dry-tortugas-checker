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

# Target date
TARGET_DATE = "2026-04-09"

try:
    # Setup headless Chrome
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(DRY_TORT_URL)
    
    # Wait for page / JavaScript to load (adjust if needed)
    time.sleep(5)

    # The site loads availability in a div with class 'availability' or similar
    # Adjust selector based on what you see in the browser DevTools
    availability_text = driver.find_element(By.TAG_NAME, "body").text

    if TARGET_DATE in availability_text:
        send_email(
            f"Dry Tortugas Alert: {TARGET_DATE} Available!",
            f"✅ {TARGET_DATE} for 1 night is now available. Go book it!"
        )
    else:
        print(f"{TARGET_DATE} is not available yet.")

    driver.quit()

except Exception as e:
    send_email(
        "Dry Tortugas Script Error",
        f"Something went wrong when checking availability:\n{e}"
    )
    raise
