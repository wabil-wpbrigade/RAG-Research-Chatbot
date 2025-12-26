import smtplib

from email.message import EmailMessage
from app.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD


class SMTPClient:
    """
    Lightweight SMTP client wrapper.

    Manages the SMTP connection lifecycle including connecting,
    authenticating, sending messages, and closing the connection.
    """
    def __init__(self):
        """
        Initialize the SMTP client without an active connection.
        """
        self.server = None

    def connect(self):
        """
        Establish a secure SMTP connection and authenticate.

        Uses STARTTLS and logs in using credentials from configuration.
        """
        self.server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        self.server.starttls()
        self.server.login(SMTP_USER, SMTP_PASSWORD)

    def send(self, message: EmailMessage):
        """
        Send an email message via SMTP.

        Automatically connects to the SMTP server if no active
        connection exists.

        Args:
            message (EmailMessage): The email message to send.
        """
        if not self.server:
            self.connect()

        self.server.send_message(message)

    def close(self):
        """
        Close the SMTP connection if it is open.
        """
        if self.server:
            self.server.quit()
            self.server = None
