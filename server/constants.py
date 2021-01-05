import os

# for connection status values
ONLINE:int = 1 # signifies the the client/sender is online
OFFLINE:int = 0 # signifies that the client/sender is offline

# for account status
ACTIVE:int = 1
INACTIVE:int = 0

# for stored message availability
MESSAGES_STORED:int = 1
NO_MESSAGES_STORED:int = 0

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

# maximum email sending retries
MAX_EMAIL_RETRIES:int = 3

# storage path
MESSAGES_STORAGE_PATH:str = os.path.join(os.path.dirname(__file__), 'storage', 'messages')