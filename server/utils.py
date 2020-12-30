from datetime import datetime
import string, random


def get_current_datetime():
    """
    Returns the current date and time of the system
    """
    return str(datetime.now()).split('.')[0]


def generate_activation_code(length=6):
    """
    Generates a 6-digit secret code
    """
    chars = string.digits
    return ''.join(random.choice(chars) for i in range(length))