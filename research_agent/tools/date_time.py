from datetime import datetime

def get_date_time() -> str:
    """
    A tool that returns the current date and time.
    """
    now = datetime.now()

    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%I:%M:%S %p"),
        "day": now.strftime("%A")
    }
