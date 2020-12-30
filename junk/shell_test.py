# from prompt_toolkit import Application
# from prompt_toolkit.buffer import Buffer
# from prompt_toolkit.layout.containers import VSplit, HSplit, Window
# from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
# from prompt_toolkit.layout.layout import Layout
# from prompt_toolkit.key_binding import KeyBindings
# from prompt_toolkit.formatted_text import HTML
# from constants import *
# from prompt_styles import SenderPrompt, ReceiptPrompt
# import utils
# from prompt_toolkit.styles import Style

# # Editable buffers
# text_field_buffer = Buffer()

# # key binding object
# kb = KeyBindings()

# # formatted text controls for chat section
# chat_title = FormattedTextControl(focusable=False)
# chat_display = FormattedTextControl(style=('bg:ansiblack fg:ansicyan'), focusable=True)
# user_info = FormattedTextControl(focusable=False)

# # formatted text controls for contacts section
# contacts_title = FormattedTextControl(text=HTML('<aaa align="center">CONTACTS</aaa>'), focusable=False)
# contacts_display = FormattedTextControl(focusable=True)
# status_bar_content = FormattedTextControl(focusable=False)

# # borders
# horizonal_border = Window(height=1, char='+', style=('bg:ansiblack fg:ansigreen'))
# vertical_border = Window(width=1, char='|', style=('bg:ansiblack fg:ansigreen'))

# # chat sending and display windows
# chat_title_window = Window(content=chat_title, height=2, style=('bg:ansigreen fg:ansiwhite'))
# chat_display_window = Window(content=chat_display, wrap_lines=True, style=('bg:ansiblack fg:ansiwhite'))
# user_info_window = Window(content=user_info, height=2, style=('bg:ansigreen fg:ansiwhite'))
# text_field_window = Window(content=BufferControl(buffer=text_field_buffer), height=5, wrap_lines=True, style=('bg:ansiblack fg:ansiwhite'))

# # contacts display windows
# contacts_title_window = Window(content=contacts_title, width=30, height=2, wrap_lines=True, style=('bg:ansigreen fg:ansiwhite'))
# contacts_display_window = Window(content=contacts_display, width=30, wrap_lines=True, style=('bg:ansiblack fg:ansiwhite'))

# # status bar window
# status_bar_window = Window(content=status_bar_content, height=1, style=('bg:ansigreen fg:ansiwhite'))

# # create root container with all windows arranged
# chat_container = HSplit([
#     chat_title_window,
#     # horizonal_border,
#     chat_display_window,
#     # horizonal_border,
#     user_info_window,
#     # horizonal_border,
#     text_field_window,
# ])

# contacts_container = HSplit([
#     contacts_title_window,
#     # horizonal_border,
#     contacts_display_window,
# ])

# chat_and_contacts_container = VSplit([
#     contacts_container,
#     vertical_border,
#     chat_container,
# ])

# root_container = HSplit([
#     chat_and_contacts_container,
#     status_bar_window,
# ])

# # add events
# @kb.add('c-q')
# def _(event):
#     """
#     Press CTRL-Q to exit the user interface.
#     """
#     event.app.exit()

# @kb.add('tab')
# def _(event):
#     """
#     Press TAB to switch to next focusable window
#     """
#     event.app.layout.focus_next()

# @kb.add('c-e')
# def _(event):
#     """
#     Press CTRL-E to switch to message text field
#     """
#     event.app.layout.focus(text_field_window)

# @kb.add('c-r')
# def _(event):
#     """
#     Press CTRL-R to switch to chat display
#     """
#     event.app.layout.focus(chat_display_window)

# @kb.add('c-c')
# def _(event):
#     """
#     Press CTRL-C to switch to contacts display
#     """
#     event.app.layout.focus(contacts_display_window)

# @kb.add('c-m')
# def _(event):
#     """
#     Press enter to send messages
#     """
#     newlines = '\n\n' if not chat_display.text.strip() == '' else ''
#     chat_display.text = f'{chat_display.text}{newlines}{text_field_buffer.document.text}'
#     text_field_buffer.text = ''

# # @kb.add('down')
# # def _(event):
# #     text_field_buffer.join_next_line()


# layout = Layout(root_container)
# app = Application(layout=layout, key_bindings=kb, full_screen=True, mouse_support=True)
# app.run()



"""
Horizontal split example.
"""
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Float, FloatContainer, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame

LIPSUM = " ".join(
    (
        """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Maecenas quis interdum enim. Nam viverra, mauris et blandit malesuada, ante est
bibendum mauris, ac dignissim dui tellus quis ligula. Aenean condimentum leo at
dignissim placerat. In vel dictum ex, vulputate accumsan mi. Donec ut quam
placerat massa tempor elementum. Sed tristique mauris ac suscipit euismod. Ut
tempus vehicula augue non venenatis. Mauris aliquam velit turpis, nec congue
risus aliquam sit amet. Pellentesque blandit scelerisque felis, faucibus
consequat ante. Curabitur tempor tortor a imperdiet tincidunt. Nam sed justo
sit amet odio bibendum congue. Quisque varius ligula nec ligula gravida, sed
convallis augue faucibus. Nunc ornare pharetra bibendum. Praesent blandit ex
quis sodales maximus. """
        * 100
    ).split()
)


# 1. The layout
left_text = "Floating\nleft"
right_text = "Floating\nright"
top_text = "Floating\ntop"
bottom_text = "Floating\nbottom"
center_text = "Floating\ncenter"
quit_text = "Press 'q' to quit."


body = FloatContainer(
    content=Window(FormattedTextControl(LIPSUM), wrap_lines=True),
    floats=[
        # Important note: Wrapping the floating objects in a 'Frame' is
        #                 only required for drawing the border around the
        #                 floating text. We do it here to make the layout more
        #                 obvious.
        # Left float.
        Float(
            Frame(
                Window(FormattedTextControl(left_text), width=10, height=2),
                style="bg:#44ffff #ffffff",
            ),
            left=0,
        ),
        # Right float.
        Float(
            Frame(
                Window(FormattedTextControl(right_text), width=10, height=2),
                style="bg:#44ffff #ffffff",
            ),
            right=0,
        ),
        # Bottom float.
        Float(
            Frame(
                Window(FormattedTextControl(bottom_text), width=10, height=2),
                style="bg:#44ffff #ffffff",
            ),
            bottom=0,
        ),
        # Top float.
        Float(
            Frame(
                Window(FormattedTextControl(top_text), width=10, height=2),
                style="bg:#44ffff #ffffff",
            ),
            top=0,
        ),
        # Center float.
        Float(
            Frame(
                Window(FormattedTextControl(center_text), width=10, height=2),
                style="bg:#44ffff #ffffff",
            )
        ),
        # Quit text.
        Float(
            Frame(
                Window(FormattedTextControl(quit_text), width=18, height=1),
                style="bg:#ff44ff #ffffff",
            ),
            top=6,
        ),
    ],
)


# 2. Key bindings
kb = KeyBindings()


@kb.add("q")
def _(event):
    " Quit application. "
    event.app.exit()


# 3. The `Application`
application = Application(layout=Layout(body), key_bindings=kb, full_screen=True)


def run():
    application.run()


if __name__ == "__main__":
    run()