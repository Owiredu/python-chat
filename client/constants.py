import os


# for connection status values
ONLINE:int = 1 # signifies the the client/sender is online
OFFLINE:int = 0 # signifies that the client/sender is offline
MESSAGE_THREAD_UP:int = 8 # signifies that the messaging thread has already started
MESSAGE_THREAD_DOWN:int = -8

# for message types
SUCCESS:int = 2 # for success notifications
ERROR:int = -2 # for error notifications 
REGISTER:int = 3 # for new client registration
NORMAL:int = 4 # for normal client to client messages
STATUS_UPDATE:int = 5 # notify a change in the online/offline status of a client
ACTIVATION:int = 7 # for activation of account

# server name for sending messages to clients
SERVER_NAME:str = 'server'

# port numbers
REGISTER_PORT:str = '9000'
LOGIN_PORT:str = '9001'
CHAT_PORT:str = '9002'

# password regex string
PASSWORD_REGEX_STRING:str = "(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$"

# activation code length
ACTIVATION_CODE_LENGTH:int = 6

# indent for chat messages
CHAT_MESSAGE_INDENT:str = '#=>  '

# app data storage path
DATA_STORAGE_PATH:str = os.path.join(os.path.expanduser('~'), '.schat_storage')

# local chat history database path
LOCAL_CHAT_HISTORY_DB_PATH:str = os.path.join(DATA_STORAGE_PATH, 'dbs')

# local chat history database file prefix
LOCAL_CHAT_HISTORY_DB_FILE_PREFIX:str = 'chat_db'

# local database extension
LOCAL_DB_EXTENSION:str = '.db'

# local chat history db template path
LOCAL_CHAT_HISTORY_DB_TEMPLATE_PATH:str = os.path.join(os.path.dirname(__file__), 'resources', 'chat_history_db_template' + LOCAL_DB_EXTENSION)

# maximum history database size in megabytes (MB)
MAXIMUM_CHAT_HISTORY_DB_SIZE = 50