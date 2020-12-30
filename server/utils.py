from datetime import datetime
import string, random, os, sys
from constants import *


def get_current_datetime():
    """
    Returns the current date and time of the system
    """
    return str(datetime.now()).split('.')[0]


def generate_activation_code(length=ACTIVATION_CODE_LENGTH):
    """
    Generates a 6-digit secret code
    """
    chars = string.digits
    return ''.join(random.choice(chars) for i in range(length))


def resource_path(self, relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)