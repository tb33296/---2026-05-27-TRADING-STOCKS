from datetime import datetime


def current_timestamp() -> str:
    """
    Get formatted timestamp.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )