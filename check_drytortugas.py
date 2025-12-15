from playwright.sync_api import sync_playwright
import smtplib
from email.message import EmailMessage
import os

URL = "https://www.drytortugas.com/overnight-camping-reservations/"
TARGET_DAY = "9"
TEST_MODE = True  # Change to False once the test works

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
    page.wait_for_timeout(8000)  # Wait for JS to load calendar

    # Take a screenshot for debugging and artifact upload
    page.screenshot(path="calendar_debug.png", full_page=True)
    print("Screenshot saved as calendar_debug.png")

    # TODO: Replace this selector with the correct arrow button after inspecting screenshot
    arrow_selector = "button:has-text('>')"  # placeholder

    # Click the arrow 6 times to reach April
    for _ in range(6):
        page.wait_for_selector(arrow_selector, timeout=60000)
        page.click(arrow_selector)
        page.wait_for_timeout(2000)

    # Check if the target day exists on the page
    month_text = page.inner_text("body")

    if TEST_MODE:
        send_email("TEST: Dry Tortugas Checker", "Your checker ran successfully!")
        print("Test email sent.")
    else:
        if TARGET_DAY in month_text:
            send_email("Dry Tortugas Available!", f"April {TARGET_DAY} is available!")
            print(f"April {TARGET_DAY} is available! Email sent.")

    browser.close()
