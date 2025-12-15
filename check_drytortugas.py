from playwright.sync_api import sync_playwright
import smtplib
from email.message import EmailMessage
import os

URL = "https://www.drytortugas.com/overnight-camping-reservations/"
TARGET_DAY = "9"
TEST_MODE = True  # Change to False once the test works

# Email sending function
def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = os.environ["EMAIL_TO"]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASS"])
        server.send_message(msg)

# Main browser logic
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, timeout=60000)
    page.wait_for_timeout(3000)

    # Click the ">" arrow to move the calendar forward 6 times to reach April
    for _ in range(6):
        page.wait_for_selector("button.ui-datepicker-next", timeout=60000)
        page.click("button.ui-datepicker-next")
        page.wait_for_timeout(2000)  # wait 2 seconds between clicks

    # Check page text for the target day
    month_text = page.inner_text("body")

    if TEST_MODE:
        send_email("TEST: Dry Tortugas Checker", "Your checker ran successfully!")
        print("Test email sent.")
    else:
        if TARGET_DAY in month_text:
            send_email("Dry Tortugas Available!", f"April {TARGET_DAY} is available!")
            print(f"April {TARGET_DAY} is available! Email sent.")

    browser.close()
