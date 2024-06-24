import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(data):
    # Email credentials
    sender_email = "kashishvarshney63@gmail.com"
    receiver_email = "varkashish@gmail.com"
    password = "yfpdshqgkhnveusa"  # Use an app-specific password if using Gmail

    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Subject of the Email"

    # Add body to email
    body = f"This is the body of the email , {data}"
    message.attach(MIMEText(body, "plain"))

    # Connect to the server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Secure the connection

    try:
        # Login to the email account
        server.login(sender_email, password)
        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Disconnect from the server
        server.quit()
