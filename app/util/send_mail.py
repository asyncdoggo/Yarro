import smtplib
import ssl
from email.message import EmailMessage
from dotenv import dotenv_values

config = dotenv_values(".env")


def send_mail(to_email, uname, url, confirm):
    try:
        mailaddr = config["EMAIL"]
        password = config["EMAIL_PASSWORD"]

        port = 465  # For SSL

        # Create a secure SSL context
        context = ssl.create_default_context()

        msg = EmailMessage()

        if not confirm:
            msg.set_content(
                f"Yarro account reset request\n Your Yarro account username is {uname} \n To reset your password "
                f"click this link:\n {url}")

            msg['Subject'] = 'Yarro password reset'
        else:
            msg.set_content(
                f"""
                To confirm your email click this link: \n {url}
                """
            )
            msg['Subject'] = 'Yarro verify email'

        msg['From'] = mailaddr
        msg['To'] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(mailaddr, password)
            server.send_message(msg)
            server.quit()
            return True
    except Exception as e:
        print(e)
