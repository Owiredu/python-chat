from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.formatted_text import HTML
from constants import *
from prompt_styles import SenderPrompt, ReceiptPrompt
import utils
from prompt_toolkit.styles import Style

# Editable buffers
text_field_buffer = Buffer()

# key binding object
kb = KeyBindings()

# formatted text controls for chat section
chat_title = FormattedTextControl(focusable=False)
chat_display = FormattedTextControl(style=('bg:ansiblack fg:ansicyan'), focusable=True)
user_info = FormattedTextControl(focusable=False)

# formatted text controls for contacts section
contacts_title = FormattedTextControl(text=HTML('<aaa align="center">CONTACTS</aaa>'), focusable=False)
contacts_display = FormattedTextControl(focusable=True)
status_bar_content = FormattedTextControl(focusable=False)

# borders
horizonal_border = Window(height=1, char='+', style=('bg:ansiblack fg:ansigreen'))
vertical_border = Window(width=1, char='|', style=('bg:ansiblack fg:ansigreen'))

# chat sending and display windows
chat_title_window = Window(content=chat_title, height=2, style=('bg:ansigreen fg:ansiwhite'))
chat_display_window = Window(content=chat_display, wrap_lines=True, style=('bg:ansiblack fg:ansiwhite'))
user_info_window = Window(content=user_info, height=2, style=('bg:ansigreen fg:ansiwhite'))
text_field_window = Window(content=BufferControl(buffer=text_field_buffer), height=5, wrap_lines=True, style=('bg:ansiblack fg:ansiwhite'))

# contacts display windows
contacts_title_window = Window(content=contacts_title, width=30, height=2, wrap_lines=True, style=('bg:ansigreen fg:ansiwhite'))
contacts_display_window = Window(content=contacts_display, width=30, wrap_lines=True, style=('bg:ansiblack fg:ansiwhite'))

# status bar window
status_bar_window = Window(content=status_bar_content, height=1, style=('bg:ansigreen fg:ansiwhite'))

# create root container with all windows arranged
chat_container = HSplit([
    chat_title_window,
    # horizonal_border,
    chat_display_window,
    # horizonal_border,
    user_info_window,
    # horizonal_border,
    text_field_window,
])

contacts_container = HSplit([
    contacts_title_window,
    # horizonal_border,
    contacts_display_window,
])

chat_and_contacts_container = VSplit([
    contacts_container,
    vertical_border,
    chat_container,
])

root_container = HSplit([
    chat_and_contacts_container,
    status_bar_window,
])

# add events
@kb.add('c-q')
def _(event):
    """
    Press CTRL-Q to exit the user interface.
    """
    event.app.exit()

@kb.add('tab')
def _(event):
    """
    Press TAB to switch to next focusable window
    """
    event.app.layout.focus_next()

@kb.add('c-e')
def _(event):
    """
    Press CTRL-E to switch to message text field
    """
    event.app.layout.focus(text_field_window)

@kb.add('c-r')
def _(event):
    """
    Press CTRL-R to switch to chat display
    """
    event.app.layout.focus(chat_display_window)

@kb.add('c-c')
def _(event):
    """
    Press CTRL-C to switch to contacts display
    """
    event.app.layout.focus(contacts_display_window)

@kb.add('c-m')
def _(event):
    """
    Press enter to send messages
    """
    newlines = '\n\n' if not chat_display.text.strip() == '' else ''
    chat_display.text = f'{chat_display.text}{newlines}{text_field_buffer.document.text}'
    text_field_buffer.text = ''

# @kb.add('down')
# def _(event):
#     text_field_buffer.join_next_line()


layout = Layout(root_container)
app = Application(layout=layout, key_bindings=kb, full_screen=True, mouse_support=True)
app.run()