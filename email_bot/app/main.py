from app.worker import run_daemon
from app.config import validate_config



def main():
    """
    Initialize and start the email bot.

    Validates configuration and starts the background worker
    that continuously scans the email outbox and sends messages.
    """
    validate_config()
    run_daemon()


if __name__ == "__main__":
    main()
