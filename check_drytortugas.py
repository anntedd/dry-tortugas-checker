import os
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
TARGET_MONTH = "April 2026"

try:
    # Setup headless Chrome
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(DRY_TORT_URL)

    wait = WebDriverWait(driver, 15)

    # Wait for the calendar to appear
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-cy='calendar']")))

    # Navigate to the correct month
    month_header = driver.find_element(By.CSS_SELECTOR, "div[data-cy='month-info']").text
    while month_header != TARGET_MONTH:
        driver.find_element(By.CSS_SELECTOR, "button[data-cy='month-navigation-right']").click()
        time.sleep(1)  # small wait for animation
        month_header = driver.find_element(By.CSS_SELECTOR, "div[data-cy='month-info']").text

    # Collect available days (buttons that are not disabled)
    available_dates = []
    for btn in driver.find_elements(By.CSS_SELECTOR, "button[data-cy='calendar-day']:not([disabled])"):
        day_number = btn.find_element(By.CSS_SELECTOR, "span[data-cy='day-number']").text
        # Format date as YYYY-MM-DD
        available_dates.append(f"2026-04-{int(day_number):02d}")

    if TARGET_DATE in available_dates:
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
