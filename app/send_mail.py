import smtplib
import ssl
import json
import os
from email.message import EmailMessage

import flask


def send_mail(to_email, uname, url, confirm):
    try:
        jsonfile = os.path.join(flask.current_app.root_path, "gapw.json")
        with open(jsonfile) as file:
            data = json.load(file)
        mailaddr = data["email"]
        password = data["password"]

        port = 465  # For SSL

        # Create a secure SSL context
        context = ssl.create_default_context()

        msg = EmailMessage()

        if not confirm:
            msg.set_content(
                f"Biitter account reset request\n Your B-itter account username is {uname} \n To reset your password "
                f"click this link:\n {url}")

            msg['Subject'] = 'B-itter password reset'
        else:
            msg.set_content(
                f"""
                To confirm your email click this link: \n {url}
                """
            )
            msg['Subject'] = 'B-itter verify email'

        msg['From'] = mailaddr
        msg['To'] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(mailaddr, password)
            server.send_message(msg)
            server.quit()
            return True
    except Exception as e:
        print(e)
