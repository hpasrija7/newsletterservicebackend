import schedule
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
import os


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': os.environ["DBPassword"],
    'database': 'newslettersystemdb',
}

def send_newsletter(user_email):
    subject = 'Weekly Newsletter'
    
    body = f"""
    <html>
        <body>
            <p>Dear user,</p>
            <p>This is your weekly newsletter</p>
            <p>We wish to inform you that we have launched Parentune PLUS with many advanced features like 1:1 caoching, diet plan, nutrition traker etc.</p>
            <p>Click the link below to buy PLUS or to see what the parents are saying about PLUS. </p>
            <button><a href="https://newsletter-3uy1.onrender.com/">Buy Parentune PLUS</a></button>
            <p>Happy Parenting !!</p>
        </body>
    </html>
    """

    smtp_server = 'smtp.gmail.com'
    smtp_port = 25
    smtp_username = os.environ["smtp_username"]
    smtp_password = os.environ["smtp_password"]
    sender_email = os.environ["sender_email"]

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = user_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'html'))

        server.sendmail(sender_email, user_email, message.as_string())
        
        server.quit()

        log_successful_newsletter(user_email)

    except Exception as e:
        log_failed_newsletter(user_email, str(e))

def log_successful_newsletter(user_email):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT id FROM user WHERE email = %s", (user_email,))
        user_id = cursor.fetchone()
        if user_id:
            print("inside if")
            cursor.execute("INSERT INTO log (user_id, status, timestamp) VALUES (%s, %s, %s)", (user_id[0], 'success', datetime.now()))
            print("exec insert")
            connection.commit()
        print("outside if")


    except Exception as e:
        print(f"Error logging successful newsletter: {str(e)}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

def log_failed_newsletter(user_email, error_message):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT id FROM user WHERE email = %s", (user_email,))
        user_id = cursor.fetchone()

        if user_id:
            cursor.execute("INSERT INTO log (user_id, status, error_message, timestamp) VALUES (%s, %s, %s, %s)",
                           (user_id[0], 'failure', error_message, datetime.now()))
            connection.commit()

    except Exception as e:
        print(f"Error logging failed newsletter: {str(e)}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

def retrieve_subscribed_users():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT email FROM user WHERE subscription_status = true")
        subscribed_users = [user['email'] for user in cursor.fetchall()]
        return subscribed_users
    
    except Exception as e:
        print(f"Error retrieving subscribed users: {str(e)}")
        return []

    finally:
        cursor.close()
        connection.close()

def schedule_newsletter_job():
    subscribed_users = retrieve_subscribed_users()
    for user_email in subscribed_users:
        schedule.every().sunday.at("19:08").do(send_newsletter, user_email)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    schedule_newsletter_job()
    run_scheduler()
