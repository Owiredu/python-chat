from prompt_toolkit import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import TextArea, Label, Dialog, Button, Frame
from prompt_toolkit.layout.containers import HSplit, Float, FloatContainer
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
import socketio, threading, re, sys, os
from pyisemail import is_email
from constants import *


sio = socketio.Client() # socketio.Client(logger=True, engineio_logger=True)
server_url = 'http://localhost:' + REGISTER_PORT

# check whether the messaging thread has started or not
messages_thread_status = MESSAGE_THREAD_DOWN

# track the server connection status
server_connection_status = OFFLINE

# key binding object
kb = KeyBindings()

# create the default registration data
registration_data = dict(_from='', to=SERVER_NAME, username='', password='', activation_code='', file='', msg_type=REGISTER)


#--------------------- START CHAT BACKEND ---------------------#

@sio.event(namespace='/register')
def connect():
    # notify onlines
    global server_connection_status
    server_connection_status = ONLINE
    registration_frame.title = get_status_text('You', 'Online')
    registration_dialog.error_label.text = ''
    # notify server that client is online
    global messages_thread_status
    if messages_thread_status == MESSAGE_THREAD_DOWN:
        # start the background activity for sending data
        sio.start_background_task(send_text_data)
        messages_thread_status = MESSAGE_THREAD_UP


@sio.event(namespace='/register')
def connect_error(error_msg):
    registration_frame.title = get_status_text('You', 'Offline')


@sio.event(namespace='/register')
def disconnect():
    global server_connection_status
    server_connection_status = OFFLINE
    registration_frame.title = get_status_text('You', 'Offline')


@sio.event(namespace='/register')
def send(data):
    sio.emit('receive', data, namespace='/register')


def send_text_data():
    while True:
        sio.sleep(0)
        global registration_data, server_connection_status
        if registration_data['_from'] != '' and registration_data['username'] != '' and registration_data['password'] != '' and registration_data['msg_type'] == REGISTER:
            if server_connection_status == ONLINE:
                # show submission message
                registration_dialog.error_label.text = registration_dialog.get_loading_message('Submitting data ...')
                # send the data to the recipient
                send(registration_data)
            else:
                # show error message
                registration_dialog.error_label.text = registration_dialog.get_error_message('You are not connected to the server')
            # clear the sender message
            registration_data = dict(_from='', to=SERVER_NAME, username='', password='', activation_code='', file='', msg_type=REGISTER)


@sio.event(namespace='/register')
def receive(data):
    if data['_from'] == SERVER_NAME:
        if data['msg_type'] == ERROR:
            registration_dialog.error_label.text = registration_dialog.get_error_message(data['message'])
        else:
            registration_dialog.error_label.text = registration_dialog.get_success_message(data['message'])


def connect_to_server():
    """
    Connects to the chat server
    """
    try:
        sio.connect(server_url, namespaces=['/register'])
    except:
        # show error message
        registration_dialog.error_label.text = registration_dialog.get_error_message('Not connected to server. Use Ctrl + C to connect')
    sio.wait()


def start_registration_thread():
    """
    Starts the registration thread
    """
    try:
        sio_thread = threading.Thread(target=connect_to_server, daemon=True)
        sio_thread.start()
    except:
        pass

#--------------------- END CHAT BACKEND ---------------------#


#--------------------- START REGISTRATION DIALOG ---------------------#

reg_email = ''
reg_username = ''
reg_password = ''
reg_verification_code = ''


def reset_registration_data():
    """
    Resets the registration data dict
    """
    global registration_data
    registration_data = dict(_from='', to=SERVER_NAME, username='', password='', activation_code='', file='', msg_type=REGISTER)


class RegistrationDialog:
    def __init__(self):
        self.title = 'Sign Up to sChat'
        self.email_label = Label(text='Email: ')
        self.username_label = Label(text='Username: ')
        self.password_label = Label(text='Password: ')
        self.space_label = Label(text='')

        registration_data['msg_type'] = REGISTER

        def accept():
            """
            Respond to okay button press
            """
            # reset registration data dict
            reset_registration_data()

            # get the registration data
            reg_email = self.email_textarea.text.strip()
            reg_username = self.username_textarea.text
            reg_password = self.password_textarea.text

            # validate email
            if is_email(reg_email):
                registration_data['_from'] = reg_email
            else:
                self.error_label.text = self.get_error_message('Invalid email')

            # validate username
            if len(reg_username) >= 4:
                if not re.search(r'[^\w\_]+', reg_username):
                    registration_data['username'] = reg_username
                else:
                    self.error_label.text = self.get_error_message('User must contain only alphabets and numbers')
            else:
                self.error_label.text = self.get_error_message('Username must be at least 4 characters long')

            # validate password
            if re.search(PASSWORD_REGEX_STRING, reg_password):
                registration_data['password'] = reg_password
            else:
                self.error_label.text = self.get_error_message('Invalid password')


        def cancel():
            """
            Respond to cancel option
            """
            # hide dialog 
            close_registration_dialog()
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

        self.error_label = Label(
            text='',
            width=D(preferred=40),
        )

        email_hsplit = HSplit([self.email_label, self.email_textarea])
        username_hsplit = HSplit([self.username_label, self.username_textarea])
        password_hsplit = HSplit([self.password_label, self.password_textarea])

        input_area_hsplit = HSplit([email_hsplit, username_hsplit, password_hsplit, self.space_label, self.error_label])

        ok_button = Button(text="Continue", handler=accept)
        cancel_button = Button(text="Cancel", handler=cancel)

        self.dialog = Dialog(
            title=self.title,
            body=input_area_hsplit,
            buttons=[ok_button, cancel_button],
            width=D(preferred=80),
            modal=True,
        )

    def get_error_message(self, message):
        return FormattedText([('bg:red fg:white', message)])

    def get_loading_message(self, message):
        return FormattedText([('bg:orange fg:white', message)])

    def get_success_message(self, message):
        return FormattedText([('bg:green fg:white', message)])

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


def close_registration_dialog():
    """
    Closes the registration dialog
    """
    if registration_float in root_container.floats:
        root_container.floats.remove(registration_float)

#--------------------- END REGISTRATION DIALOG ---------------------#

def get_status_text(label, status):
    """
    Returns a formatted status text
    """
    formatted_text = FormattedText([
        ('#ffffff', f'{label}: '),
        ('#00aa00' if status.lower() == 'online' else '#ff0066', status),
    ])
    return formatted_text


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


@kb.add('c-c')
def _(event):
    """
    Press CTRL-C to connect to the server
    """
    if messages_thread_status == MESSAGE_THREAD_DOWN:
        registration_dialog.error_label.text = registration_dialog.get_loading_message('Connecting to server ...')
        start_registration_thread()


# start the registration thread
start_registration_thread()

# put interface together
registration_frame = Frame(title=get_status_text('You', 'Offline'), body=HSplit([]))
root_container = FloatContainer(content=registration_frame, floats=[])
layout = Layout(root_container, focused_element=registration_dialog)
app = Application(layout=layout, key_bindings=kb, full_screen=True, mouse_support=True, refresh_interval=0.11)

# open the registration dialog
open_registration_dialog()

# run the application
app.run()