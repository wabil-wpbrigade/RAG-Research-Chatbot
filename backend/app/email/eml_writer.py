import os
import uuid
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

EMAIL_OUTBOX_PATH = os.getenv("EMAIL_OUTBOX_PATH", "/emails")
EMAIL_FROM = os.getenv("EMAIL_FROM", "no-reply@rag-chatbot.local")


def write_eml_file(to: str, subject: str, body: str) -> str:
    """
    Create and enqueue an email by writing a .eml file to the outbox directory.

    The generated file is written atomically to ensure it is never read
    partially by the email worker. Once written, the email worker
    will pick up the file, send it via SMTP, and delete it upon success.

    Args:
        to (str): Recipient email address.
        subject (str): Email subject line.
        body (str): Plain-text email body.

    Returns:
        str: Absolute path to the generated .eml file.

    Raises:
        ValueError: If any required email field is empty.
    """
    if not to or not subject or not body:
        raise ValueError("Email fields must not be empty")

    os.makedirs(EMAIL_OUTBOX_PATH, exist_ok=True)

    msg = EmailMessage()
    msg["From"] = EMAIL_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="rag-chatbot.local")

    msg.set_content(body)

    filename = f"email_{uuid.uuid4().hex}.eml"
    file_path = os.path.join(EMAIL_OUTBOX_PATH, filename)

    # ✅ Atomic write (BYTES, not text)
    tmp_path = f"{file_path}.tmp"
    with open(tmp_path, "wb") as f:
        f.write(msg.as_bytes())

    os.replace(tmp_path, file_path)

    return file_path
