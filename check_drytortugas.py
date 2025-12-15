import smtplib
from email.mime.text import MIMEText
import os

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

msg = MIMEText("If you got this, GitHub Actions can email you.")
msg["Subject"] = "Dry Tortugas Email Test"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO

# Use SSL directly
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.send_message(msg)

print("Email sent")
