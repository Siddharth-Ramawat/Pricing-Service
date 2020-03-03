from typing import List
import os
from requests import Response, post


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun:

    FROM_EMAIL = "<do-not-reply@sandbox6e769479e7c84f8fa0efac40249c69f7.mailgun.org>"
    FROM_TITLE = f"Pricing Service <do-not-reply@{FROM_EMAIL}>"

    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        api_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)

        if api_key is None:
            raise MailgunException("Failed to load Mailgun API_Key")
        if domain is None:
            raise MailgunException("Failed to load Mailgun Domain")

        response = post(
            f"{domain}/messages",
            auth=("api", "key-4877531ece758788416250bd5229258a"),
            data={"from": cls.FROM_TITLE,
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html})

        if response.status_code != 200:
            raise MailgunException('An error occured while sending email')
        else:
            return response


Mailgun.send_mail(['siddharth_ramawat@yahoo.com'], "Hello", "This is mailgun test email", "<p>This is a HTML Test</p>")