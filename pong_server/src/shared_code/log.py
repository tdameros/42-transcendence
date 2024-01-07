import sys

from src.shared_code.settings import DEBUG


def log(log_message, end: str | None = '\n'):
    if DEBUG:
        print(log_message, end=end)
        sys.stdout.flush()
