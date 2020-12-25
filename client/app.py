from prompt_toolkit import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.widgets import (TextArea, Label, MenuContainer, SearchToolbar, MenuItem, 
                                    FormattedTextToolbar, Checkbox, RadioList, Box, Dialog, 
                                    Frame, Button, SystemToolbar, VerticalLine, HorizontalLine)
from prompt_toolkit.layout.containers import VSplit, HSplit
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText, HTML
from utils import get_current_datetime


# get users' data
sender_username = "Owiredu"
sender_alias = "You"
sender_email = "nanakofiowiredu@gmail.com"
recipient_username = "Samson"
recipient_email = "samsom@yahoo.com"
sender_connection_status = "Online"
recipient_connection_status = "Offline"

# get current datetime
current_datetime = get_current_datetime()

# key binding object
kb = KeyBindings()

#################### SEND/RECIEVE MESSAGE WIDGETS ####################

def get_sender_message(buffer):
    """
    Get text from the message text area
    """
    message = get_chat_text(sender_email, sender_alias, buffer.text)
    chat_textarea.buffer.insert_text(message)
    # TODO: send the message to the recipient
    buffer.text = ''
    return True


def send_message_button_handler():
    """
    Sends the message to the recipient when the send button is clicked
    """
    message = get_chat_text(sender_email, sender_alias, message_textarea.text)
    chat_textarea.buffer.insert_text(HTML('<aaa fg="red">afdkjasflkjasfd</aaa>'))
    # send the message to the recipient
    message_textarea.text = ''


def get_prefix_text(email, username):
    """
    Returns the formatted text for the message and chat prefix
    """
    formatted_text = FormattedText([
        ('ansicyan', sender_email),
        ('#ffa500', '-'),
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
    if x == 0:
        return formatted_text
    return ' ' * len(f'{sender_email}{sender_username}-[]# ')


def get_chat_text(email, username, message):
    """
    Returns the prefix for the send message textarea
    """
    formatted_text = FormattedText([
        ('ansicyan', sender_email),
        ('#ffa500', '-'),
        ('#00aa00', '['),
        ('#ffff00', sender_username),
        ('#00aa00', ']'),
        ('#00aa00', '-[ '),
        ('', '\n'),
        ('#ffffff', message),
        ('', '\n\n')
    ])
    return formatted_text


message_textarea = TextArea(accept_handler=get_sender_message, multiline=True, scrollbar=True, get_line_prefix=get_message_line_prefix)
send_message_button = Button('Send', handler=send_message_button_handler)
send_message_container = VSplit([
    message_textarea,
    VerticalLine(),
    send_message_button,
])
send_message_frame = Frame(title=get_status_text(sender_alias, sender_connection_status), body=send_message_container)


chat_textarea = TextArea(multiline=True, scrollbar=True, read_only=True)
chat_frame = Frame(title=get_status_text(recipient_username, recipient_connection_status), body=chat_textarea)

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
    else:
        get_app().layout.focus(message_textarea)

#################### GENERAL ####################

@kb.add('c-q')
def _(event):
    """
    Press CTRL-Q to exit the user interface.
    """
    event.app.exit()


root_container = None
layout = Layout(chat_message_container)
app = Application(layout=layout, key_bindings=kb, full_screen=True, mouse_support=True, refresh_interval=0.5)
app.run()