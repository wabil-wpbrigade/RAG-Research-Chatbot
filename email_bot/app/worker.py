import os
import time

from app.smtp_client import SMTPClient
from app.eml_parser import parse_eml_file
from app.config import EMAIL_OUTBOX_PATH, SCAN_INTERVAL_SECONDS


def process_outbox():
    """
    Processes all pending .eml files in the outbox directory.
    Sends emails via SMTP and removes files upon success.
    """
    smtp = SMTPClient()
    for file_path in eml_files():
        handle_email_file(smtp, file_path)
    smtp.close()



def run_daemon():
    """
    Runs the email worker in daemon mode.
    Periodically scans and processes the outbox.
    """
    print("[*] Email bot started. Watching outbox...")
    while True:
        process_outbox()
        time.sleep(SCAN_INTERVAL_SECONDS)




def eml_files() -> list[str]:
    """
    Returns a list of absolute paths to .eml files in the outbox.
    """
    return [
        os.path.join(EMAIL_OUTBOX_PATH, f)
        for f in os.listdir(EMAIL_OUTBOX_PATH)
        if f.lower().endswith(".eml")
    ]


def handle_email_file(smtp: SMTPClient, file_path: str):
    """
    Parses, sends, and deletes an email file.
    Leaves the file intact if processing fails.
    """
    try:
        send_email_file(smtp, file_path)
        remove_file(file_path)
    except Exception as e:
        print(f"[!] Failed to process {file_path}: {e}")



def send_email_file(smtp: SMTPClient, file_path: str):
    """
    Parses an email file and sends it via SMTP.
    """
    message = parse_eml_file(file_path)
    smtp.send(message)



def remove_file(path: str):
    """
    Removes a file from disk.
    """
    os.remove(path)
    print(f"[✓] Sent and removed: {os.path.basename(path)}")

