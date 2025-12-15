from playwright.sync_api import sync_playwright
import smtplib
from email.message import EmailMessage
import os

URL = "https://www.drytortugas.com/overnight-camping-reservations/"
TARGET_DAY = "9"
TEST_MODE = True  # Set to False once you want real alerts

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

    # Wait for page to fully load
    page.wait_for_timeout(5000)

    # Take an initial screenshot of the full page (to see headers, inputs, calendar)
    page.screenshot(path="calendar_debug.png", full_page=True)
    print("Initial screenshot saved as calendar_debug.png")

    # Print out all input elements for inspection
    inputs = page.query_selector_all("input")
    print("Found input elements:")
    for i, inp in enumerate(inputs):
        print(i, inp.get_attribute("id"), inp.get_attribute("name"), inp.get_attribute("placeholder"))

    # Print out all headers for inspection
    headers = page.query_selector_all("h1, h2, h3, h4, h5, h6")
    print("Found headers:")
    for h in headers:
        print(h.inner_text())

    # Stop here for debugging; later you can click the input and arrow once you know the selector
    # For example:
    # page.click("input#arrivalDate")
    # page.wait_for_selector("div.ui-datepicker-group", timeout=10000)
    # arrow_selector = "button.ui-datepicker-next"
    # for _ in range(6):
    #     page.click(arrow_selector)
    #     page.wait_for_timeout(1000)
    # month_text = page.inner_text("div.ui-datepicker-group")
    # if TARGET_DAY in month_text:
    #     send_email("Dry Tortugas Available!", f"April {TARGET_DAY} is available!")
    #     print(f"April {TARGET_DAY} is available! Email sent.")

    # Close browser
    browser.close()
