from email import message_from_bytes
from email.message import EmailMessage
from email import policy


def parse_eml_file(path: str) -> EmailMessage:
    """
    Parse and validate an .eml file from disk.

    Reads a raw .eml file and converts it into an EmailMessage object.
    Ensures the message contains required headers before it is sent.

    Args:
        path (str): Path to the .eml file.

    Returns:
        EmailMessage: A validated email message ready for SMTP sending.

    Raises:
        ValueError: If the file is not a valid EML email or is missing
                    required headers such as To, From, or Subject.
    """
    with open(path, "rb") as f:
        msg = message_from_bytes(f.read(), policy=policy.default)

    # Now this IS an EmailMessage
    if not isinstance(msg, EmailMessage):
        raise ValueError("Invalid EML file")

    # Validate headers
    if not msg["To"] or not msg["From"] or not msg["Subject"]:
        raise ValueError("Invalid EML file")

    return msg
