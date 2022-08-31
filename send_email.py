import email, smtplib, ssl
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

class SendEmail:
    def __init__(self, subject, sender, recipient, body, attachment, smtp_server, port):
        self.subject = subject
        self.sender = sender
        self.recipient = recipient
        self.body = body
        self.attachment = attachment
        self.smtp_server = smtp_server
        self.port = port

    def send_email(self):
        message = MIMEMultipart()
        message['Subject'] = self.subject
        message['From'] = self.sender
        message['To'] = self.recipient

        sender = self.sender
        recipient = self.recipient
        body = self.body
        attachment = self.attachment
        smtp_server = self.smtp_server
        port = self.port

        try:
            with open(body, 'r', encoding='utf-8') as file:
                message.attach(MIMEText(file.read(), 'html'))
        except FileNotFoundError:
            print("File for email's body not found!")

        try:
            with open(attachment, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={attachment}'
                )
                message.attach(part)
        except FileNotFoundError:
            print("Attachment file not found!")

        text = message.as_string()
        context = ssl._create_unverified_context()

        try:
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.sendmail(sender, recipient, text)
        except Exception as e:
            print(e)
