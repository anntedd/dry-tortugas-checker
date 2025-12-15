import os
import smtplib

# Get credentials and recipient from environment (GitHub Secrets)
EMAIL_FROM = os.environ.get('EMAIL_FROM')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_TO = os.environ.get('EMAIL_TO')

# Check that everything is set
if not EMAIL_FROM or not EMAIL_PASSWORD or not EMAIL_TO:
    raise ValueError("One or more email environment variables are missing!")

# Connect to Gmail SMTP and send email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    
    subject = "Test Email"
    body = "This is a test email from your DryT script."
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg)

print("Email sent successfully!")
