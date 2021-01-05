from datetime import datetime
import sys, os


def get_current_datetime():
    """
    Returns the current date and time of the system
    """
    return str(datetime.now()).split('.')[0]


def resource_path(relative_path):
    """
    Returns absolute path of project relative paths
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_current_dir():
    """
    Returns the path to the base folder containing this file
    """
    return os.path.dirname(__file__)