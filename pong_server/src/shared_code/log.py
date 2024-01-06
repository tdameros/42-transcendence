from src.shared_code.settings import DEBUG


def log(log_message):
    if DEBUG:
        print(log_message)
