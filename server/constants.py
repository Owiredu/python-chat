# for connection status values
ONLINE = 1 # signifies the the client/sender is online
OFFLINE = 0 # signifies that the client/sender is offline

# for account status
ACTIVE = 1
INACTIVE = 0

# for message types
SUCCESS = 2 # for success notifications
ERROR = -2 # for error notifications 
REGISTER = 3 # for new client registration
NORMAL = 4 # for normal client to client messages
STATUS_UPDATE = 5 # notify a change in the online/offline status of a client
ACTIVATION = 7 # for activation of account

# server name for sending messages to clients
SERVER_NAME = 'server'

# port numbers
REGISTER_PORT = '9000'
LOGIN_PORT = '9001'
CHAT_PORT = '9002'

# password regex string
PASSWORD_REGEX_STRING = "(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$"

# activation code length
ACTIVATION_CODE_LENGTH = 6

# maximum email sending retries
MAX_EMAIL_RETRIES = 3