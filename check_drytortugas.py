from playwright.sync_api import sync_playwright
import smtplib
from email.message import EmailMessage
import os

URL = "https://www.drytortugas.com/overnight-camping-reservations/"
TARGET_DAY = "9"
TEST_MODE = True  # Change to False once everything works

# ----------------------
# Email function
# ----------------------
def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = os.environ["EMAIL_TO"]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
        server.send_message(msg)

# ----------------------
# Main Playwright logic
# ----------------------
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, timeout=60000)

    # Wait for the calendar container to fully load
    page.wait_for_selector("div#ui-datepicker-div", timeout=15000)

    # Take a screenshot after calendar loads
    page.screenshot(path="calendar_debug.png", full_page=True)
    print("Screenshot saved as calendar_debug.png")

    # Update this selector to match the "next month" arrow on the calendar
    arrow_selector = "button.ui-datepicker-next"

    # Click the arrow 6 times to reach April (adjust if needed)
    for _ in range(6):
        page.wait_for_selector(arrow_selector, timeout=10000)
        page.click(arrow_selector)
        page.wait_for_timeout(1000)  # brief pause between clicks

    # Check if the target day exists on the page
    month_text = page.inner_text("div#ui-datepicker-div")

    if TEST_MODE:
        send_email("TEST: Dry Tortugas Checker", "Your checker ran successfully!")
        print("Test email sent.")
    else:
        if TARGET_DAY in month_text:
            send_email("Dry Tortugas Available!", f"April {TARGET_DAY} is available!")
            print(f"April {TARGET_DAY} is available! Email sent.")

    browser.close()
