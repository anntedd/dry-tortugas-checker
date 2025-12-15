# check_drytortugas.py
import requests
import smtplib
from email.message import EmailMessage
from playwright.sync_api import sync_playwright
import time

# ----------------------
# CONFIG
# ----------------------
EMAIL_USER = "your_email@gmail.com"      # your email
EMAIL_PASS = "your_app_password"         # app password if using Gmail
TO_EMAIL = "your_email@gmail.com"        # can be same as your email
DATE_TO_CHECK = "2025-12-15"             # change to the date you want
CHECK_URL = "https://www.drytortugas.com/overnight-camping-reservations/"  # main page

# ----------------------
# STEP 1: Load page and select options
# ----------------------
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False so you can see it
    page = browser.new_page()
    page.goto(CHECK_URL)
    
    # Pause so you can inspect elements and find real selectors
    page.pause()
    
    # ---- CLICK "1 Night" option ----
    page.click("INSERT_SELECTOR_FOR_1_NIGHT_OPTION")
    
    # ---- CLICK DATE INPUT ----
    page.click("INSERT_SELECTOR_FOR_DATE_INPUT")
    
    # ---- CLICK NEXT MONTH ARROW until correct month is visible ----
    # You can loop here until you see your month in the calendar
    # Example:
    # while not page.is_visible("INSERT_SELECTOR_FOR_DESIRED_MONTH_HEADER"):
    #     page.click("INSERT_SELECTOR_FOR_NEXT_MONTH_ARROW")
    
    # ---- WAIT for calendar / availability to load ----
    page.wait_for_selector("INSERT_SELECTOR_FOR_CALENDAR_LOADED")

    # ---- TAKE SCREENSHOT FOR DEBUG ----
    page.screenshot(path="calendar_debug.png")

# ----------------------
# STEP 2: Fetch availability via API (optional)
# ----------------------
# You can optionally fetch the JSON data if you know the API URL
API_URL = "INSERT_API_URL_FOR_DATE_CHECK"  # the URL you found in network tab
try:
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print("API request failed:", e)
    data = []

# ----------------------
# STEP 3: Check if your date is available
# ----------------------
date_available = False
for day in data:
    if day.get("localDate") == DATE_TO_CHECK and day.get("available"):
        date_available = True
        break

# ----------------------
# STEP 4: Send email if available
# ----------------------
if date_available:
    msg = EmailMessage()
    msg.set_content(f"The date {DATE_TO_CHECK} is available!")
    msg["Subject"] = f"Dry Tortugas Opening: {DATE_TO_CHECK}"
    msg["From"] = EMAIL_USER
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
    print("Email sent!")
else:
    print(f"{DATE_TO_CHECK} is not available.")

browser.close()
