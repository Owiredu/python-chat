from queue import Queue
from typing import Union
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
import threading, time
from constants import (
    MESSAGE_THREAD_UP, MESSAGE_THREAD_DOWN, CHAT_PORT, SERVER_NAME, STATUS_UPDATE, 
    ONLINE, OFFLINE, NORMAL, CHAT_MESSAGE_INDENT)
from chat_lexer import ChatLexer


# connection variables
sio:socketio.Client = socketio.Client(logger=False, engineio_logger=False) # socketio.Client(logger=True, engineio_logger=True)
server_url:str = 'http://localhost:' + CHAT_PORT

# message variables
sender_message_type:int = NORMAL
sender_message:str = ''
messages_thread_status:int = MESSAGE_THREAD_DOWN
receive_messages_queue:Queue = Queue()

# track the server connection status
server_connection_status:int = OFFLINE

# get users' data
# sender_username:str = "owiredu_nana_kofi"
# sender_alias:str = "You"
# sender_email:str = "nanakofiowiredu@gmail.com"
# recipient_username:str = "owiredu_hack"
# recipient_email:str = "khristinapiatek@gmail.com"
recipient_connection_status:str = "Offline"

sender_username:str = "owiredu_hack"
sender_alias:str = "You"
sender_email:str = "khristinapiatek@gmail.com"
recipient_username:str = "owiredu_nana_kofi"
recipient_email:str = "nanakofiowiredu@gmail.com"

# get current datetime
current_datetime:str = get_current_datetime()

# get app name
app_name:str = 'sChat'

# key binding object
kb:KeyBindings = KeyBindings()

#--------------------- START CHAT BACKEND ---------------------#

@sio.event(namespace='/chat')
def connect():
    global messages_thread_status, server_connection_status
    server_connection_status = ONLINE
    send_message_frame.title = get_status_text('You', 'Online')
    # send status update message
    data:dict = dict(_from={'email': sender_email, 'username': sender_username}, to=SERVER_NAME, message=ONLINE, file='', msg_type=STATUS_UPDATE)
    send(data)
    if messages_thread_status == MESSAGE_THREAD_DOWN:
        # start the background activity for sending data
        sio.start_background_task(send_text_data)
        # start backgroud task for receiving data
        sio.start_background_task(receive_messages)
        messages_thread_status = MESSAGE_THREAD_UP


@sio.event(namespace='/chat')
def connect_error(error_msg:str):
    send_message_frame.title = get_status_text('You', 'Offline')


@sio.event(namespace='/chat')
def disconnect():
    global server_connection_status
    server_connection_status = OFFLINE
    send_message_frame.title = get_status_text('You', 'Offline')


@sio.event(namespace='/chat')
def send(data:dict):
    sio.emit('receive', data, namespace='/chat')


def send_text_data() -> None:
    while True:
        sio.sleep(0)
        #data = dict() # (from, to, text, file[dict] = [filename, file type, file data])
        data:dict = dict(_from={'email': sender_email, 'username': sender_username}, to=recipient_email, message='', file='', msg_type=NORMAL)
        global sender_message, sender_message_type
        data['msg_type'] = sender_message_type
        data['message'] = sender_message
        if not data['message'] == '':
            # send the data to the recipient
            send(data)
            # clear the sender message
            sender_message = ''
            message_textarea.text = ''
            # focus on the message textarea
            get_app().layout.focus(message_textarea)


@sio.event(namespace='/chat')
def receive(data:dict):
    receive_messages_queue.put(data)


def connect_to_server() -> None:
    """
    Connects to the chat server
    """
    try:
        sio.connect(server_url, namespaces=['/chat'])
        sio.wait()
    except:
        time.sleep(1)
        connect_to_server()


def start_messaging_thread() -> None:
    """
    Starts the messaging thread
    """
    try:
        # print(open('client/resources/banner.txt', 'r').read())
        # time.sleep(2)
        sio_thread:threading.Thread = threading.Thread(target=connect_to_server, daemon=True)
        sio_thread.start()
    except:
        pass

#--------------------- END CHAT BACKEND ---------------------#


#--------------------- START CHAT FRONTEND ---------------------#

#################### SEND/RECIEVE MESSAGE WIDGETS ####################

def update_chat(new_message:str, email:str, username:str) -> None:
    """
    Updates the chat messages when a new message is sent or received
    """
    existing_messages:str = chat_textarea.text
    message_prefix:str =  f'({get_current_datetime()}){email}[{username}]' + '\n' 
    message_suffix:str = '\n'
    updated_messages:str = ''
    new_message:str = '\n'.join([CHAT_MESSAGE_INDENT + line for line in new_message.split('\n')])

    if chat_textarea.document.line_count <= 1:
        updated_messages = existing_messages + message_prefix + new_message + message_suffix
    else:
        updated_messages = existing_messages + '\n\n' + message_prefix + new_message + message_suffix

    chat_textarea.document = Document(text=updated_messages, cursor_position=len(updated_messages))


def receive_messages() -> None:
    """
    Receives messages from the server
    """
    while True:
        if not receive_messages_queue.empty():
            data:dict = receive_messages_queue.get()

            if data['_from']['username'] == SERVER_NAME:
                # TODO: log server messages to the a log file
                pass
            else:
                update_chat(data['message'], data['_from']['email'], data['_from']['username'])
                # TODO: save the message to the chat database


def send_message_button_handler() -> None:
    """
    Sends the message to the recipient when the send button is clicked
    """
    if messages_thread_status == MESSAGE_THREAD_UP:
        new_message:str = message_textarea.text
        if new_message.strip() != '':
            # update the chat
            update_chat(new_message, sender_email, sender_alias)
            # send the message to the recipient
            global sender_message, sender_message_type
            sender_message_type = NORMAL
            sender_message = new_message


def get_prefix_text(email:str, username:str) -> FormattedText:
    """
    Returns the formatted text for the message and chat prefix
    """
    formatted_text:FormattedText = FormattedText([
        ('ansicyan', email),
        # ('#ffa500', '-'),
        ('#00aa00', '['),
        ('#ffff00', username),
        ('#00aa00', ']'),
        ('#00aa00', '# ')
    ])
    return formatted_text


def get_status_text(label:str, status:str) -> FormattedText:
    """
    Returns a formatted status text
    """
    formatted_text:FormattedText = FormattedText([
        ('#ffffff', f'{label}: '),
        ('#00aa00' if status.lower() == 'online' else '#ff0066', status),
    ])
    return formatted_text


def get_message_line_prefix(x:int, y:int) -> Union[FormattedText, str]:
    """
    Returns the prefix for the send message prompt
    """
    formatted_text:FormattedText = get_prefix_text(sender_email, sender_username)
    if x == 0 and y == 0:
        return formatted_text
    return ' ' * len(f'{sender_email}{sender_username}[]# ')


def get_search_prompt(type:str) -> FormattedText:
    """
    Returns the prefix for the search chat field
    """
    formatted_text:FormattedText = FormattedText([
        ('#00aa00', '['),
        ('#ffff00', f'{type} Search'),
        ('#00aa00', ']'),
        ('#00aa00', '# ')
    ])
    return formatted_text


# send message area
message_textarea:TextArea = TextArea(multiline=True, scrollbar=True, get_line_prefix=get_message_line_prefix)
send_message_button:Button = Button('Send', handler=send_message_button_handler)
send_message_container:VSplit = VSplit([
    message_textarea,
    VerticalLine(),
    send_message_button,
])
send_message_frame:Frame = Frame(title=get_status_text(sender_alias, 'Offline'), body=send_message_container)


# display chat area
chat_search_field:SearchToolbar = SearchToolbar(text_if_not_searching=[("class:not-searching", "Press '/' to start searching.")], forward_search_prompt=get_search_prompt('Forward'), 
                                    backward_search_prompt=get_search_prompt('Backward'), ignore_case=True)
chat_textarea:TextArea = TextArea(multiline=True, scrollbar=True, read_only=True, search_field=chat_search_field, lexer=ChatLexer())
chat_hsplit:HSplit = HSplit([
    chat_textarea,
    chat_search_field, 
])
chat_frame:Frame = Frame(title=get_status_text(recipient_username, recipient_connection_status), body=chat_hsplit)

chat_message_container:HSplit = HSplit([
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

def exit_app() -> None:
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


style:Style = Style.from_dict(
    {
        "status": "reverse",
        "status.position": "#aaaa00",
        "status.key": "#ffaa00",
        "not-searching": "#888888",
    }
)

if __name__=='__main__':
    root_container:FloatContainer = FloatContainer(content=chat_message_container, floats=[])
    layout:Layout = Layout(root_container, focused_element=message_textarea)
    app:Application = Application(layout=layout, key_bindings=kb, full_screen=True, mouse_support=True, refresh_interval=0.11, style=style)
    app.run()

#--------------------- END CHAT FRONTEND ---------------------#