import smtplib

recipient_email = 'hpasrija7@gmail.com'
smtp_server = 'smtp.gmail.com'
smtp_port = 25
smtp_username = 'hp001166@gmail.com'
smtp_password = 'pbyy halp fvhu fclc'
sender_email = 'hp001166@gmail.com'

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    subject = 'Test Email'
    body = 'This is a test email.'

    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(sender_email, recipient_email, message)

    print("Test email sent successfully!")

except Exception as e:
    print(f"Error sending test email: {str(e)}")

finally:
    server.quit()
