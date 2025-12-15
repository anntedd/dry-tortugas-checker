import requests
import os
from email.message import EmailMessage
import smtplib

# ----------------------
# CONFIG
# ----------------------
API_URL = "https://checkout-api.ventrata.com/octo/availability/calendar?productId=5a39dbd6-98c1-4170-a4e7-4b4292632a99&optionId=435606fd-0077-44ba-b9d4-a383004ac6aa&rentalDurationId=&localDateStart=2025-12-01&localDateEnd=2025-12-31&units%5B0%5D%5Bid%5D=unit_52e53817-b7d8-4d96-b3d8-b1aa1fef77ec&units%5B0%5D%5Bquantity%5D=1&units%5B0%5D%5Bextras%5D%5B%5D=&currency=USD&extras%5B%5D="
TARGET_DATE = "2026-04-09"  # change to the date you want
TEST_MODE = True  # set to False to only send email when date is available

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
# Fetch API and check availability
# ----------------------
response = requests.get(API_URL)
response.raise_for_status()  # fail if API request fails
data = response.json()

# Find the target date in the JSON
found = False
for day in data:
    if day.get("localDate") == TARGET_DATE:
        found = True
        if day.get("available", False):
            send_email("Dry Tortugas Camping Available!", f"{TARGET_DATE} is available!")
            print(f"{TARGET_DATE} is available! Email sent.")
        else:
            print(f"{TARGET_DATE} is not available yet.")
        break

if TEST_MODE:
    send_email("TEST: Dry Tortugas Checker", f"Checker ran successfully. Found date? {found}")
    print("Test email sent.")
