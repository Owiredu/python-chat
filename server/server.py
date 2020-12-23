import eventlet
import re
import socketio
from pyisemail import is_email
from constants import *


sio = socketio.Server() # socketio.Server(logger=True, engineio_logger=True)
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'server/templates/index.html'}
})
# get table objects
db = Database()
users_table = db.table('users')
# track number of user connected
num_of_clients_connected = 0


@sio.event(namespace='/chat')
def connect(sid, environ):
    """
    Handle client connections 
    """
    global num_of_clients_connected
    num_of_clients_connected += 1
    print('\n' + '-' * 30)
    print('Client connected:', sid)
    print('Number of clients connected:', num_of_clients_connected)
    print('-' * 30, '\n')


@sio.event(namespace='/chat')
def receive(sid, data):
    """
    Handle messages from clients
    """
    if data['msg_type'] == STATUS_UPDATE:
        # TODO: if the email already exists in the users table, update the status to online
        # TODO: if the email doesn't exist, send secret code to complete registration
        pass
    if data['msg_type'] == REGISTER:
        # register the client
        register(sid, data)
    if data['msg_type'] == NORMAL:
        # TODO: forward the message to the addressed recipient
        print('\n', '-' * 30)
        print('FROM:'+ data['_from'], '\nTO:', data['to'], '\nMESSAGE: ', data['message'], '\nFILE:', data['file'], '\nMSG_TYPE': data['msg_type'])
        print('-' * 30, '\n')
        # sio.emit('receive', 'Server response', namespace='/chat', room=sid)


def register(sid, data):
    """
    Register clients
    """
    try:
        # TODO: check if the email already exists before registering the user
        # get and validate email address
        email_address = data['email'].lower().strip()
        if not is_email(email_address, diagnose=True, check_dns=True):
            data = dict(_from=SERVER_NAME, to='', message=f'Invalid email address {email_address}', file=None, msg_type=ERROR)
            sio.emit('receive', data, namespace='/chat', room=sid)
        # get and validate username
        username = data['username'].strip()
        if not re.search(r'[^\w\_]+', username):
            data = dict(_from=SERVER_NAME, to='', message=f'Invalid username ({username}): Only alphabets, numbers and underscore (_) allowed.', file=None, msg_type=ERROR)
            sio.emit('receive', data, namespace='/chat', room=sid)
        # get and hash the password
        password = data['password']
        password_hash = db.get_password_hash(password)
        # submit the user's data
        result = users_table.insert().values(email=email, username=username, password_hash=password_hash, status=ONLINE, stored_messages=0, sid=sid)
        # send confirmation message to user
        data = dict(_from=SERVER_NAME, to='', message=f'Registration successful', file=None, msg_type=SUCCESS)
        sio.emit('receive', data, namespace='/chat', room=sid)
    except Exception as e:
        print(e)
        # send error message to the client
        data = dict(_from=SERVER_NAME, to='', message=f'Fatal error occurred. Try again.', file=None, msg_type=ERROR)
        sio.emit('receive', data, namespace='/chat', room=sid)


@sio.event(namespace='/chat')
def disconnect(sid):
    """
    Handle disconnection of clients
    """
    # TODO: change the user's status to offline if they exist in the database
    global num_of_clients_connected
    num_of_clients_connected -= 1
    print('\n' + '-' * 30)
    print('Client disconnected:', sid)
    print('Number of clients connected:', num_of_clients_connected)
    print('-' * 30, '\n')
    

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)