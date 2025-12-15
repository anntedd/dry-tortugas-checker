import smtplib
from email.mime.text import MIMEText
import os

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

msg = MIMEText("✅ GitHub Actions email test successful.")
msg["Subject"] = "Dry Tortugas Email Test"
msg["From"] = EMAIL_FROM
msg["To"] = EMAIL_TO

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.send_message(msg)

print("Email sent successfully!")
