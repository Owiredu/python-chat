from datetime import datetime
import os


def get_current_datetime():
    """
    Returns the current date and time of the system
    """
    return str(datetime.now()).split('.')[0]


def get_wordlist():
    """
    Returns a list of words from the words file
    """
    return [w.replace('\n', '') for w in open(os.path.join('client', 'resources', 'words.txt'), 'r', newline='\n').readlines()]