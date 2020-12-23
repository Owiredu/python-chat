import socketio
import threading
from constants import *


sio = socketio.Client() # socketio.Client(logger=True, engineio_logger=True)
server_url = 'http://localhost:5000'
my_contact = 'nkowiredu@gmail.com'
contacts = dict() # (email: username)


@sio.event(namespace='/chat')
def connect():
    print('\n' + '-' * 20, 'Connected to server', '-' * 20, '\n')
    # notify server that client is online
    data = dict(_from=my_contact, to=SERVER_NAME, message=ONLINE, file=None, msg_type=STATUS_UPDATE)
    send(data)
    # start the background activity for sending data
    sio.start_background_task(send_text_data)


@sio.event(namespace='/chat')
def connect_error(error_msg):
    print('\n' + '-' * 20, f'Error: {error_msg}', '-' * 20, '\n')


@sio.event(namespace='/chat')
def disconnect():
    print('\n' + '-' * 20, 'Disconnected from server', '-' * 20, '\n')


@sio.event(namespace='/chat')
def send(data):
    sio.emit('receive', data, namespace='/chat')


def send_text_data():
    while True:
        #data = dict() # (from, to, text, file[dict] = [filename, file type, file data])
        data = dict(_from=my_contact, to='jason@gmail.com', message='', file=None, msg_type=REGISTER)
        data['message'] = input("Enter message: ").strip()
        if not data['message'] == '':
            # disconnect from server when quitting
            if data['message'].strip().lower() == '/quit':
                sio.disconnect()
                break
            # send the data to the recipient
            send(data)


@sio.event(namespace='/chat')
def receive(data):
    if data['_from'] == SERVER_NAME:
        # handle server messages
        pass
    else:
        print(f"{data['_from']}: {data['message']}")


sio.connect(server_url, namespaces=['/chat'])
sio.wait()