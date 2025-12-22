import os

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

EMAIL_OUTBOX_PATH = os.getenv("EMAIL_OUTBOX_PATH", "/emails")
SCAN_INTERVAL_SECONDS = int(os.getenv("SCAN_INTERVAL_SECONDS", "5"))


def validate_config():
    """
    Validate required environment variables.

    Ensures that all mandatory configuration values needed to send emails
    (SMTP host, username, and password) are present. The application
    will fail fast at startup if any required configuration is missing.

    Raises:
        RuntimeError: If one or more required environment variables are missing.
    """
    missing = []
    for key, value in {
        "SMTP_HOST": SMTP_HOST,
        "SMTP_USER": SMTP_USER,
        "SMTP_PASSWORD": SMTP_PASSWORD,
    }.items():
        if not value:
            missing.append(key)

    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
