from datetime import datetime
import sys, os, shutil
from constants import (
    DATA_STORAGE_PATH, LOCAL_CHAT_HISTORY_DB_PATH, LOCAL_CHAT_HISTORY_DB_TEMPLATE_PATH, 
    LOCAL_CHAT_HISTORY_DB_FILE_PREFIX, LOCAL_DB_EXTENSION
)
from database import ChatHistoryDb


def get_current_datetime() -> str:
    """
    Returns the current date and time of the system
    """
    return str(datetime.now()).split('.')[0]


def resource_path(relative_path:str) -> str:
    """
    Returns absolute path of project relative paths
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_file_size_MB(path:str) -> float:
    """
    Returns the size of a file in MB
    """
    return os.stat(path).st_size / (1024 * 1024)


def current_chat_db_name() -> str:
    """
    Returns the name of the current local chat history database file
    """
    os.makedirs(LOCAL_CHAT_HISTORY_DB_PATH, exist_ok=True)
    sorted_db_names:list = sorted(os.listdir(LOCAL_CHAT_HISTORY_DB_PATH), key=lambda name: int(name.split('.')[0].replace(LOCAL_CHAT_HISTORY_DB_FILE_PREFIX, '')))
    db_name:str = f'{LOCAL_CHAT_HISTORY_DB_FILE_PREFIX}0{LOCAL_DB_EXTENSION}'
    if len(sorted_db_names) > 0:
        db_name = sorted_db_names[-1]
    return db_name


def next_chat_db_name() -> str:
    """
    Returns the next local chat database name
    """
    os.makedirs(LOCAL_CHAT_HISTORY_DB_PATH, exist_ok=True)
    sorted_db_names:list = sorted(os.listdir(LOCAL_CHAT_HISTORY_DB_PATH), key=lambda name: int(name.split('.')[0].replace(LOCAL_CHAT_HISTORY_DB_FILE_PREFIX, '')))
    db_name:str = f'{LOCAL_CHAT_HISTORY_DB_FILE_PREFIX}0{LOCAL_DB_EXTENSION}'
    if len(sorted_db_names) > 0:
        next_db_index:int = int(sorted_db_names[-1].split('.')[0].replace(LOCAL_CHAT_HISTORY_DB_FILE_PREFIX, '')) + 1
        db_name = f'{LOCAL_CHAT_HISTORY_DB_FILE_PREFIX}{next_db_index}{LOCAL_DB_EXTENSION}'
    return db_name


def create_next_chat_db(db_name:str) -> None:
    """
    Creates the next local chat database
    """
    new_db_path = os.path.join(LOCAL_CHAT_HISTORY_DB_PATH, db_name)
    if not os.path.exists(new_db_path):
        shutil.copyfile(LOCAL_CHAT_HISTORY_DB_TEMPLATE_PATH, new_db_path)
