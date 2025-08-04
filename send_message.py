import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib3
import certifi

def send_message(author):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )

    # Your email and the App Password you generated
    sender_email = "w.use.mjk@gmail.com"
    app_password = "zmhl ubof poyy phbx" # Use the 16-character App Password here

    # The recipient email address
    receiver_email = "markjoekenny53@gmail.com"

    # The subject and body of the email
    subject = "New Patreon Update: " + author 
    body = "This author has just been updated!"

    # Create a multipart message to handle both text and other content if needed
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain")) # Attach the plain text body

    # Set up the SMTP server details for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Notification sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")