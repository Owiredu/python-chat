import socketio
import threading


sio = socketio.Client() # socketio.Client(logger=True, engineio_logger=True)
server_url = 'http://localhost:5000'
contacts = dict() # (phone[key], username)


@sio.event(namespace='/chat')
def connect():
    print('\n', '-' * 20, 'Connected to server', '-' * 20, '\n')
    # start the thread for sending data
    sio.start_background_task(send_text_data)


@sio.event(namespace='/chat')
def connect_error(error_msg):
    print('\n', '-' * 20, f'Error: {error_msg}', '-' * 20, '\n')


@sio.event(namespace='/chat')
def disconnect():
    print('\n', '-' * 20, 'Disconnected from server', '-' * 20, '\n')


@sio.event(namespace='/chat')
def send(data):
    sio.emit('receive', data, namespace='/chat')


def send_text_data():
    while True:
        #data = dict() # (from, to, text, file[dict] = [filename, file type, file data])
        data = input("Enter message: ")
        if data.strip().lower() == 'quit':
            sio.disconnect()
            break
        send(data)


@sio.event(namespace='/chat')
def receive(data):
    print('MESSAGE: ', data)


sio.connect(server_url, namespaces=['/chat'])
sio.wait()