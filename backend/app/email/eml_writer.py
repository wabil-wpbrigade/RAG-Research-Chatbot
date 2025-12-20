import os
import uuid
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

EMAIL_OUTBOX_PATH = os.getenv("EMAIL_OUTBOX_PATH", "/emails")
EMAIL_FROM = os.getenv("EMAIL_FROM", "no-reply@rag-chatbot.local")

def write_eml_file(to: str, subject: str, body: str) -> str:
    """
    Creates and enqueues an email by writing a .eml file to disk.
    Ensures atomic writes so the email worker never reads partial files.
    """
    validate_email_fields(to, subject, body)
    ensure_outbox_dir()
    msg = build_email(to, subject, body)
    return write_email_atomically(msg)



def validate_email_fields(to: str, subject: str, body: str):
    """
    Validates that required email fields are present.
    """
    if not to or not subject or not body:
        raise ValueError("Email fields must not be empty")




def ensure_outbox_dir():
    """
    Ensures the email outbox directory exists.
    """
    os.makedirs(EMAIL_OUTBOX_PATH, exist_ok=True)



def build_email(to: str, subject: str, body: str) -> EmailMessage:
    """
    Builds a properly formatted email message.
    """
    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="rag-chatbot.local")
    msg.set_content(body)
    return msg



def write_email_atomically(msg: EmailMessage) -> str:
    """
    Writes the email to disk using an atomic file operation.
    """
    path = email_file_path()
    tmp = f"{path}.tmp"
    write_bytes(tmp, msg.as_bytes())
    os.replace(tmp, path)
    return path


def write_bytes(path: str, content: bytes):
    """
    Writes raw bytes to a file.
    """
    with open(path, "wb") as f:
        f.write(content)


def email_file_path() -> str:
    """
    Generates a unique file path for the email.
    """
    name = f"email_{uuid.uuid4().hex}.eml"
    return os.path.join(EMAIL_OUTBOX_PATH, name)
