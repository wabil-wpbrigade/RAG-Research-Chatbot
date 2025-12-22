import os
import time
from app.config import EMAIL_OUTBOX_PATH, SCAN_INTERVAL_SECONDS
from app.smtp_client import SMTPClient
from app.eml_parser import parse_eml_file


def process_outbox():
    """
    Process all pending .eml files in the outbox directory.

    Each valid email file is parsed, sent via SMTP, and removed
    upon successful delivery. Failed files remain in the outbox
    for retry in the next cycle.
    """
    smtp = SMTPClient()

    files = [
        f for f in os.listdir(EMAIL_OUTBOX_PATH)
        if f.lower().endswith(".eml")
    ]

    for filename in files:
        file_path = os.path.join(EMAIL_OUTBOX_PATH, filename)

        try:
            message = parse_eml_file(file_path)
            smtp.send(message)

            os.remove(file_path)
            print(f"[✓] Sent and removed: {filename}")

        except Exception as e:
            print(f"[!] Failed to process {filename}: {e}")
            # File remains for retry

    smtp.close()


def run_daemon():
    """
    Run the email worker in daemon mode.

    Continuously monitors the email outbox directory and processes
    pending emails at a fixed interval defined in configuration.
    """
    print("[*] Email bot started. Watching outbox...")

    while True:
        process_outbox()
        time.sleep(SCAN_INTERVAL_SECONDS)
