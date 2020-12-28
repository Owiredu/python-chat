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
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.shortcuts import input_dialog
from utils import get_current_datetime
import socketio
import threading, time
from constants import *
import sys


sio = socketio.Client() # socketio.Client(logger=True, engineio_logger=True)
server_url = 'http://localhost:5000'
my_contact = 'nkowiredu@gmail.com'
contacts = dict() # (email: username)
sender_message_type = NORMAL
sender_message = ''
messages_thread_status = MESSAGE_THREAD_DOWN

# get users' data
sender_username = "Owiredu"
sender_alias = "You"
sender_email = "nanakofiowiredu@gmail.com"
recipient_username = "Samson"
recipient_email = "samsom@yahoo.com"
recipient_connection_status = "Offline"

# get current datetime
current_datetime = get_current_datetime()

# get chat message indent
chat_message_indent = ' ' * 5

# get app name
app_name = 'sChat'

# key binding object
kb = KeyBindings()

#--------------------- START CHAT BACKEND ---------------------#

@sio.event(namespace='/chat')
def connect():
    send_message_frame.title = get_status_text('You', 'Online')
    # notify server that client is online
    global messages_thread_status
    if messages_thread_status == MESSAGE_THREAD_DOWN:
        data = dict(_from=my_contact, to=SERVER_NAME, message=ONLINE, file=None, msg_type=STATUS_UPDATE)
        send(data)
        # start the background activity for sending data
        sio.start_background_task(send_text_data)
        messages_thread_status = MESSAGE_THREAD_UP


@sio.event(namespace='/chat')
def connect_error(error_msg):
    send_message_frame.title = get_status_text('You', 'Offline')


@sio.event(namespace='/chat')
def disconnect():
    send_message_frame.title = get_status_text('You', 'Offline')


@sio.event(namespace='/chat')
def send(data):
    sio.emit('receive', data, namespace='/chat')


def send_text_data():
    while True:
        #data = dict() # (from, to, text, file[dict] = [filename, file type, file data])
        data = dict(_from=my_contact, to='jason@gmail.com', message='', file=None, msg_type=NORMAL)
        global sender_message, sender_message_type
        data['msg_type'] = sender_message_type
        data['message'] = sender_message
        if not data['message'] == '':
            # disconnect from server when quitting
            if data['message'].strip().lower() == '/quit':
                sio.disconnect()
                break
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


def start_instant_messaging():
    """
    Connects to the chat server
    """
    sio.connect(server_url, namespaces=['/chat'])
    sio.wait()

#--------------------- END CHAT BACKEND ---------------------#



#--------------------- START REGISTRATION DIALOG ---------------------#

reg_email = ''
reg_username = ''
password = ''
verification_code = ''

class RegistrationDialog:
    def __init__(self):
        self.title = 'Sign Up to sChat'
        self.email_label = 'Email: '
        self.username_label = 'Username: '
        self.password_label = 'Password: '

        def accept():
            """
            Respond to okay button press
            """
            message_textarea.text = self.text_area.text

        def cancel():
            """
            Respond to cancel option
            """
            # hide dialog 
            if registration_float in root_container.floats:
                root_container.floats.remove(registration_float)
            # disconnect from server and quit app
            exit_app()
            

        self.email_textarea = TextArea(
            multiline=False,
            width=D(preferred=40),
        )

        self.username_textarea = TextArea(
            multiline=False,
            width=D(preferred=40),
        )

        self.password_textarea = TextArea(
            multiline=False,
            width=D(preferred=40),
            password=True
        )

        email_hsplit = HSplit([Label(text=self.email_label), self.email_textarea])
        username_hsplit = HSplit([Label(text=self.username_label), self.username_textarea])
        password_hsplit = HSplit([Label(text=self.password_label), self.password_textarea])

        input_area_hsplit = HSplit([email_hsplit, username_hsplit, password_hsplit])

        ok_button = Button(text="Continue", handler=accept)
        cancel_button = Button(text="Cancel", handler=cancel)

        self.dialog = Dialog(
            title=self.title,
            body=input_area_hsplit,
            buttons=[ok_button, cancel_button],
            width=D(preferred=80),
            modal=True,
        )

    def __pt_container__(self):
        return self.dialog


registration_dialog = RegistrationDialog()
registration_float = Float(registration_dialog)

def open_registration_dialog():
    """
    Opens the registration dialog
    """
    # show the registration dialog
    root_container.floats.insert(0, registration_float)
    get_app().layout.focus(registration_dialog)

#--------------------- END REGISTRATION DIALOG ---------------------#



#--------------------- START CHAT FRONTEND ---------------------#

#################### SEND/RECIEVE MESSAGE WIDGETS ####################

def get_sender_message(buffer):
    """
    Get text from the message text area
    """
    existing_messages = chat_textarea.text
    message_prefix =  f'({get_current_datetime()})-{sender_email}[{sender_username}]--' + '{\n' 
    message_suffix = '\n}'
    updated_messages = ''

    original_message = buffer.text
    if original_message.strip() != '':
        new_message = '\n'.join([chat_message_indent + line for line in original_message.split('\n')])

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
    existing_messages = chat_textarea.text
    message_prefix =  f'({get_current_datetime()})-{sender_email}[{sender_username}]--' + '{\n' 
    message_suffix = '\n}'
    updated_messages = ''

    original_message = message_textarea.text
    if original_message.strip() != '':
        new_message = '\n'.join([chat_message_indent + line for line in original_message.split('\n')])

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
        ('ansicyan', sender_email),
        # ('#ffa500', '-'),
        ('#00aa00', '['),
        ('#ffff00', sender_username),
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


message_textarea = TextArea(accept_handler=get_sender_message, multiline=True, scrollbar=True, get_line_prefix=get_message_line_prefix)
send_message_button = Button('Send', handler=send_message_button_handler)
send_message_container = VSplit([
    message_textarea,
    VerticalLine(),
    send_message_button,
])
send_message_frame = Frame(title=get_status_text(sender_alias, 'Offline'), body=send_message_container)

class ChatLexer(Lexer):
    """
    This is controls syntax highlighting in the chat area
    """

    def lex_document(self, document):

        def get_line(lineno):
            style = []
            line = document.lines[lineno]
            if line.startswith('(') and line.endswith(']--{'):
                # style for message prefix. Eg. (2020-12-26 22:58:09)-nanakofiowiredu@gmail.com[Owiredu]--{
                datetime_with_left_bracket, email_username_symbols = line.split(')-') # (2020-12-26 22:58:09 and nanakofiowiredu@gmail.com[Owiredu]--{
                email, username = email_username_symbols[:-4].split('[') # nanakofiowiredu@gmail.com and Owiredu
                style.append(('#ff0066', datetime_with_left_bracket + ')'))
                style.append(('#00aa00', '-'))
                style.append(('ansicyan', email))
                style.append(('#00aa00', '['))
                style.append(('#ffff00', username))
                style.append(('#00aa00', ']'))
                style.append(('orange', '--{'))
            elif line.startswith(chat_message_indent):
                # style for actual message
                style.append(('#ffffff', line))
            elif line.startswith('}'):
                # style for message suffix
                style.append(('orange', '}'))
            return style

        return get_line

chat_search_field = SearchToolbar(text_if_not_searching=[("class:not-searching", "Press '/' to start searching.")], forward_search_prompt=get_search_prompt('Forward'), 
                                    backward_search_prompt=get_search_prompt('Backward'), ignore_case=True)
chat_textarea = TextArea(multiline=True, scrollbar=True, read_only=True, search_field=chat_search_field, lexer=ChatLexer()) # lexer=DynamicLexer(lambda: ChatLexer())
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
    if not get_app().layout.has_focus(registration_dialog):
        if get_app().layout.has_focus(message_textarea):
            get_app().layout.focus(send_message_button)
        elif get_app().layout.has_focus(send_message_button):
            get_app().layout.focus(message_textarea)


@kb.add('c-c')
def _(event):
    """
    Press CTRL-C to switch between message area and chat area
    """
    if not get_app().layout.has_focus(registration_dialog):
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


@kb.add('c-s')
def _(event):
    """
    Press CTRL-S to connect to the server
    """
    sio_thread.start()


@kb.add('c-a')
def _(event):
    """
    Press CTRL-R open dialog
    """
    root_container.floats.insert(0, registration_float)
    get_app().layout.focus(registration_dialog)


@kb.add('c-r')
def _(event):
    """
    Press CTRL-R open dialog
    """
    if registration_float in root_container.floats:
        root_container.floats.remove(registration_float)
        get_app().layout.focus(message_textarea)


style = Style.from_dict(
    {
        "status": "reverse",
        "status.position": "#aaaa00",
        "status.key": "#ffaa00",
        "not-searching": "#888888",
    }
)


try:
    print(open('client/resources/banner.txt', 'r').read())
    time.sleep(2)
    # d = TextInputDialog(title='Test', label_text='Enter name: ')
    # text = input_dialog(title='Input dialog example', text='Please type your name:').run()
except:
    pass

sio_thread = threading.Thread(target=start_instant_messaging, daemon=True)
sio_thread.start()


root_container = FloatContainer(content=chat_message_container, floats=[])
layout = Layout(root_container, focused_element=registration_dialog)
app = Application(layout=layout, key_bindings=kb, full_screen=True, mouse_support=True, refresh_interval=0.11, style=style)
open_registration_dialog()  # TODO: check if registration file exists before showing dialog, implement continue action
app.run()

#--------------------- END CHAT FRONTEND ---------------------#