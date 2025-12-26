import os

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

EMAIL_OUTBOX_PATH = os.getenv("EMAIL_OUTBOX_PATH", "/emails")
SCAN_INTERVAL_SECONDS = int(os.getenv("SCAN_INTERVAL_SECONDS", "5"))


def required_env_vars() -> dict:
    return {
        "SMTP_HOST": SMTP_HOST,
        "SMTP_USER": SMTP_USER,
        "SMTP_PASSWORD": SMTP_PASSWORD,
    }


def find_missing(vars_map: dict) -> list[str]:
    return [key for key, value in vars_map.items() if not value]


def validate_config() -> None:
    missing = find_missing(required_env_vars())
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
