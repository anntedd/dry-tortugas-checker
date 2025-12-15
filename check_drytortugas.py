import os
import smtplib
from email.mime.text import MIMEText
import requests

# ===========================
# Email setup (works with your GitHub secrets + App Password)
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
# Example API endpoint the site uses (inspect via browser Network tab):
API_URL = "https://www.drytortugas.com/overnight-camping-reservations/api/reservations"

# Request payload — checking April 9 for 1 night
payload = {
    "month": 4,       # April
    "year": 2026,     # adjust as needed
    "nights": 1
}

try:
    response = requests.get(API_URL, params=payload)
    response.raise_for_status()
    data = response.json()

    # Inspect data structure — assuming a list of available dates
    # (adjust key names if the API uses different names)
    available_dates = [entry["date"] for entry in data.get("availability", [])]

    if "2026-04-09" in available_dates:
        send_email(
            "Dry Tortugas Alert: April 9 Available!",
            "✅ April 9 for 1 night is now available. Go book it!"
        )
    else:
        print("April 9 is not available yet.")

except Exception as e:
    send_email(
        "Dry Tortugas Script Error",
        f"Something went wrong when checking availability:\n{e}"
    )
    raise
