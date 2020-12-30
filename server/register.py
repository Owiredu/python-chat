import eventlet
import re
import socketio
from pyisemail import is_email
from constants import *
from database import Database
from utils import generate_activation_code


sio = socketio.Server() # socketio.Server(logger=True, engineio_logger=True)
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'server/templates/index.html'}
})
# get table objects
db = Database() # database object
db_conn = db.db_conn # database connection object
users_table = db.table('users') # users table object

# track number of user connected
num_of_clients_connected = 0


@sio.event(namespace='/register')
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


@sio.event(namespace='/register')
def receive(sid, data):
    """
    Handle messages from clients
    """
    if data['msg_type'] == REGISTER:
        # register the client
        register(sid, data)
        # print(data)
    if data['msg_type'] == ACTIVATION:
        # activate account
        activate(sid, data)

def activate(sid, data):
    """
    Activates an account
    """
    try:
        # get and validate the activation code
        activation_code = data['activation_code'].strip()
        if not re.search(r'^[\d]{6}$', activation_code):
            data = dict(_from=SERVER_NAME, to='', message='Invalid activation code', file='', msg_type=ERROR)
            sio.emit('receive', data, namespace='/register', room=sid)
            return
        # updated the activation status
        existing_session_query = users_table.select().where(users_table.c.sid==sid)
        existing_session = db_conn.execute(existing_session_query).fetchone()
        # if the session exists, activate the account if not activated
        # if the session does not exist, send activation failed message and ask for registration
        if existing_session:
            if existing_session[-1] == 0: # check activation status
                if existing_session[-2] == activation_code: # check activation code
                    update_activation_status_query = users_table.update().where(users_table.c.sid==sid).values(activation_status=1)
                    db_conn.execute(update_activation_status_query)
                else:
                    data = dict(_from=SERVER_NAME, to='', message='Wrong activation code', file='', msg_type=ERROR)
                    sio.emit('receive', data, namespace='/register', room=sid)
                    return
            else:
                data = dict(_from=SERVER_NAME, to='', message='Account is already active. Login instead.', file='', msg_type=SUCCESS)
                sio.emit('receive', data, namespace='/register', room=sid)
                return
        else:
            # send activation failed since session does not exist
            data = dict(_from=SERVER_NAME, to='', message='Activation failed! Redo registration.', file='', msg_type=ERROR)
            sio.emit('receive', data, namespace='/register', room=sid)
            return
        # send confirmation message to user
        data = dict(_from=SERVER_NAME, to='', message=f'Activation successful', file='', msg_type=SUCCESS)
        sio.emit('receive', data, namespace='/register', room=sid)
    except Exception as e:
        print(e)
        # send error message to the client
        data = dict(_from=SERVER_NAME, to='', message=f'Fatal error occurred. Try again.', file='', msg_type=ERROR)
        sio.emit('receive', data, namespace='/register', room=sid)


def register(sid, data):
    """
    Register clients
    """
    try:
        # get and validate email address
        email_address = data['_from'].lower().strip()
        if not is_email(email_address, diagnose=True, check_dns=True):
            data = dict(_from=SERVER_NAME, to='', message='Invalid email', file='', msg_type=ERROR)
            sio.emit('receive', data, namespace='/register', room=sid)
            return
        # get and validate username
        username = data['username']
        if re.search(r'[^\w\_]+', username):
            data = dict(_from=SERVER_NAME, to='', message='Invalid username', file='', msg_type=ERROR)
            sio.emit('receive', data, namespace='/register', room=sid)
            return
        # get and hash the password
        password = data['password']
        if not re.search(PASSWORD_REGEX_STRING, password):
            data = dict(_from=SERVER_NAME, to='', message='Invalid password', file='', msg_type=ERROR)
            sio.emit('receive', data, namespace='/register', room=sid)
            return
        password_hash = db.get_password_hash(password)
        # generate secret code and send to the email
        activation_code = generate_activation_code()
        # check if the email already exists before registering the user
        # if the email already exists and is not activated replace it else send an error message
        existing_user_query = users_table.select().where(users_table.c.email==email_address)
        existing_user = db_conn.execute(existing_user_query).fetchone()
        if existing_user:
            if existing_user[-1] == 0:
                update_user_query = users_table.update().where(users_table.c.email==email_address).values(email=email_address, username=username, password_hash=password_hash, sid=sid, activation_code=activation_code)
                db_conn.execute(update_user_query)
            else:
                data = dict(_from=SERVER_NAME, to='', message='Account already exists. Use another email', file='', msg_type=ERROR)
                sio.emit('receive', data, namespace='/register', room=sid)
                return
        else:
            # submit the user's registration data
            insert_user_query = users_table.insert().values(email=email_address, username=username, password_hash=password_hash, sid=sid, activation_code=activation_code)
            db_conn.execute(insert_user_query)
        # send confirmation message to user
        data = dict(_from=SERVER_NAME, to='', message=f'Submission successful', file='', msg_type=SUCCESS)
        sio.emit('receive', data, namespace='/register', room=sid)
    except Exception as e:
        print(e)
        # send error message to the client
        data = dict(_from=SERVER_NAME, to='', message=f'Fatal error occurred. Try again.', file='', msg_type=ERROR)
        sio.emit('receive', data, namespace='/register', room=sid)


@sio.event(namespace='/register')
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
    eventlet.wsgi.server(eventlet.listen(('', int(REGISTER_PORT))), app)