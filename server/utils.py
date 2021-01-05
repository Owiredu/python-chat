from datetime import datetime
import io
import string, random, os, sys, json, shutil
from constants import ACTIVATION_CODE_LENGTH, MESSAGES_STORAGE_PATH
from file_encrypter import FileEncrypter


def get_current_datetime() -> str:
    """
    Returns the current date and time of the system
    """
    return str(datetime.now()).split('.')[0]


def generate_activation_code(length:int=ACTIVATION_CODE_LENGTH) -> str:
    """
    Generates a 6-digit secret code
    """
    chars = string.digits
    return ''.join(random.choice(chars) for i in range(length))


def resource_path(relative_path:str) -> str:
    """
    Returns absolute path of project relative paths
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname("."), relative_path)


def encrypt_json_data(json_data:str) -> bytes:
    """
    Encryptes json data data
    """
    f = FileEncrypter()
    return f.encrypt(bytes(json_data, encoding='utf-8'))

def decrypt_json_data(encrypted_data:bytes) -> bytes:
    """
    Decrypts json data
    """
    f = FileEncrypter()
    return f.decrypt(encrypted_data)


def save_message(email_address:str, data:dict) -> None:
    """
    Creates the storage directory for a user's messages
    """
    try:
        # create the user's directory if it does not exist
        dir_path:str = os.path.join(MESSAGES_STORAGE_PATH, email_address)
        os.makedirs(dir_path, exist_ok=True)
        # get the message file name
        file_name:str = '0.json'
        message_file_names:list = os.listdir(dir_path)
        if len(message_file_names) > 0:
            sorted_message_file_names:list = sorted(message_file_names, key=lambda name: int(name.split('.')[0]))
            file_name = str(int(sorted_message_file_names[-1].split('.')[0]) + 1) + '.json'
        # convert the data to json and encrypt
        json_data:str = json.dumps(data)
        encrypted_json_data:bytes = encrypt_json_data(json_data)
        # save the file
        json_file:io = open(os.path.join(dir_path, file_name), 'wb')
        json_file.write(encrypted_json_data)
        json_file.close()
    except Exception as e:
        print(e)


def load_messages(email_address:str) -> dict:
    """
    Loads a stored messages and returns them as a dictionary.
    The filenames are the keys and the data are the values
    """
    messages:dict = dict()
    try:
        dir_path:str = os.path.join(MESSAGES_STORAGE_PATH, email_address)
        # load the message files, decrypt them and add the data to a dictionary
        message_file_names:list = os.listdir(dir_path)
        sorted_message_file_names:list = sorted(message_file_names, key=lambda name: int(name.split('.')[0]))
        for file_name in sorted_message_file_names:
            json_file:io = open(os.path.join(dir_path, file_name), 'rb')
            encrypted_json_data:bytes = json_file.read()
            decrypted_json_data:bytes = decrypt_json_data(encrypted_json_data)
            decrypted_json_data:dict = json.loads(decrypted_json_data)
            messages[file_name] = decrypted_json_data
        return messages
    except Exception as e:
        print(e)
    return messages


def delete_message(email_address:str, file_name:str) -> None:
    """
    Deletes a message file and the directory if empty
    """
    try:
        dir_path:str = os.path.join(MESSAGES_STORAGE_PATH, email_address)
        # delete the message file
        os.remove(os.path.join(dir_path, file_name))
        # delete the user's message directory if no message exists
        if len(os.listdir(dir_path)) == 0:
            shutil.rmtree(dir_path)
    except Exception as e:
        print(e)
