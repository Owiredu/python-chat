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
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.document import Document
from prompt_toolkit.lexers import Lexer
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

# get chat message indent
chat_message_indent = ' ' * 5

# key binding object
kb = KeyBindings()

#################### SEND/RECIEVE MESSAGE WIDGETS ####################

def get_sender_message(buffer):
    """
    Get text from the message text area
    """
    existing_messages = chat_textarea.text
    message_prefix =  f'({get_current_datetime()})-{sender_email}[{sender_username}]--' + '{\n' 
    message_suffix = '\n}'
    updated_messages = ''

    new_message = '\n'.join([chat_message_indent + line for line in buffer.text.split('\n')])

    if chat_textarea.document.line_count <= 1:
        updated_messages = existing_messages + message_prefix + new_message + message_suffix
    else:
        updated_messages = existing_messages + '\n\n' + message_prefix + new_message + message_suffix

    chat_textarea.document = Document(text=updated_messages, cursor_position=len(updated_messages))
    # TODO: send the message to the recipient
    buffer.text = ''
    return True


def send_message_button_handler():
    """
    Sends the message to the recipient when the send button is clicked
    """
    existing_messages = chat_textarea.text
    message_prefix =  f'({get_current_datetime()})-{sender_email}[{sender_username}]--' + '{\n' 
    message_suffix = '\n}'
    updated_messages = ''

    new_message = '\n'.join([chat_message_indent + line for line in message_textarea.text.split('\n')])

    if chat_textarea.document.line_count <= 1:
        updated_messages = existing_messages + message_prefix + new_message + message_suffix
    else:
        updated_messages = existing_messages + '\n\n' + message_prefix + new_message + message_suffix

    chat_textarea.document = Document(text=updated_messages, cursor_position=len(updated_messages))
    # TODO: send the message to the recipient
    message_textarea.text = ''


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
send_message_frame = Frame(title=get_status_text(sender_alias, sender_connection_status), body=send_message_container)

class ChatLexer(Lexer):

    # def lex_document(self, document):

    #     def get_line(lineno):
    #         return [
    #             ('ansicyan', sender_email),
    #             ('#00aa00', '['),
    #             ('#ffff00', sender_username),
    #             ('#00aa00', ']'),
    #             ('#00aa00', '--{'),
    #             ('', '\n'),
    #             ('#ffffff', document.text[:-1].split('{')[-1]),
    #             ('#00aa00', '}'),
    #             ('', '\n\n')
    #         ]
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

@kb.add('c-q')
def _(event):
    """
    Press CTRL-Q to exit the user interface.
    """
    event.app.exit()


style = Style.from_dict(
    {
        "status": "reverse",
        "status.position": "#aaaa00",
        "status.key": "#ffaa00",
        "not-searching": "#888888",
    }
)


root_container = None
layout = Layout(chat_message_container, focused_element=message_textarea)
app = Application(layout=layout, key_bindings=kb, full_screen=True, mouse_support=True, refresh_interval=0.11, style=style)
app.run()