import smtplib
from email.mime.text import MIMEText

def send_email_notification(to_email, message):
    # Email server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'your_email@gmail.com'
    smtp_password = 'your_email_password'

    # Create the email message
    msg = MIMEText(message)
    msg['Subject'] = 'Satellite Passing Notification'
    msg['From'] = smtp_username
    msg['To'] = to_email

    # Send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, msg.as_string())

# Example usage:
send_email_notification('user@example.com', 'Satellite will pass over your location at: 12:00 PM')
