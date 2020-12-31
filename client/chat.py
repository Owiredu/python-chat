from prompt_toolkit import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import (TextArea, Label, MenuContainer, SearchToolbar, MenuItem, 
                                    FormattedTextToolbar, Checkbox, RadioList, Box, Dialog, 
                                    Frame, Button, SystemToolbar, VerticalLine, HorizontalLine)
from prompt_toolkit.layout.containers import VSplit, HSplit, Float, FloatContainer, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.document import Document
from utils import get_current_datetime
import socketio
import threading, time, re
from pyisemail import is_email
from constants import (
    MESSAGE_THREAD_UP, MESSAGE_THREAD_DOWN, CHAT_PORT, SERVER_NAME, STATUS_UPDATE, 
    ONLINE, OFFLINE, NORMAL, CHAT_MESSAGE_INDENT)
from chat_lexer import ChatLexer


# connection variables
sio = socketio.Client() # socketio.Client(logger=True, engineio_logger=True)
server_url = 'http://localhost:' + CHAT_PORT

# message variables
sender_message_type = NORMAL
sender_message = ''
messages_thread_status = MESSAGE_THREAD_DOWN

# track the server connection status
server_connection_status = OFFLINE

# get users' data
sender_username = "owiredu_nana_kofi"
sender_alias = "You"
sender_email = "nanakofiowiredu@gmail.com"
recipient_username = "Samson"
recipient_email = "samsom@yahoo.com"
recipient_connection_status = "Offline"

# get current datetime
current_datetime = get_current_datetime()

# get app name
app_name = 'sChat'

# key binding object
kb = KeyBindings()

#--------------------- START CHAT BACKEND ---------------------#

@sio.event(namespace='/chat')
def connect():
    global messages_thread_status, server_connection_status
    server_connection_status = ONLINE
    send_message_frame.title = get_status_text('You', 'Online')
    # send status update message
    data = dict(_from=sender_email, to=SERVER_NAME, message=ONLINE, file='', msg_type=STATUS_UPDATE)
    send(data)
    if messages_thread_status == MESSAGE_THREAD_DOWN:
        # start the background activity for sending data
        sio.start_background_task(send_text_data)
        messages_thread_status = MESSAGE_THREAD_UP


@sio.event(namespace='/chat')
def connect_error(error_msg):
    send_message_frame.title = get_status_text('You', 'Offline')


@sio.event(namespace='/chat')
def disconnect():
    global server_connection_status
    server_connection_status = OFFLINE
    send_message_frame.title = get_status_text('You', 'Offline')


@sio.event(namespace='/chat')
def send(data):
    sio.emit('receive', data, namespace='/chat')


def send_text_data():
    while True:
        sio.sleep(0)
        #data = dict() # (from, to, text, file[dict] = [filename, file type, file data])
        data = dict(_from=sender_email, to='jason@gmail.com', message='', file='', msg_type=NORMAL)
        global sender_message, sender_message_type
        data['msg_type'] = sender_message_type
        data['message'] = sender_message
        if not data['message'] == '':
            # send the data to the recipient
            send(data)
            # clear the sender message
            sender_message = ''


@sio.event(namespace='/chat')
def receive(data):
    if data['_from'] == SERVER_NAME:
        # handle server messages
        pass
    else:
        print(f"{data['_from']}: {data['message']}")


def connect_to_server():
    """
    Connects to the chat server
    """
    try:
        sio.connect(server_url, namespaces=['/chat'])
        sio.wait()
    except:
        time.sleep(1)
        connect_to_server()


def start_messaging_thread():
    """
    Starts the messaging thread
    """
    try:
        # print(open('client/resources/banner.txt', 'r').read())
        # time.sleep(2)
        sio_thread = threading.Thread(target=connect_to_server, daemon=True)
        sio_thread.start()
    except:
        pass

#--------------------- END CHAT BACKEND ---------------------#


#--------------------- START CHAT FRONTEND ---------------------#

#################### SEND/RECIEVE MESSAGE WIDGETS ####################

def get_sender_message(buffer):
    """
    Get text from the message text area
    """
    if messages_thread_status == MESSAGE_THREAD_UP:
        existing_messages = chat_textarea.text
        message_prefix =  f'({get_current_datetime()}){sender_email}[{sender_username}]' + '\n' 
        message_suffix = '\n'
        updated_messages = ''

        original_message = buffer.text
        if original_message.strip() != '':
            new_message = '\n'.join([CHAT_MESSAGE_INDENT + line for line in original_message.split('\n')])

            if chat_textarea.document.line_count <= 1:
                updated_messages = existing_messages + message_prefix + new_message + message_suffix
            else:
                updated_messages = existing_messages + '\n\n' + message_prefix + new_message + message_suffix

            chat_textarea.document = Document(text=updated_messages, cursor_position=len(updated_messages))
            buffer.text = ''
            # send the message to the recipient
            global sender_message, sender_message_type
            sender_message_type = NORMAL
            sender_message = original_message
    return True


def send_message_button_handler():
    """
    Sends the message to the recipient when the send button is clicked
    """
    if messages_thread_status == MESSAGE_THREAD_UP:
        existing_messages = chat_textarea.text
        message_prefix =  f'({get_current_datetime()}){sender_email}[{sender_username}]' + '\n' 
        message_suffix = '\n'
        updated_messages = ''

        original_message = message_textarea.text
        if original_message.strip() != '':
            new_message = '\n'.join([CHAT_MESSAGE_INDENT + line for line in original_message.split('\n')])

            if chat_textarea.document.line_count <= 1:
                updated_messages = existing_messages + message_prefix + new_message + message_suffix
            else:
                updated_messages = existing_messages + '\n\n' + message_prefix + new_message + message_suffix

            chat_textarea.document = Document(text=updated_messages, cursor_position=len(updated_messages))
            message_textarea.text = ''
            # send the message to the recipient
            global sender_message, sender_message_type
            sender_message_type = NORMAL
            sender_message = original_message


def get_prefix_text(email, username):
    """
    Returns the formatted text for the message and chat prefix
    """
    formatted_text = FormattedText([
        ('ansicyan', email),
        # ('#ffa500', '-'),
        ('#00aa00', '['),
        ('#ffff00', username),
        ('#00aa00', ']'),
        ('#00aa00', '# ')
    ])
    return formatted_text


def get_status_text(label, status):
    """
    Returns a formatted status text
    """
    formatted_text = FormattedText([
        ('#ffffff', f'{label}: '),
        ('#00aa00' if status.lower() == 'online' else '#ff0066', status),
    ])
    return formatted_text


def get_message_line_prefix(x, y):
    """
    Returns the prefix for the send message prompt
    """
    formatted_text = get_prefix_text(sender_email, sender_username)
    if x == 0 and y == 0:
        return formatted_text
    return ' ' * len(f'{sender_email}{sender_username}[]# ')


def get_search_prompt(type):
    """
    Returns the prefix for the search chat field
    """
    formatted_text = FormattedText([
        ('#00aa00', '['),
        ('#ffff00', f'{type} Search'),
        ('#00aa00', ']'),
        ('#00aa00', '# ')
    ])
    return formatted_text


# send message area
message_textarea = TextArea(accept_handler=get_sender_message, multiline=True, scrollbar=True, get_line_prefix=get_message_line_prefix)
send_message_button = Button('Send', handler=send_message_button_handler)
send_message_container = VSplit([
    message_textarea,
    VerticalLine(),
    send_message_button,
])
send_message_frame = Frame(title=get_status_text(sender_alias, 'Offline'), body=send_message_container)


# display chat area
chat_search_field = SearchToolbar(text_if_not_searching=[("class:not-searching", "Press '/' to start searching.")], forward_search_prompt=get_search_prompt('Forward'), 
                                    backward_search_prompt=get_search_prompt('Backward'), ignore_case=True)
chat_textarea = TextArea(multiline=True, scrollbar=True, read_only=True, search_field=chat_search_field, lexer=ChatLexer())
chat_hsplit = HSplit([
    chat_textarea,
    chat_search_field, 
])
chat_frame = Frame(title=get_status_text(recipient_username, recipient_connection_status), body=chat_hsplit)

chat_message_container = HSplit([
    chat_frame,
    send_message_frame,
])

@kb.add('c-i')
def _(event):
    """
    Press TAB key to toggle focus between the message textarea and send button
    """
    if get_app().layout.has_focus(message_textarea):
        get_app().layout.focus(send_message_button)
    elif get_app().layout.has_focus(send_message_button):
        get_app().layout.focus(message_textarea)


@kb.add('c-c')
def _(event):
    """
    Press CTRL-C to switch between message area and chat area
    """
    if get_app().layout.has_focus(chat_textarea):
        get_app().layout.focus(message_textarea)
    else:
        get_app().layout.focus(chat_textarea)

#################### GENERAL ####################

def exit_app():
    """
    Closes the connection and exits app
    """
    try:
        sio.disconnect()
    except:
        pass
    # exit application
    get_app().exit()


@kb.add('c-q')
def _(event):
    """
    Press CTRL-Q to exit the user interface.
    """
    exit_app()

# start the messaging thread
start_messaging_thread()


style = Style.from_dict(
    {
        "status": "reverse",
        "status.position": "#aaaa00",
        "status.key": "#ffaa00",
        "not-searching": "#888888",
    }
)

root_container = FloatContainer(content=chat_message_container, floats=[])
layout = Layout(root_container, focused_element=message_textarea)
app = Application(layout=layout, key_bindings=kb, full_screen=True, mouse_support=True, refresh_interval=0.11, style=style)
app.run()

#--------------------- END CHAT FRONTEND ---------------------#