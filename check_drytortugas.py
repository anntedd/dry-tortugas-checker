import requests
import os
from email.message import EmailMessage
import smtplib

# ----------------------
# CONFIG
# ----------------------
API_URL = "PASTE_THE_API_URL_HERE"  # Replace with the actual API endpoint you found
TARGET_DATE = "2026-04-09"  # The date you want to monitor

# Email environment variables
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")

# ----------------------
# Send email function
# ----------------------
def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
    print("Email sent:", subject)

# ----------------------
# Check availability
# ----------------------
def check_availability():
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()

        for day in data:
            if day.get("localDate") == TARGET_DATE:
                if day.get("available"):
                    send_email(
                        f"Dry Tortugas Available! {TARGET_DATE}",
                        f"April 9 is now available for booking!"
                    )
                    return True
                else:
                    print(f"{TARGET_DATE} is still not available.")
                    return False

        print(f"{TARGET_DATE} not found in API response.")
        return False

    except Exception as e:
        print("Error checking availability:", e)
        return False

# ----------------------
# MAIN
# ----------------------
if __name__ == "__main__":
    check_availability()
