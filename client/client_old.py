import socketio
import threading
from constants import *
from prompt_styles import SenderPrompt, ReceiptPrompt, SystemPrompt
from utils import get_current_datetime
from threading import Timer
from prompt_toolkit.patch_stdout import patch_stdout


sio = socketio.Client() # socketio.Client(logger=True, engineio_logger=True)
server_url = 'http://localhost:5000'
my_contact = 'nkowiredu@gmail.com'
contacts = dict() # (email: username)


@sio.event(namespace='/chat')
def connect():
    SystemPrompt(get_current_datetime(), 'Connected to server', SUCCESS).print_text()
    # print('\n' + '-' * 20, 'Connected to server', '-' * 20, '\n')
    # notify server that client is online
    data = dict(_from=my_contact, to=SERVER_NAME, message=ONLINE, file=None, msg_type=STATUS_UPDATE)
    send(data)
    # start the background activity for sending data
    sio.start_background_task(send_text_data)


@sio.event(namespace='/chat')
def connect_error(error_msg):
    SystemPrompt(get_current_datetime(), f'Error: {error_msg}', ERROR).print_text()
    # print('\n' + '-' * 20, f'Error: {error_msg}', '-' * 20, '\n')


@sio.event(namespace='/chat')
def disconnect():
    SystemPrompt(get_current_datetime(), 'Disconnected from server', ERROR).print_text()
    # print('\n' + '-' * 20, 'Disconnected from server', '-' * 20, '\n')


@sio.event(namespace='/chat')
def send(data):
    sio.emit('receive', data, namespace='/chat')


def send_text_data():
    def just_a_thread(i, j):
        print_formatted_text(HTML(text.format(i, j)))
        Timer(random.uniform(1, 2), just_a_thread, [i, j+1]).start()

        Timer(random.uniform(1, 2), just_a_thread, [1, 1]).start()
        Timer(random.uniform(1, 2), just_a_thread, [2, 1]).start()
    while True:
        #data = dict() # (from, to, text, file[dict] = [filename, file type, file data])
        data = dict(_from=my_contact, to='jason@gmail.com', message='', file=None, msg_type=REGISTER)
        data['message'] = SenderPrompt('nk@gmail.com', 'Owiredu', 'Chat').get_prompt().strip()
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
try:
    print(open('client/resources/banner.txt', 'r').read())
except:
    pass
sio.wait()