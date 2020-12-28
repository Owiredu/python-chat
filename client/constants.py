# for connection status values
ONLINE = 1 # signifies the the client/sender is online
OFFLINE = 0 # signifies that the client/sender is offline
MESSAGE_THREAD_UP = 6 # signifies that the messaging thread has already started
MESSAGE_THREAD_DOWN = -6

# for message types
SUCCESS = 2 # for success notifications
ERROR = -2 # for error notifications 
REGISTER = 3 # for new client registration
NORMAL = 4 # for normal client to client messages
STATUS_UPDATE = 5 # notify a change in the online/offline status of a client

# server name for sending messages to clients
SERVER_NAME = 'server'