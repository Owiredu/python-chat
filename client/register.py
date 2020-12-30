from prompt_toolkit import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import TextArea, Label, Dialog, Button, Frame
from prompt_toolkit.layout.containers import HSplit, Float, FloatContainer
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
import socketio, threading, re, sys, os, time
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
        if registration_float in root_container.floats:
            if registration_dialog.ok_button.text == 'Submit':
                if registration_data['_from'] != '' and registration_data['username'] != '' and registration_data['password'] != '' and registration_data['msg_type'] == REGISTER:
                    if server_connection_status == ONLINE:
                        # show submission message
                        registration_dialog.error_label.text = registration_dialog.get_loading_message('Submitting data ...')
                        # send the data to the recipient
                        send(registration_data)
                        # disable the registration form widgets
                        registration_dialog.enable_form(False)
                        # clear the sender message
                        registration_data = dict(_from='', to=SERVER_NAME, username='', password='', activation_code='', file='', msg_type=REGISTER)
                    else:
                        # show error message
                        registration_dialog.error_label.text = registration_dialog.get_error_message('Offline! Connecting to server before submission ...')
        elif activation_float in root_container.floats:
            if activation_dialog.ok_button.text == 'Submit':
                if registration_data['activation_code'] != '' and registration_data['msg_type'] == ACTIVATION:
                    if server_connection_status == ONLINE:
                        # show submission message
                        activation_dialog.error_label.text = activation_dialog.get_loading_message('Activating account ...')
                        # send the data to the recipient
                        send(registration_data)
                        # disable the registration form widgets
                        activation_dialog.enable_form(False)
                        # clear the sender message
                        registration_data = dict(_from='', to=SERVER_NAME, username='', password='', activation_code='', file='', msg_type=ACTIVATION)
                    else:
                        # show error message
                        activation_dialog.error_label.text = activation_dialog.get_error_message('Offline! Connecting to server before activation ...')



@sio.event(namespace='/register')
def receive(data):
    if data['_from'] == SERVER_NAME:
        if registration_float in root_container.floats:
            if data['msg_type'] == ERROR:
                registration_dialog.error_label.text = registration_dialog.get_error_message(data['message'])
                registration_dialog.ok_button.text = 'Submit'
                registration_dialog.enable_form(True)
            else:
                registration_dialog.error_label.text = registration_dialog.get_success_message(data['message'])
                registration_dialog.ok_button.text = 'Continue'
                registration_dialog.enable_form(True)
        elif activation_float in root_container.floats:
            if data['msg_type'] == ERROR:
                activation_dialog.error_label.text = activation_dialog.get_error_message(data['message'])
                activation_dialog.ok_button.text = 'Submit'
                activation_dialog.enable_form(True)
            else:
                activation_dialog.error_label.text = activation_dialog.get_success_message(data['message'])
                activation_dialog.ok_button.text = 'Continue'
                activation_dialog.enable_form(True)


def connect_to_server():
    """
    Connects to the chat server
    """
    try:
        sio.connect(server_url, namespaces=['/register'])
        sio.wait()
    except:
        registration_dialog.error_label.text = registration_dialog.get_loading_message('Connecting to server ...')
        time.sleep(1)
        connect_to_server()


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

        self.ok_button = Button(text="Submit", handler=self.accept)
        self.cancel_button = Button(text="Cancel", handler=self.cancel)

        self.dialog = Dialog(
            title=self.title,
            body=input_area_hsplit,
            buttons=[self.ok_button, self.cancel_button],
            width=D(preferred=80),
            modal=True,
        )

    def accept(self):
        """
        Respond to okay button press
        """
        # reset registration data dict
        reset_registration_data()
        if self.ok_button.text == 'Submit':
            global registration_data
            registration_data['msg_type'] = REGISTER 

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
        else:
            # close the registration dialog and open the activation code dialog
            close_registration_dialog()
            open_activation_dialog()

    def cancel(self):
        """
        Respond to cancel option
        """
        # hide dialog 
        close_registration_dialog()
        # disconnect from server and quit app
        exit_app()

    def get_error_message(self, message):
        return FormattedText([('bg:red fg:white', message)])

    def get_loading_message(self, message):
        return FormattedText([('bg:orange fg:white', message)])

    def get_success_message(self, message):
        return FormattedText([('bg:green fg:white', message)])

    def enable_form(self, bool_val):
        self.email_textarea.control.focusable = lambda: bool_val
        self.username_textarea.control.focusable = lambda: bool_val
        self.password_textarea.control.focusable = lambda: bool_val
        self.ok_button.control.focusable = lambda: bool_val
        if bool_val:
            get_app().layout.focus(self.ok_button)
        else:
            get_app().layout.focus(self.cancel_button)

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


#--------------------- START ACTIVATION DIALOG ---------------------#

reg_activation_code = ''

def reset_activation_code():
    global registration_data
    registration_data['activation_code'] = ''

class ActivationDialog:

    def __init__(self):
        self.title = 'Activate sChat Account'
        self.code_sent_label = Label(text='Check your email for activation code')
        self.activation_code_label = Label(text='Enter activation code: ')     
        self.space_label = Label(text='')      

        self.activation_code_textarea = TextArea(
            multiline=False,
            width=D(preferred=40),
        )

        self.error_label = Label(
            text='',
            width=D(preferred=40),
        )

        activation_code_hsplit = HSplit([self.code_sent_label, self.space_label, self.activation_code_label, self.activation_code_textarea])

        input_area_hsplit = HSplit([activation_code_hsplit, self.space_label, self.error_label])

        self.ok_button = Button(text="Submit", handler=self.accept)
        self.cancel_button = Button(text="Cancel", handler=self.cancel)

        self.dialog = Dialog(
            title=self.title,
            body=input_area_hsplit,
            buttons=[self.ok_button, self.cancel_button],
            width=D(preferred=80),
            modal=True,
        )

    def accept(self):
        """
        Respond to okay button press
        """
        reset_activation_code()

        if self.ok_button.text == 'Submit':
            global registration_data
            registration_data['msg_type'] = ACTIVATION  

            # get the activation code
            reg_activation_code = self.activation_code_textarea.text.strip()

            # validate activation code as a 6-digit string
            if re.search(r'^[\d]{6}$', reg_activation_code):
                registration_data['activation_code'] = reg_activation_code
            else:
                self.error_label.text = self.get_error_message('Invalid activation code')
        else:
            # exit activation dialog and app when continue is pressed
            self.cancel()

    def cancel(self):
        """
        Respond to cancel option
        """
        # hide dialog 
        close_activation_dialog()
        # disconnect from server and quit app
        exit_app()

    def get_error_message(self, message):
        return FormattedText([('bg:red fg:white', message)])

    def get_loading_message(self, message):
        return FormattedText([('bg:orange fg:white', message)])

    def get_success_message(self, message):
        return FormattedText([('bg:green fg:white', message)])

    def enable_form(self, bool_val):
        self.activation_code_textarea.control.focusable = lambda: bool_val
        self.ok_button.control.focusable = lambda: bool_val
        if bool_val:
            get_app().layout.focus(self.ok_button)
        else:
            get_app().layout.focus(self.cancel_button)

    def __pt_container__(self):
        return self.dialog


activation_dialog = ActivationDialog()
activation_float = Float(activation_dialog)


def open_activation_dialog():
    """
    Opens the registration dialog
    """
    # show the registration dialog
    root_container.floats.insert(0, activation_float)
    get_app().layout.focus(activation_dialog)


def close_activation_dialog():
    """
    Closes the registration dialog
    """
    if activation_float in root_container.floats:
        root_container.floats.remove(activation_float)

#--------------------- END ACTIVATION DIALOG ---------------------#

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