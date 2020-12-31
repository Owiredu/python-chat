import eventlet
from threading import Thread
from queue import Queue
import socketio
from pyisemail import is_email
from constants import (CHAT_PORT, OFFLINE, STATUS_UPDATE, ONLINE, NORMAL, ERROR, SUCCESS, SERVER_NAME)
from database import UsersDb
from status_update import StatusUpdateThread


sio = socketio.Server() # socketio.Server(logger=True, engineio_logger=True)
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'server/templates/index.html'}
})
# get table objects
db = UsersDb()
db_conn = db.db_conn
users_table = db.table('users')
# track number of user connected
num_of_clients_connected = 0

# start the status update thread
status_update_thread = StatusUpdateThread()
status_update_thread.start()


@sio.event(namespace='/chat')
def connect(sid, environ):
    """
    Handle client connections 
    """
    # print connected user count
    global num_of_clients_connected    
    num_of_clients_connected += 1
    print('\n' + '-' * 30)
    print('Client disconnected:', sid)
    print('Number of clients connected:', num_of_clients_connected)
    print('-' * 30, '\n')


@sio.event(namespace='/chat')
def receive(sid, data):
    """
    Handle messages from clients
    """
    if data['msg_type'] == STATUS_UPDATE:
        if data['message'] == ONLINE:
            # update the status to online
            status_update_thread.add_to_queue(sid, data['_from'], ONLINE)
        else:
            # change the user's status to offline
            status_update_thread.add_to_queue(sid, data['_from'], OFFLINE)
    if data['msg_type'] == NORMAL:
        # TODO: forward the message to the addressed recipient
        print('\n', '-' * 30)
        print('FROM: '+ data['_from'], '\nTO:', data['to'], '\nMESSAGE: ', data['message'], '\nFILE:', data['file'], '\nMSG_TYPE:', data['msg_type'])
        print('-' * 30, '\n')
        # sio.emit('receive', 'Server response', namespace='/chat', room=sid)


@sio.event(namespace='/chat')
def disconnect(sid):
    """
    Handle disconnection of clients
    """
    # change the user's status to offline
    status_update_thread.add_to_queue(sid, None, OFFLINE) 
    # print connected user count
    global num_of_clients_connected
    num_of_clients_connected -= 1
    print('\n' + '-' * 30)
    print('Client connected:', sid)
    print('Number of clients connected:', num_of_clients_connected)
    print('-' * 30, '\n')  
    

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', int(CHAT_PORT))), app)